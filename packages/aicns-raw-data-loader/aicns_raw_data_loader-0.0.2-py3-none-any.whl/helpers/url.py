"""
    Helper modules for URL
"""
from abc import ABCMeta, abstractmethod
from pendulum import DateTime


class URL:
    """

    """

    def __init__(self):
        self.scheme = ""
        self.host = ""
        self.port = ""

    def __str__(self):
        return f"{self.scheme}://{self.host}:{self.port}"


class URLBuilder(metaclass=ABCMeta):
    """

    """

    def __init__(self):
        self._url = URL()

    def url(self) -> str:
        return str(self._url)

    @abstractmethod
    def setScheme(self):
        pass

    @abstractmethod
    def setHost(self):
        pass

    @abstractmethod
    def setPort(self):
        pass


class HDFSBuilder(URLBuilder):
    """

    """

    def __init__(self):
        super().__init__()
        self.setScheme()
        self.data_prefix = ""
        self.cluster_path = ""
        self.feature_path = ""
        self.date_path = ""

    def setScheme(self) -> URLBuilder:
        self._url.scheme = "hdfs"
        return self

    def setHost(self, host) -> URLBuilder:
        self._url.host = host
        return self

    def setPort(self, port) -> URLBuilder:
        self._url.port = port
        return self

    def setDataPrefix(self, prefix: str) -> URLBuilder:
        self.data_prefix = prefix
        return self

    def setCluster(self, cluster_id: int) -> URLBuilder:
        self.cluster_path = "/pos_id=" + str(cluster_id)
        return self

    def setFeature(self, feature_id: int) -> URLBuilder:
        self.feature_path = "/ss_id=" + str(feature_id)
        return self

    def setDate(self, date: DateTime) -> URLBuilder:
        self.date_path = f"/year={date.year}/month={date.month:02d}/day={date.day:02d}"
        return self

    def __get_data_path(self):
        return self.data_prefix + self.cluster_path + self.feature_path

    def url(self) -> str:
        return str(self._url) + self.__get_data_path() + self.date_path
