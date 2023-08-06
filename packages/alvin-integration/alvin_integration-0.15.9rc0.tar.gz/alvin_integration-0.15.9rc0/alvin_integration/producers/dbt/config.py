from alvin_integration.interfaces.config import AbstractProducerConfig
from alvin_integration.models import AlvinPatch
from alvin_integration.producers.dbt.patch.functions import after_run, execute


class DBTProducerConfig(AbstractProducerConfig):
    @property
    def producer_name(self):
        return "dbt"

    def get_patching_list(self):
        return [
            AlvinPatch(
                package_name="dbt-core",
                function=after_run,
                supported_versions=["1.2.0"],
                destination_path="dbt.task.run.RunTask"
            ),
            AlvinPatch(
                package_name="dbt-core",
                function=execute,
                supported_versions=["1.2.0"],
                destination_path="dbt.adapters.bigquery.connections.BigQueryConnectionManager"
            )
        ]

    def get_lineage_config(self):
        pass

    def get_target_packages(self):
        return ["dbt-core"]

    def get_target_pipelines(self):
        pass