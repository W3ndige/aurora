from fastapi import UploadFile
from karton.core import Config, Producer, Task, Resource

config = Config("karton.ini")
producer = Producer(config)


def push_file(file: UploadFile, sha256: str) -> None:
    file.file.seek(0, 0)

    filename = file.filename
    content = file.file.read()

    resource = Resource(filename, content, sha256=sha256)

    task = Task({"type": "sample", "kind": "raw"})

    task.add_resource("sample", resource)

    producer.send_task(task)
