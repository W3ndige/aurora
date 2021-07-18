from enum import Enum
from functools import partial
from typing import Tuple, Optional, List

from aurora.database import queries, models


class SampleSearch(partial, Enum):
    MD5 = partial(queries.sample.get_sample_by_md5)
    SHA1 = partial(queries.sample.get_sample_by_sha1)
    SHA256 = partial(queries.sample.get_sample_by_sha256)
    SHA512 = partial(queries.sample.get_sample_by_sha512)
    SSDEEP = partial(queries.sample.get_samples_by_ssdeep)
    STRING = partial(queries.sample.get_samples_with_string)

    def __call__(self, *args, **kwargs):
        return self.value(args[0], args[1])


class StringSearch(partial, Enum):
    SHA256 = partial(queries.string.get_string_by_sha256)
    VALUE = partial(queries.string.get_string_by_value)

    def __call__(self, *args, **kwargs):
        return self.value(args[0], args[1])


def prepare_search(query: str) -> Tuple[str, str]:
    query = query.replace(" ", "")
    try:
        prefix, term = query.split(":", 1)
        prefix = prefix.lower()
    except ValueError:
        prefix, term = (None, None)

    return prefix, term


def sample_search(db, attribute: str, term: str) -> Optional[str]:
    samples = []

    # SsDeep hashes are case sensitive
    if attribute not in ["string", "ssdeep"]:
        term = term.lower()

    if attribute == "md5":
        samples.append(SampleSearch.MD5(db, term))
    elif attribute == "sha1":
        samples.append(SampleSearch.SHA1(db, term))
    elif attribute == "sha256":
        samples.append(SampleSearch.SHA256(db, term))
    elif attribute == "sha512":
        samples.append(SampleSearch.SHA512(db, term))
    elif attribute == "ssdeep":
        samples = SampleSearch.SSDEEP(db, term)
    elif attribute == "string":
        samples = SampleSearch.STRING(db, term)

    return samples


def string_search(db, attribute: str, term: str) -> List[models.String]:
    strings = []
    if attribute == "sha256":
        term = term.lower()
        strings.append(StringSearch.SHA256(db, term))
    elif attribute == "value":
        strings.append(StringSearch.VALUE(db, term))

    return strings
