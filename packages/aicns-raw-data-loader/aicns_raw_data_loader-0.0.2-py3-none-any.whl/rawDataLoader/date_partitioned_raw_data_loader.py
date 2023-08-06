"""

"""

from rawDataLoader import RawDataLoader
from feature.featureCluster import FeatureCluster
from helpers.url import URLBuilder, HDFSBuilder
from pendulum import period, DateTime, Period, now
#import logging
from functools import reduce
from pyspark.sql import DataFrame
from typing import List
from pyspark.sql.types import StructType

#logger = logging.getLogger(__name__)


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

    def load_data(self, start, end, clusters: List[FeatureCluster]):
        """ v1. just date partitioned (neither positions nor sensors) raw data

        :param start:
        :param end:
        :param clusters
        :return:
        """
        _period = period(start, end)

        # load data
        df = self.spark.createDataFrame([], StructType([])) 
        print(f"[{now()}]Data load start")
        for date in _period.range("days"):
            path = self.url_builder.setDate(date).url()
            try:
                date_df = self.spark.read.format("org.apache.spark.sql.json").load(path)
                df = df.unionByName(date_df, allowMissingColumns=True)  # todo : compare with broadcasting small df
                #logger.debug(f"Data path was loaded: {path}")
                print(f"[{now()}]Data path was loaded: {path}")
            except Exception as e:
                #logger.debug(f"Data path does not exists: {path}")
                print(f"Error: {e}")
        df.cache()
        print(f"[{now()}]Data load end")

        # Partition for each sensor, position
        print(f"[{now()}]Data Filtering for each sensors start")
        data = dict()
        for position in clusters:
            data[str(position.pos_id)] = dict()
            pos_data = dict()
            if "ss_id" in df.columns:
                for sensor in position.get_features():
                    ss_df = df.filter(df["ss_id"] == sensor.ss_id)
                    ss_df.cache()
                    if ss_df.count() > 0:
                        pos_data[str(sensor.ss_id)] = ss_df
                        print(f"Sensor [{sensor.ss_id}] was yielded")
            data[str(position.pos_id)] = pos_data
        print(f"[{now()}]Data Filtering end")
        df.unpersist()
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
