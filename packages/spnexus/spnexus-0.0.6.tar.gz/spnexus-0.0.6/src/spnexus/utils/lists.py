from geopandas import GeoDataFrame
from .base import UtilBase


class ListUtil(UtilBase):

    @staticmethod
    def diff(l1, l2):
        return list((s1 := set(l1)) - (s2 := set(l2))) + list(s2 - s1)

    @staticmethod
    def from_geo_data_frame(frame: GeoDataFrame) -> list or bool:
        if not isinstance(frame, GeoDataFrame):
            return False

        fields = frame.keys()

        if not len(fields):
            return False

        result = []

        for i in range(1, len(frame[fields[0]])):
            row = {}

            for field_name in fields:
                row[field_name] = frame[field_name][i]

            result.append(row)

        return result
