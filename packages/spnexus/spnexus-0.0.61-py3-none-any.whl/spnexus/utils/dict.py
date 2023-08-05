from .base import UtilBase


class DictUtil(UtilBase):
    CASE_LOWER: int = 0
    CASE_UPPER: int = 1

    @staticmethod
    def index_fields(fields: list) -> dict:
        index_map: dict = {}

        for i in range(0, len(fields)):
            index_map[fields[i]] = i

        return index_map

    @staticmethod
    def map_fields(field_index: dict, line: list) -> dict:
        field_map: dict = {}

        for key, index in field_index.items():
            if len(line) >= index + 1:
                if isinstance(line[index], str):
                    line[index] = line[index].strip()
                field_map[key] = line[index]

        return field_map

    @staticmethod
    def change_key_case(source: dict, case: int) -> dict:
        target: dict = {}

        for key, value in source.items():
            if case == DictUtil.CASE_LOWER:
                key = str(key).lower()
            if case == DictUtil.CASE_UPPER:
                key = str(key).upper()
            target[key] = value

        return target
