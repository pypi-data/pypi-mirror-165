"""
This module contains functions with queries specific for meteringpoints
"""
from typing import List

from google.cloud import bigquery
from google.cloud.bigquery.job import QueryJob
import pandas as pd

from forecast_dataprep.data_fetching.data_models import BigQueryBundle


def get_meteringpoint_hourly_data(bq: BigQueryBundle,
                                  mpid: List[int]) -> pd.DataFrame:
    query = (
        "SELECT meteringPointId AS modelTargetId, measurementTime, energyWh  "
        f"FROM `{bq.project.name}.{bq.project.dataset}.{bq.project.meteringpoint_hourly}` "
        "WHERE meteringPointId IN UNNEST(@mpid) "
        "ORDER BY meteringPointId DESC, measurementTime DESC ")

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ArrayQueryParameter("mpid", "INT64", mpid)])
    query_job: QueryJob = bq.client.query(query, job_config=job_config)

    result: pd.DataFrame = query_job.result().to_dataframe(
        create_bqstorage_client=False)
    result.set_index('measurementTime', inplace=True)
    return result


def get_meteringpoint_weekly_data(bq: BigQueryBundle,
                                  mpid: List[int]) -> pd.DataFrame:
    query = (
        "SELECT meteringPointId AS modelTargetId, hourOfWeek, medianEnergyWh "
        f"FROM `{bq.project.name}.{bq.project.dataset}.{bq.project.meteringpoint_weekly}` "
        "WHERE meteringPointId IN UNNEST(@mpid) "
        "ORDER BY meteringPointId DESC, hourOfWeek ASC ")

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ArrayQueryParameter("mpid", "INT64", mpid)])
    query_job: QueryJob = bq.client.query(query, job_config=job_config)

    result: pd.DataFrame = query_job.result().to_dataframe(
        create_bqstorage_client=False)
    result.set_index('hourOfWeek', inplace=True)
    return result


def get_meteringpoint_metadata(bq: BigQueryBundle,
                               mpid: List[int]) -> pd.DataFrame:
    query = (
        "SELECT meteringPointId AS modelTargetId, trafoId, latitude, longitude, municipalityNo, postalCode, consumptionCodeDescription, businessSectorDescription "
        f"FROM `{bq.project.name}.{bq.project.dataset}.{bq.project.meteringpoint_metadata}` "
        "WHERE meteringPointId IN UNNEST(@mpid) ")

    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ArrayQueryParameter("mpid", "INT64", mpid)])
    query_job: QueryJob = bq.client.query(query, job_config=job_config)

    result = query_job.result().to_dataframe(create_bqstorage_client=False)
    return result
