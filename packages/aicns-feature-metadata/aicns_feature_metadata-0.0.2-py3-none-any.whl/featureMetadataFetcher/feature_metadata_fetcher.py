"""
    Interface module for feature metadata fetcher
"""

from abc import ABCMeta, abstractmethod
from typing import Tuple, List
from feature.feature import Feature
from feature.featureCluster import FeatureCluster
from utils.feature_util import map_cluster_with_belonging_features


class FeatureMetadataFetcher(metaclass=ABCMeta):
    """
        Interface for feature meatadata fetcher
    """

    def __init__(self, client=None):
        self.client = client

    @abstractmethod
    def get_or_create_conn(self, conn_info):
        """ Get or create whatever whether conn object, such as client and session, is established or not

        :param conn_info:
        :return:
        """
        pass

    @abstractmethod
    def _fetch_features(self) -> List[Feature]:
        pass

    @abstractmethod
    def _fetch_clusters(self) -> List[FeatureCluster]:
        pass

    def fetch_metadata(self) -> Tuple[List[Feature], List[FeatureCluster]]:
        """Template method for tuple consisted of features and feature clusters

        :return:
        """
        features: List[Feature] = self._fetch_features()
        clusters: List[FeatureCluster] = self._fetch_clusters()
        map_cluster_with_belonging_features(features=features, clusters=clusters)
        return features, clusters

    @abstractmethod
    def close_conn(self):
        pass
