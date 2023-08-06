from pyspark.sql import DataFrame
from pyspark.sql import SparkSession

from tecton_proto.materialization.params_pb2 import MaterializationTaskParams


class MetricsCollector:
    def observe(self, df: DataFrame) -> DataFrame:
        raise NotImplementedError

    def publish(self):
        raise NotImplementedError


class NoopMetricsCollector(MetricsCollector):
    def observe(self, df: DataFrame) -> DataFrame:
        return df

    def publish(self):
        pass


class SparkMetricsCollector(MetricsCollector):
    def __init__(self, jvm_collector):
        self._jvm_collector = jvm_collector

    def observe(self, df: DataFrame) -> DataFrame:
        new_jdf = self._jvm_collector.observe(df._jdf)
        return DataFrame(new_jdf, df.sql_ctx)

    def publish(self):
        self._jvm_collector.publish()


def create_feature_metrics_collector(spark: SparkSession, params: MaterializationTaskParams) -> MetricsCollector:
    if not params.HasField("data_observability_config"):
        return NoopMetricsCollector()

    config = params.data_observability_config
    if not config.enabled:
        return NoopMetricsCollector()

    jvm_collector = spark._jvm.com.tecton.dataobs.spark.MetricsCollector.fromMaterializationTaskParams(
        params.SerializeToString()
    )
    return SparkMetricsCollector(jvm_collector)
