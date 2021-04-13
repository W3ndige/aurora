import hashlib
from typing import Dict

def upload_file(filename: str = None, content: str = None) -> Dict[str, str]:
    if not filename:
        filename = "filename"

    if not content:
        content = "content"

    sha256_object = hashlib.sha256()
    sha256_object.update(content.encode("utf-8"))
    sha256 = sha256_object.hexdigest()

    return {
        "filename": filename,
        "content": content,
        "sha256": sha256
    }


