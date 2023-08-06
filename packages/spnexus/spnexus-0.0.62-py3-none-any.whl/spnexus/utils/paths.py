class PathsUtil:

    @staticmethod
    def add_leading_slash(path: str) -> str:
        if path[0] != '/':
            path = f'/{path}'
        return path

    @staticmethod
    def remove_leading_slash(path: str) -> str:
        if path[0] == '/':
            path = path[1:]
        return path

    @staticmethod
    def add_trailing_slash(path: str) -> str:
        if path[-1] != '/':
            path += '/'
        return path

    @staticmethod
    def remove_trailing_slash(path: str) -> str:
        if path[-1] == '/':
            path = path[:-1]
        return path
