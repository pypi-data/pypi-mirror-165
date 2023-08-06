"""
This module contains functions with queries against Edna BQ, specific to substations
"""
from typing import List

from google.cloud import bigquery
from google.cloud.bigquery.job import QueryJob
import pandas as pd

from forecast_dataprep.data_fetching.data_models import BigQueryBundle


def get_substation_hourly_data(bq: BigQueryBundle,
                               substations: List[str]) -> pd.DataFrame:
    """
    Query and fetch historical hourly consumption for the substations selected.
    :params BigQueryBundle bq: object with a BigQuery client and project info
    """
    query = (
        "SELECT trafoId AS modelTargetId, measurementTime, energyWh  "
        f"FROM `{bq.project.name}.{bq.project.dataset}.{bq.project.substation_hourly}` "
        "WHERE trafoId IN UNNEST(@trafo) "
        "ORDER BY trafoId DESC, measurementTime DESC ")

    job_config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ArrayQueryParameter("trafo", "STRING", substations)
    ])
    query_job: QueryJob = bq.client.query(query, job_config=job_config)

    result: pd.DataFrame = query_job.result().to_dataframe(
        create_bqstorage_client=False)
    result.set_index('measurementTime', inplace=True)
    return result


def get_substation_weekly_data(bq: BigQueryBundle,
                               substation: List[str]) -> pd.DataFrame:
    query = (
        "SELECT trafoId AS modelTargetId, hourOfWeek, energyWh  "
        f"FROM `{bq.project.name}.{bq.project.dataset}.{bq.project.substation_weekly}` "
        "WHERE trafoId IN UNNEST(@trafo) "
        "ORDER BY trafoId DESC, hourOfWeek ASC ")

    job_config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ArrayQueryParameter("trafo", "STRING", substation)
    ])
    query_job: QueryJob = bq.client.query(query, job_config=job_config)

    result: pd.DataFrame = query_job.result().to_dataframe(
        create_bqstorage_client=False)
    result.set_index('hourOfWeek', inplace=True)
    return result


def get_substation_metadata(bq: BigQueryBundle,
                            substation: List[str]) -> pd.DataFrame:
    query = (
        "SELECT trafoId AS modelTargetId, latitude, longitude, municipalityNo "
        f"FROM `{bq.project.name}.{bq.project.dataset}.{bq.project.substation_metadata}` "
        "WHERE trafoId IN UNNEST(@trafo) ")

    job_config = bigquery.QueryJobConfig(query_parameters=[
        bigquery.ArrayQueryParameter("trafo", "STRING", substation)
    ])
    query_job: QueryJob = bq.client.query(query, job_config=job_config)

    result = query_job.result().to_dataframe(create_bqstorage_client=False)
    return result
