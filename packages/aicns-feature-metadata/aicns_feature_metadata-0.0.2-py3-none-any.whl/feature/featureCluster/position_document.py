"""
    Position document module for MongoDB ORM
"""

from feature.featureCluster import Position
from mongoengine import StringField, IntField, Document


class PositionMeta(type(Position), type(Document)):
    """Merged metaclass to avoid metaclass conflict

    """

    pass


class PositionDocument(Document, Position, metaclass=PositionMeta):
    meta = {"collection": "position"}
    pos_id = IntField(required=True, unique=True)

    pos_code = StringField(max_length=16)
    pos_dtl = StringField(max_length=32)
    pos_name = StringField(max_length=16)

    def get_cluster_id(self) -> int:
        return self.pos_id
