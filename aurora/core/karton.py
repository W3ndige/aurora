from typing import List
from fastapi import UploadFile
from karton.core import Config, Producer, Task, Resource

config = Config("karton.ini")
producer = Producer(config)


def push_file(file: UploadFile, mime: str, sha256: str) -> None:
    file.file.seek(0, 0)

    filename = file.filename
    content = file.file.read()

    resource = Resource(filename, content, sha256=sha256)

    task = Task({"type": "sample", "kind": mime})

    task.add_payload("sample", resource)

    producer.send_task(task)


def push_minhash(sha256: str, seed: int, hash_values: List, minhash_type: str) -> None:
    task = Task({"type": "feature", "kind": "minhash"})

    task.add_payload("sha256", sha256)
    task.add_payload("seed", seed)
    task.add_payload("hash_values", hash_values)
    task.add_payload("minhash_type", minhash_type)

    producer.send_task(task)


def push_ssdeep(sha256: str, chunksize: int, ssdeep: List) -> None:
    task = Task({"type": "feature", "kind": "ssdeep"})

    task.add_payload("sha256", sha256)
    task.add_payload("chunksize", chunksize)
    task.add_payload("ssdeep", ssdeep)

    producer.send_task(task)
