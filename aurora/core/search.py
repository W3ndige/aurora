from enum import Enum
from functools import partial
from typing import Tuple, Optional

from aurora.database import queries


class SampleSearch(partial, Enum):
    MD5 = partial(queries.sample.get_sample_by_md5)
    SHA1 = partial(queries.sample.get_sample_by_sha1)
    SHA256 = partial(queries.sample.get_sample_by_sha256)
    SHA512 = partial(queries.sample.get_sample_by_sha512)

    def __call__(self, *args, **kwargs):
        return self.value(args[0], args[1])


class StringSearch(partial, Enum):
    SHA256 = partial(queries.string.get_string_by_sha256)
    VALUE = partial(queries.string.get_string_by_value)

    def __call__(self, *args, **kwargs):
        return self.value(args[0], args[1])


def prepare_search(query: str) -> Tuple[str, str]:
    query = query.replace(" ", "")
    prefix, term = query.split(":", 1)
    prefix = prefix.lower()

    return prefix, term


def sample_search(db, attribute: str, term: str) -> Optional[str]:
    sample = None
    term = term.lower()
    if attribute == "md5":
        sample = SampleSearch.MD5(db, term)
    elif attribute == "sha1":
        sample = SampleSearch.SHA1(db, term)
    elif attribute == "sha256":
        sample = SampleSearch.SHA256(db, term)
    elif attribute == "sha512":
        sample = SampleSearch.SHA512(db, term)

    return sample


def string_search(db, attribute: str, term: str) -> Optional[str]:
    string = None
    if attribute == "sha256":
        term = term.lower()
        string = StringSearch.SHA256(db, term)
    elif attribute == "value":
        string = StringSearch.VALUE(db, term)

    return string
