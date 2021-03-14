import os
import magic
import ssdeep
import hashlib

from typing import IO


def get_magic(stream: IO, mimetype: bool = False) -> str:
    stream.seek(0, os.SEEK_SET)
    return magic.from_buffer(stream.read(), mime=mimetype)


def get_hash(stream: IO, hash_obj, digest_func) -> str:
    stream.seek(0, os.SEEK_SET)

    for chunk in iter(lambda: stream.read(4096), b""):
        hash_obj.update(chunk)

    return digest_func(hash_obj)


def get_md5(stream: IO) -> str:
    return get_hash(stream, hashlib.md5(), lambda h: h.hexdigest())


def get_sha1(stream: IO) -> str:
    return get_hash(stream, hashlib.sha1(), lambda h: h.hexdigest())


def get_sha256(stream: IO) -> str:
    return get_hash(stream, hashlib.sha256(), lambda h: h.hexdigest())


def get_sha512(stream: IO) -> str:
    return get_hash(stream, hashlib.sha512(), lambda h: h.hexdigest())


def get_ssdeep(stream: IO) -> str:
    return get_hash(stream, ssdeep.Hash(), lambda h: h.digest())
