from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Tuple, Optional

import pandas as pd

from forecast_dataprep.data_enrichment.cyclical_features import add_cyclical_features
from forecast_dataprep.data_enrichment.delayed_features import add_delayed_consumption_feature
from forecast_dataprep.data_enrichment.national_holiday import add_national_holiday
from forecast_dataprep.data_enrichment.prices import add_prices
from forecast_dataprep.data_enrichment.school_holiday import add_school_holidays
from forecast_dataprep.data_enrichment.temperature import get_temperature_forecasts_from_metadata
from forecast_dataprep.data_enrichment.weekly_average import add_hour_of_the_week_average
from forecast_dataprep.data_fetching import get_dataframes, get_metadata
from forecast_dataprep.data_fetching.data_models import BigQueryBundle
from forecast_dataprep.data_ingestion.prediction import there_is_enough_historical_data
from forecast_dataprep.data_ingestion.shared import ingest_metadata_dataframe
from forecast_dataprep.data_ingestion.training import ingest_hourly_consumption_data
from forecast_dataprep.data_models import ModelTargetList, IngestedDataframes
from forecast_dataprep.data_enrichment.time_constants import TimeConstants
from forecast_dataprep.weather_api.data_models import WeatherApiBundle


def fetch_ingest_and_enrich(
        bq: BigQueryBundle,
        targets: ModelTargetList,
        timespan: Tuple[datetime, datetime],
        weather_api: WeatherApiBundle,
        training: bool = False,
        use_prices: bool = True,
        prediction_start: Optional[datetime] = None) -> pd.DataFrame:
    """
    Get data from BQ, then ingest and enrich it, so it can be used for training or prediction

    :param BigQueryBundle bq: Object with the BigQuery client and project details
    :param ModelTargetList targets: Object containing either meteringpoint or substation identifiers
    :param tuple timespan: datetime tuple with the start and end of the time period of interest
    :param WeatherApiBundle weather_api: Object with Weather API info and credentials
    :param bool training: True if training constraints should be applied on the data
    :param bool use_prices: If true, add the price information as an additional feature
    :param datetime prediction_start: Used only if not training. Adjusts the prediction horizon
    """
    # Step 0: Check input types
    if not isinstance(targets, ModelTargetList):
        raise TypeError

    # Step 1: Get metadata
    dfm = get_metadata(bq, targets)

    # Step 2: Branching. Separate route that run simultaneously to minimise run time
    with ThreadPoolExecutor() as executor:
        path_1_task = executor.submit(main_ingestion_and_enrichment_route, dfm,
                                      targets, bq, timespan, training,
                                      use_prices, prediction_start)
        path_2_task = executor.submit(get_temperature_forecasts_from_metadata,
                                      dfm, timespan, weather_api)
    df_hourly = path_1_task.result()
    df_temp = path_2_task.result()

    # Step 3: Merge route
    return finish_enrichment_process(df_hourly, df_temp)


def _enrich_hourly_consumption_data(ingested_hourly_consumption: pd.DataFrame,
                                    ingested_metadata: pd.DataFrame,
                                    pre_ingested: IngestedDataframes,
                                    timespan: Tuple[datetime, datetime],
                                    use_prices: bool) -> pd.DataFrame:
    """
    Adds features (cyclical, holidays, hour-of-the-week average consumption, shifted consumption) 
    to the hourly consumption data. The metadata dataframe needs to be enriched with fylke, as 
    this is needed to add the school holidays.

    :param bool use_prices: If true, add the price information as an additional feature
    """

    ingested_hourly_consumption = add_cyclical_features(
        ingested_hourly_consumption)

    ingested_hourly_consumption = add_national_holiday(
        ingested_hourly_consumption, pre_ingested.national_holidays,
        timespan[0], timespan[1])

    ingested_hourly_consumption = add_hour_of_the_week_average(
        ingested_hourly_consumption, pre_ingested.weekly_average)

    if use_prices:
        ingested_hourly_consumption = add_prices(ingested_hourly_consumption,
                                                 pre_ingested.prices)

    for delay in TimeConstants.DELAYED_FEATURES:
        ingested_hourly_consumption = add_delayed_consumption_feature(
            ingested_hourly_consumption, delay)

    ingested_hourly_consumption = add_school_holidays(
        ingested_hourly_consumption, pre_ingested.school_holidays,
        ingested_metadata, timespan[0], timespan[1])

    return ingested_hourly_consumption


def main_ingestion_and_enrichment_route(
        raw_metadata: pd.DataFrame,
        model_targets: ModelTargetList,
        bq: BigQueryBundle,
        timespan: Tuple[datetime, datetime],
        training: bool,
        use_prices: bool,
        prediction_start: Optional[datetime] = None) -> Optional[pd.DataFrame]:
    """
    This enrichment route is meant to run in parallel with :py:func:`~forecast_dataprep.data_enrichment.temperature.get_temperature_forecasts_from_metadata`

    :param pd.DataFrame raw_metadata: Result from :py:func:`~forecast_dataprep.data_fetching.__init__.get_metadata` 
    :param ModelTargetList model_targets: Object representing desired substations or meteringpoints
    :param BigQueryBundle bq: Object containing the BQ client and the BQ project name
    :param tuple timespan: datetime tuple with the start and end of the time period of interest
    :param bool training: If true, the hourly consumption data will be filtered using certain conditions
    :param bool use_prices: If true, add the price information as an additional feature
    :param datetime prediction_start: Point in time when one wants the prediction to start. Ignored if training
    :returns: pd.DataFrame or None if any of the input/intermediate dataframes is either empty or None. 
    """
    dfm_ingested = ingest_metadata_dataframe(raw_metadata)

    dfs = get_dataframes(bq, model_targets, timespan, use_prices)

    if dfs.hourly_consumption is None or dfs.hourly_consumption.empty:
        raise ValueError('No hourly consumption data')

    if training:
        dfh_ingested = ingest_hourly_consumption_data(timespan,
                                                      dfs.hourly_consumption)
    elif not there_is_enough_historical_data(
            dfs.hourly_consumption, TimeConstants.DELAYED_FEATURES,
            TimeConstants.FORECAST_HORIZON, prediction_start):
        raise ValueError('Not enough hourly consumption data')

    return _enrich_hourly_consumption_data(dfh_ingested, dfm_ingested,
                                           dfs.ingested, timespan, use_prices)


def finish_enrichment_process(
        enriched_hourly_data: Optional[pd.DataFrame],
        temperature_data: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Final stage of the ingestion and enrichment process. In this function two dataframes are 
    merged, each resulting from a different route: The main route dataframe, with most of the 
    features, and the dataframe with the temperature data coming from calls to Weather API.
    
    :param pd.DataFrame enriched_hourly_data: Result from :py:func:`~forecast_dataprep.methods.main_ingestion_and_enrichment_route` 
    :param pd.DataFrame temperature_data: Result from :py:func:`~forecast_dataprep.data_enrichment.temperature.get_temperature_forecasts_from_metadata` 
    :returns: pd.DataFrame or None if any of the input dataframes is either empty or None
    """
    if enriched_hourly_data is not None \
        and not enriched_hourly_data.empty and not temperature_data.empty:
        return enriched_hourly_data.reset_index().merge(
            temperature_data.rename(columns={'time': 'measurementTime'}),
            on=['measurementTime',
                'modelTargetId']).set_index('measurementTime')
    return None
