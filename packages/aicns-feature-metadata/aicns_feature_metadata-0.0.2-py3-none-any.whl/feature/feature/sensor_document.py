"""
    Sensor document module for MongoDB ORM
"""

from feature.feature import Sensor, Feature
from mongoengine import (
    StringField,
    IntField,
    FloatField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
)


class SensorTypeDocument(EmbeddedDocument):
    type_code = StringField(max_length=16)
    type_name = StringField(max_length=32)
    unit = StringField(max_length=16)
    type_id = IntField()
    type_color_code = StringField(max_length=16)


class SensorPositionDocument(EmbeddedDocument):
    pos_code = StringField(max_length=8)
    pos_dtl = StringField(max_length=32)
    pos_name = StringField(max_length=16)
    pos_id = IntField()


class SensorMeta(type(Sensor), type(Document)):
    """Merged metaclass to avoid metaclass conflict

    """

    pass


class SensorDocument(Document, Sensor, metaclass=SensorMeta):
    """Sensor ORM class.
    Inheritance order is very importance because Python mro
    """

    meta = {"collection": "sensor"}
    ss_id = IntField(required=True, unique=True)

    range_type = IntField()
    rstart = FloatField(required=True)
    rlev1 = FloatField(required=True)
    rlev2 = FloatField(required=True)
    rlev3 = FloatField(required=True)
    rlev4 = FloatField(required=True)
    rlev5 = FloatField()
    rlev6 = FloatField()
    rlev7 = FloatField()
    rlev8 = FloatField()
    rend = FloatField(required=True)
    type = EmbeddedDocumentField(SensorTypeDocument)
    position = EmbeddedDocumentField(SensorPositionDocument)

    def is_belonging_cluster(self, cluster_id: int) -> bool:
        return self.position.pos_id == cluster_id
