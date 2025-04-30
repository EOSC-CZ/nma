import yaml

from common.vocabularies.europa_base import EuropaBaseTypeReader


class EuropaLanguagesTypeReader(EuropaBaseTypeReader):
    def __init__(
        self,
        *,
        source=None,
        base_path=None,
        base_url="http://publications.europa.eu/resource/authority/language",
        languages=["cs", "en"],
        **kwargs,
    ):
        """Constructor.
        :param source: Data source (e.g. filepath, stream, ...)
        """
        super().__init__(
            source=source, base_path=base_path, base_url=base_url, languages=languages
        )


if __name__ == "__main__":
    reader = EuropaLanguagesTypeReader()
    data = []
    for entry in reader:
        data.append(entry.entry)
    with open("fixtures/vocabulary-languages.yaml", "w") as f:
        f.write(yaml.dump_all(data, sort_keys=True, allow_unicode=True))
