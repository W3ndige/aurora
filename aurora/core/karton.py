"""Helper functions to interact with Karton pipeline.

This module exhibits helper functions that allows to interact with the Karton pipeline,
pushing elements for further analysis..


Attributes:
    config: (Config): Karton config.
    producer (Producer): Karton producer used to send tasks to the pipeline.
"""

import os

from typing import List
from fastapi import UploadFile
from karton.core import Config, Producer, Task, Resource

directory = os.path.dirname(__file__)
os.path.join(directory, "logger.conf")

config = Config(os.path.join(directory, "../../karton.ini"))
producer = Producer(config)


def push_file(file: UploadFile, magic: str, sha256: str) -> None:
    """Push file to the Karton pipeline.

    Creates a Karton task with the content of passed file as a Resource. Sends that task using Producer.

    Args:
        file (UploadFile): File to be uploaded to pipeline.
        magic (str): Magic value of the passed file, used to assign task to different kartons.
        sha256 (str): SHA256 hash of the passed file.

    Returns:
        None
    """

    file.file.seek(0, 0)

    filename = file.filename
    content = file.file.read()

    resource = Resource(filename, content, sha256=sha256)

    task = Task({"type": "sample", "kind": "raw"})

    task.add_payload("sample", resource)
    task.add_payload("magic", magic)

    producer.send_task(task)


def push_minhash(
    sha256: str, seed: int, hash_values: List[int], minhash_type: str
) -> None:
    """Push minhash to the Karton pipeline.

    Creates a Karton task with the minhash contents as payload values.

    Args:
        sha256 (str): SHA256 hash of the owner sample.
        seed (int): Minhash seed.
        hash_values (List(int)): List of hash values of the minhash.
        minhash_type (str): Type of minhash.

    Returns:
        None

    """

    task = Task(
        {
            "type": "feature",
            "stage": "minhash",
            "kind": minhash_type
        }
    )

    task.add_payload("sha256", sha256)
    task.add_payload("seed", seed)
    task.add_payload("hash_values", hash_values)
    task.add_payload("reanalyze", reanalyze)

    producer.send_task(task)


def push_ssdeep(sha256: str, chunksize: int, ssdeep: str) -> None:
    """Push ssdeep to the Karton pipeline.

    Creates a Karton task with the ssdeep contents as payload values.

    Args:
        sha256 (str): SHA256 hash of the owner sample.
        chunksize (int): Chunksize part of the ssdeep hash.
        ssdeep (List(int)): Whole ssdeep hash.

    Returns:
        None

    """

    task = Task({"type": "feature", "stage": "ssdeep"})

    task.add_payload("sha256", sha256)
    task.add_payload("chunksize", chunksize)
    task.add_payload("ssdeep", ssdeep)

    producer.send_task(task)
