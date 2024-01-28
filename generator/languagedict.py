import yaml

LANGUAGES = ['finnish', 'english']

class LanguageDict(dict):
    def __init__(self, language: str):
        self._supported_languages = LANGUAGES
        if language not in self._supported_languages:
            raise RuntimeError(f"Language '{language}' is not supported. Supported languages are: {self._supported_languages}")

        self._language = language
        super().__init__()

    def __getitem__(self, key):
        if dict.__contains__(self, key):
            item = dict.__getitem__(self, key)
            if isinstance(item, dict) and list(item.keys()) == self._supported_languages:
                return dict.__getitem__(self, key)[self._language]
            else:
                return dict.__getitem__(self, key)

        elif dict.__contains__(self, self._language) and dict.__contains__(self[self._language], key):
            return self[self._language][key]

        else:
            raise KeyError('not found yo')

    def __str__(self):
        if list(self.keys()) == self._supported_languages:
            return str(dict.__getitem__(self, self._language))

        return dict.__str__(self)


class LanguageDictLoader(yaml.FullLoader):
    def __init__(self, language: str, stream):
        self._language = language
        super().__init__(stream)

    def construct_yaml_map(self, node):
        data = LanguageDict(self._language)
        yield data
        value = self.construct_mapping(node)
        data.update(value)

LanguageDictLoader.add_constructor(
    'tag:yaml.org,2002:map',
    LanguageDictLoader.construct_yaml_map
)

def makeLanguageDictLoader(language: str):
    return lambda stream : LanguageDictLoader(language, stream)

def get_supported_languages():
    return LANGUAGES

__all__ = [LanguageDict, makeLanguageDictLoader, get_supported_languages()]
