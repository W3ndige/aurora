"""Basic utils for extracting common information from file.

This module exhibits functions for extracting hashes from the file stream.
"""


import os
import magic
import ssdeep
import hashlib

from typing import IO


def get_magic(stream: IO, mimetype: bool = False) -> str:
    """Get magic value from the stream.

    Extracts the magic of the passed stream using `python-magic` module.

    Args:
        stream (IO): File stream.
        mimetype (bool)): Decides if the magic or mimetype is extracted. Defaults to `false`.

    Returns:
        str: Magic value of the passed stream.
    """

    stream.seek(0, os.SEEK_SET)
    return magic.from_buffer(stream.read(), mime=mimetype)


def get_hash(stream: IO, hash_obj, digest_func) -> str:
    """Helper functions for calculating hash_obj digest based on passed parameters.

    Helper function that accepts hash object and digest function to calculate digest value of a stream.

    Args:
        stream (IO): File stream.
        mimetype (bool)): Decides if the magic or mimetype is extracted. Defaults to `false`.

    Returns:
        str: Return value of digest function on the hash object.
    """

    stream.seek(0, os.SEEK_SET)

    for chunk in iter(lambda: stream.read(4096), b""):
        hash_obj.update(chunk)

    return digest_func(hash_obj)


def get_md5(stream: IO) -> str:
    """Calculate MD5 hash of a stream.

    Helper function that calculates the MD5 digest of a stream using `get_hash` helper function.

    Args:
        stream (IO): File stream.

    Returns:
        str: MD5 hash.
    """

    return get_hash(stream, hashlib.md5(), lambda h: h.hexdigest())


def get_sha1(stream: IO) -> str:
    """Calculate SHA1 hash of a stream.

    Helper function that calculates the SHA1 digest of a stream using `get_hash` helper function.

    Args:
        stream (IO): File stream.

    Returns:
        str: SHA1 hash.
    """

    return get_hash(stream, hashlib.sha1(), lambda h: h.hexdigest())


def get_sha256(stream: IO) -> str:
    """Calculate SHA256 hash of a stream.

    Helper function that calculates the SHA256 digest of a stream using `get_hash` helper function.

    Args:
        stream (IO): File stream.

    Returns:
        str: SHA256 hash.
    """

    return get_hash(stream, hashlib.sha256(), lambda h: h.hexdigest())


def get_sha512(stream: IO) -> str:
    """Calculate SHA512 hash of a stream.

    Helper function that calculates the SHA512 digest of a stream using `get_hash` helper function.

    Args:
        stream (IO): File stream.

    Returns:
        str: SHA512 hash.
    """

    return get_hash(stream, hashlib.sha512(), lambda h: h.hexdigest())


def get_ssdeep(stream: IO) -> str:
    """Calculate SSDEEP hash of a stream.

    Helper function that calculates the SSDEEP digest of a stream using `get_hash` helper function.

    Args:
        stream (IO): File stream.

    Returns:
        str: SSDEEP hash.
    """

    return get_hash(stream, ssdeep.Hash(), lambda h: h.digest())
