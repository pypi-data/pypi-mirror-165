from dataclasses import dataclass

from dbt.adapters.bigquery.connections import BigQueryAdapterResponse


@dataclass
class AlvinBigQueryAdapterResponse(BigQueryAdapterResponse):
    job_id: str = None
    alvin_platform_id: str = None
