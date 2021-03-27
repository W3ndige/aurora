import re
import requests
import hashlib

from typing import Dict
from karton.core import Karton, Task, Config


SUS_KEYWORDS = [
    r".*pdb$",
    r"(Mozilla)\/[0-9]\.[0.9].*",
    r"http://.*",

]

class AuroraConfig(Config):
    def __init__(self, path=None) -> None:
        super().__init__(path)
        self.aurora_config = dict(self.config.items("aurora"))


def post_string_to_sample(url: str, sha256: str, string_input=Dict) -> Dict:
    r = requests.post(f"{url}/sample/{sha256}/string", json=string_input)

    return r.json()

class SusStrings(Karton):
    identity = "kartons.susstrings"
    filters = [{"type": "feature", "kind": "strings"}]


    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.compiled_keywords = [
            re.compile(x) for x in SUS_KEYWORDS
        ]

    def process(self, task: Task) -> None:
        strings = task.get_payload("strings")

        sha256 = task.get_payload("sha256")

        sus_strings = []
        for string in strings:
            for keyword in self.compiled_keywords:
                if re.match(keyword, string):
                    string_hash = hashlib.sha256(bytes(string, encoding="UTF-8")).hexdigest()
                    sus_strings.append(string)

                    post_string_to_sample(self.config.aurora_config["url"], sha256, {"value": string, "sha256": string_hash})
