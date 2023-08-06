"""

"""
from typing import List
from abc import ABCMeta, abstractmethod
from feature.feature import Feature


class FeatureCluster(metaclass=ABCMeta):
    """Abstract Feature Cluster object represent cluster of features, such as position having many sensor features

    """

    features: List[Feature]

    def link_belonging_features(self, features: List[Feature]):
        self.features = features

    @abstractmethod
    def get_cluster_id(self) -> int:
        pass

    def get_features(self) -> List[Feature]:
        return self.features
