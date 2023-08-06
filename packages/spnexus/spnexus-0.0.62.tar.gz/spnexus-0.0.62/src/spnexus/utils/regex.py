from re import Match
from .base import UtilBase


class RegexUtil(UtilBase):

    @staticmethod
    def map_match_groups(match: Match, fields: list) -> dict or bool:
        if len(fields) != len(match.groups()):
            return False

        group_map = {}
        index = 1
        for field_name in fields:
            group_map[field_name] = match.group(index)
            index += 1

        return group_map
