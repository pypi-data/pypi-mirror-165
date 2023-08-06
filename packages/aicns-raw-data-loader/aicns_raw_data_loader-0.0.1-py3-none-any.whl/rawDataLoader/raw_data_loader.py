"""
    Interface module for raw data loader that fetch speci
"""

from abc import ABCMeta, abstractmethod
from feature.featureCluster import FeatureCluster


class RawDataLoader(metaclass=ABCMeta):
    """

    """

    @abstractmethod
    def prepare_to_load(self, **conn):
        pass

    @abstractmethod
    def load_data_in_a_cluster(self, start, end, cluster: FeatureCluster):
        pass
