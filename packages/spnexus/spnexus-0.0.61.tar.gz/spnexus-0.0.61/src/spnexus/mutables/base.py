from ..base import Base


class MutableBase(Base):
    _data_map: dict

    def __init__(self, **kwargs):
        for attr_name, attr_value in kwargs.items():
            if hasattr(self, attr_name):
                setattr(self, attr_name, attr_value)
        self.spn_load_mutables()

    def spn_hash(self, name: str = None) -> str:
        import hashlib
        hashes = self._hashes if hasattr(self, '_hashes') and isinstance(self._hashes, dict) else {}
        hash_sources = None
        negative_match_mode = False
        
        if name is None and ((is_default := 'default' in hashes) or 'default_no' in hashes):
            hash_sources = hashes['default'] if is_default else hashes['default_no']
            negative_match_mode = not is_default
        elif name is not None:
            if name in hashes:
                hash_sources = hashes[name]
            elif (no_key := name + '_no') in hashes:
                hash_sources = hashes[no_key]
                negative_match_mode = True
        else:
            hash_sources = self.__dict__.keys()

        if isinstance(hash_sources, str):
            hash_sources = str.split(',')

        hash_source = ''
        for field in self.__dict__.keys():
            if negative_match_mode and field in hash_sources:
                continue
            if hasattr(self, field) and (attr := getattr(self, field)) is not None:
                if hasattr(attr, '__call__'):
                    result = str(attr()).strip()
                    if len(result):
                        hash_source += result
                elif len(formatted := str(attr).strip()):
                    hash_source += formatted

        encoded_source = hash_source.encode('utf-8')
        return hashlib.sha256(encoded_source).hexdigest()

    def spn_load_mutables(self):
        import importlib
        if hasattr(self, '_mutables') and isinstance(self._mutables, dict):
            for key, value in self._mutables.items():
                if not hasattr(self, key) or not isinstance((attr := getattr(self, key)), dict):
                    continue

                module_parts = value.split('.')
                cls_name = module_parts[-1]
                module_parts.pop()
                module_ref = '.'.join(module_parts)
                module = importlib.import_module(module_ref)
                cls = getattr(module, cls_name)
                
                if 'object' in attr and attr['object'] == 'list' and 'data' in attr and isinstance(attr['data'], list):
                    mutable = []
                    for data_source in attr['data']:
                        mutable.append(cls.factory(**data_source))
                else:
                    mutable = cls.factory(**attr)

                setattr(self, 'mutable_' + str(key), mutable)

    @classmethod
    def factory(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def get_data_map(cls) -> dict or None:
        return cls._data_map

    @classmethod
    def extract_fields(cls, source: dict) -> dict or bool:
        if not isinstance(source, dict) or not len(source.items()):
            return False

        result: dict = {}

        for key, value in source.items():
            if key not in cls._data_map:
                continue

            result[cls._data_map[key]] = value

        return result
