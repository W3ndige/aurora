import requests
import datasketch

from typing import Dict, List
from karton.core import Karton, Task, Config

def post_minhash_to_sample(url: str, sha256: str, minhash_input=Dict) -> Dict:
    r = requests.post(f"{url}/sample/{sha256}/minhash", json=minhash_input)

    return r.json()

def extract_ngrams(data: List[any], n: int = 4):
    output = []

    for i in range(len(data) - n - 1):
        output.append(" ".join(data[i:i+n]))

    return output

class AuroraConfig(Config):
    def __init__(self, path=None) -> None:
        super().__init__(path)
        self.aurora_config = dict(self.config.items("aurora"))


class Minhash(Karton):
    identity = "kartons.minhash"
    filters = [{"type": "feature"}]


    def process(self, task: Task) -> None:
        data = None
        minhash_type = None
        sha256 = task.get_payload("sha256")
        if task.headers["kind"] == "strings":
            data = task.get_payload("strings")
            minhash_type = "STRINGS_MINHASH"

        if task.headers["kind"] == "disasm":
            data = task.get_payload("opcodes")
            data = extract_ngrams(data)
            minhash_type = "DISASM_MINHASH"

        if data:
            lean_minhash = self.process_minhash(data)
            minhash_input = {
                "seed": lean_minhash.seed,
                "hash_values": lean_minhash.hashvalues.tolist(),
                "minhash_type": minhash_type,
            }

            post_minhash_to_sample(self.config.aurora_config["url"], task.get_payload("sha256"), minhash_input)

            task = Task({"type": "feature", "kind": "minhash"})

            task.add_payload("sha256", sha256)
            task.add_payload("seed", lean_minhash.seed)
            task.add_payload("hash_values",  lean_minhash.hashvalues.tolist())
            task.add_payload("minhash_type", minhash_type)

            self.send_task(task)

    def process_minhash(self, data: List[str]) -> None:
        minhash = datasketch.MinHash(num_perm=256)
        for value in data:
            minhash.update(value.encode("utf-8"))

        return datasketch.LeanMinHash(minhash)
