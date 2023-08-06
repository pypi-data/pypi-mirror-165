"""

"""

from rawDataLoader import RawDataLoader
from feature.featureCluster import FeatureCluster
from helpers.url import URLBuilder, HDFSBuilder
from pendulum import period, DateTime, Period
import logging
from functools import reduce
from pyspark.sql import DataFrame

logger = logging.getLogger(__name__)


class DatePartitionedRawDataLoader(RawDataLoader):
    """

    """

    def __init__(self):
        self.url_builder: HDFSBuilder = None
        self.spark = None

    def prepare_to_load(self, **conn):
        self.__generate_url_builder(conn)
        self.url_builder
        self.spark = conn["sql_context"]

    def load_data_in_a_cluster(self, start, end, cluster: FeatureCluster):
        """ v1. just date partitioned (neither positions nor sensors) raw data

        :param start:
        :param end:
        :param cluster:
        :return:
        """
        position_id = cluster.pos_id
        # self.url_builder.setCluster(position_id)
        _period = period(start, end)
        data = dict()

        # load data
        dfs = []
        for date in _period.range("days"):
            path = self.url_builder.setDate(date).url()
            try:
                df = self.spark.read.format("org.apache.spark.sql.json").load(path)
                dfs.append(df)
                logger.debug(f"Data path was loaded: {path}")
            except Exception as e:
                logger.debug(f"Data path does not exists: {path}")
        if len(dfs) > 0:
            ss_df = reduce(DataFrame.unionAll, dfs)
        else:
            return data

        # Partition for each sensor belonging
        for sensor in cluster.get_features():
            df = ss_df.filter(ss_df["ss_id"] == sensor.ss_id).sort("event_time")
            if df.count() > 0:
                data[str(sensor.ss_id)] = df
        return data

    def __generate_url_builder(self, conn_conf):
        self.url_builder = (
            HDFSBuilder()
            .setHost(conn_conf["SOURCE_HOST"])
            .setPort(conn_conf["SOURCE_PORT"])
            .setDataPrefix(conn_conf["SOURCE_DATA_PATH_PREFIX"])
        )

    def __set_date_in_url(self, date: DateTime):
        self.url_builder.setDate(date)
