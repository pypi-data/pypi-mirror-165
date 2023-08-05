from json import JSONEncoder


class MutableJSONEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
