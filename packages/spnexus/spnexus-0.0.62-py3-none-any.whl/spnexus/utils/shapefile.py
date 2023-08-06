from .base import UtilBase


class ShapefileUtil(UtilBase):
    ERR_PATH_NOT_STRING: int = 1
    ERR_PATH_NOT_FOUND: int = 2
    ERR_PATH_NOT_READABLE: int = 3
    ERR_PATH_EMPTY: int = 4

    @staticmethod
    def load_directory(path: str) -> dict or int:
        import geopandas
        import os
        result: dict = {}

        if not isinstance(path, str):
            return ShapefileUtil.ERR_PATH_NOT_STRING

        if path[-1] != '/':
            path += '/'

        if not os.path.exists(path):
            return ShapefileUtil.ERR_PATH_NOT_FOUND

        if not os.access(path, os.R_OK):
            return ShapefileUtil.ERR_PATH_NOT_READABLE

        nodes = os.listdir(path)

        if not len(nodes):
            return ShapefileUtil.ERR_PATH_EMPTY

        for node in nodes:
            if not os.path.isfile(node_path := f'{path}{node}'):
                continue

            name_parts = node.split('.')
            extension = str(name_parts[-1])
            name_parts.pop()
            index_name = '.'.join(name_parts)

            if extension.lower() == 'zip':
                result[index_name] = geopandas.read_file(node_path)

        return result
