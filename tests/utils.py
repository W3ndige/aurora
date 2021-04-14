import os
import ssdeep
import hashlib
import datasketch

from typing import Dict, Any


def upload_file(filename: str = None, content: str = None) -> Dict[str, str]:
    if not filename:
        filename = "filename"

    if not content:
        content = "content"

    ssdeep_object = ssdeep.Hash()
    ssdeep_object.update(content.encode("utf-8"))
    ssdeep_hash = ssdeep_object.digest()

    sha256_object = hashlib.sha256()
    sha256_object.update(content.encode("utf-8"))
    sha256 = sha256_object.hexdigest()

    return {
        "filename": filename,
        "content": content,
        "sha256": sha256,
        "ssdeep": ssdeep_hash,
    }


def add_minhash() -> Dict[str, Any]:
    minhash = datasketch.MinHash()

    random_bytes = os.urandom(256)
    minhash.update(random_bytes)

    lean_minhash = datasketch.LeanMinHash(minhash)

    return {"seed": lean_minhash.seed, "hash_values": lean_minhash.hashvalues.tolist()}


def add_string(string: str = None, heuristic: str = None) -> Dict[str, str]:
    if not string:
        string = "string"

    if not heuristic:
        heuristic = "heuristic"

    sha256_object = hashlib.sha256()
    sha256_object.update(string.encode("utf-8"))
    sha256 = sha256_object.hexdigest()

    return {"value": string, "sha256": sha256, "heuristic": heuristic}
