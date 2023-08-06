"""
    Util module for features
"""
from typing import List
from feature.feature import Feature
from feature.featureCluster import FeatureCluster
from mongoengine import EmbeddedDocumentField, StringField, FloatField, IntField


def map_cluster_with_belonging_features(
    features: List[Feature], clusters: List[FeatureCluster]
):
    """Relate cluster(1) and features(N)

    :param features:
    :param clusters:
    :return:
    """
    for cluster in clusters:
        cluster_id = cluster.get_cluster_id()
        belonging_features = list(
            filter(lambda feature: feature.is_belonging_cluster(cluster_id), features)
        )
        cluster.link_belonging_features(belonging_features)


def mongo_to_dict(obj, exclude_fields=[]):
    return_data = []
    if obj is None:
        return None
    for field_name in obj._fields:
        if field_name in exclude_fields:
            continue
        if field_name in ("id",):
            continue
        data = obj._data[field_name]
        if data is not None:
            if isinstance(obj._fields[field_name], EmbeddedDocumentField):
                return_data.append((field_name, mongo_to_dict(data, [])))
            else:
                return_data.append(
                    (field_name, mongo_to_python_type(obj._fields[field_name], data))
                )
        else:
            return_data.append((field_name, None))
    return dict(return_data)


def mongo_to_python_type(field, data):
    if isinstance(field, StringField):
        return str(data)
    elif isinstance(field, FloatField):
        return float(data)
    elif isinstance(field, IntField):
        return int(data)
    else:
        return str(data)
