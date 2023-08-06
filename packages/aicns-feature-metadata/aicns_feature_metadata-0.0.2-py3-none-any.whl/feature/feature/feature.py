"""
    Base Interface for feature objects
"""

from abc import ABCMeta, abstractmethod


class Feature(metaclass=ABCMeta):
    """Base Interface for feature objects

    """

    @abstractmethod
    def is_belonging_cluster(self, cluster_id: int) -> bool:
        pass
