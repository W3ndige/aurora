import subprocess

from typing import List
from karton.core import Karton, Task


def extract_strings(path: str, encoding: str = "s", n: int = 4) -> List:
    if encoding not in "sSbBlL":
        return []

    encoding_arg = "-e" + encoding
    minumum_size_arg = "-n" + str(n)

    strings_process = subprocess.run(
        ["strings", encoding_arg, minumum_size_arg, path], stdout=subprocess.PIPE
    )

    strings = strings_process.stdout.decode("utf-8").split("\n")

    return strings


class Strings(Karton):
    identity = "kartons.strings"
    filters = [{"type": "sample"}]

    def process(self, task: Task) -> None:
        sample = task.get_resource("sample")

        with sample.download_temporary_file() as sample_file:
            path = sample_file.name

            ascii_strings = extract_strings(path)
            wide_strings = extract_strings(path, encoding="l")

            task = Task(
                {
                    "type": "feature",
                    "kind": "strings",
                }
            )

            strings = ascii_strings + wide_strings

            task.add_payload("strings", strings)
            task.add_payload("sha256", sample.sha256)

            self.send_task(task)
