"""
    AICNS Sensor and Position metadata fetcher
"""

from mongoengine import connect, disconnect
from typing import List
from feature.feature import Feature, SensorDocument
from feature.featureCluster import FeatureCluster, PositionDocument
from featureMetadataFetcher import FeatureMetadataFetcher


class SensorMetadataFetcher(FeatureMetadataFetcher):
    """
        Sensor feature metadata fetcher depend on MongoDB metadata store
    """

    def get_or_create_conn(self, conn_info=None):
        """ Get or create whatever whether conn object, such as client and session, is established or not

        :param conn_info:
        :return:
        """
        if self.client is None:
            connect(
                "feature",
                host=conn_info["METADATA_HOST"],
                port=int(conn_info["METADATA_PORT"]),
            )
        self.client = True

    def _fetch_features(self) -> List[Feature]:
        sensors = list(SensorDocument.objects.all())
        return sensors

    def _fetch_clusters(self) -> List[FeatureCluster]:
        positions = list(PositionDocument.objects.all())
        return positions

    def close_conn(self):
        disconnect()
