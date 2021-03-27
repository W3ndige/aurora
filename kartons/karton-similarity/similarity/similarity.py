import ssdeep
import requests
import datasketch

from typing import Dict, Optional, List
from karton.core import Karton, Task, Config


def get_minhash_types(url: str) -> List[str]:
    r =  requests.get(f"{url}/minhash/types")
    return r.json()


def get_minhashes(url: str, type: Optional[str] = None) -> Dict:
    if type:
        r = requests.get(f"{url}/minhash/?minhash_type={type}")
    else:
        r = requests.get(f"{url}/minhash/")

    return r.json()


def get_ssdeep_hashes(url: str, chunksize: int) -> Dict:
    r = requests.get(f"{url}/ssdeep/?chunksize={chunksize}")

    return r.json()


def get_sample_minhash(url: str, sha256: str, minhash_type: str) -> Dict:
    r = requests.get(f"{url}/sample/{sha256}/minhash?minhash_type={minhash_type}")
    return r.json()


def post_relation(
    url: str, this_sha256: str, other_sha256: str, type: str, confidence: str
) -> Dict:
    r = requests.post(
        f"{url}/relation/",
        json={
            "parent_sha256": this_sha256,
            "child_sha256": other_sha256,
            "type": type,
            "confidence": confidence,
        },
    )

    return r.json()

class AuroraConfig(Config):
    def __init__(self, path=None) -> None:
        super().__init__(path)
        self.aurora_config = dict(self.config.items("aurora"))


class Similarity(Karton):
    identity = "kartons.similarity"
    filters = [{"type": "feature"}]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        minhash_types = get_minhash_types(self.config.aurora_config["url"])
        self.minhash_lsh_dict = dict.fromkeys(minhash_types, None)
        for minhash_type in minhash_types:
            self.minhash_lsh_dict[minhash_type] = datasketch.MinHashLSH(
                threshold=0.5,
                num_perm=256,
                storage_config={
                    "type": "redis",
                    "basename": minhash_type.encode('UTF-8'),
                    "redis": {"host": "redis", "port": 6379}
                }
            )

    def process(self, task: Task) -> None:
        if task.headers["kind"] == "minhash":
            self.process_minhash(task)
        elif task.headers["kind"] == "ssdeep":
            self.process_ssdeep(task)

    def process_minhash(self, task: Task) -> None:
        sha256 = task.get_payload("sha256")
        seed = task.get_payload("seed")
        hash_values = task.get_payload("hash_values")
        minhash_type = task.get_payload("minhash_type")

        minhash = datasketch.LeanMinHash(seed=seed, hashvalues=hash_values)

        try:
            self.minhash_lsh_dict[minhash_type].insert(sha256, minhash)
        except ValueError as e:
            self.logger.warning(f"Could not insert Minhash to LSH: {e}")

        lsh_sha256_list = self.minhash_lsh_dict[minhash_type].query(
            minhash
        )

        for sample_sha256 in lsh_sha256_list:

            if sample_sha256 == sha256:
                continue

            db_minhash = get_sample_minhash(self.config.aurora_config["url"], sample_sha256, minhash_type)[0]

            db_lean_minhash = datasketch.LeanMinHash(
                seed=db_minhash["seed"], hashvalues=db_minhash["hash_values"]
            )

            jaccard_coefficient = minhash.jaccard(db_lean_minhash)
            if jaccard_coefficient > 0.5:
                post_relation(
                    self.config.aurora_config["url"], sha256, db_minhash["sample"]["sha256"], minhash_type, jaccard_coefficient
                )

    def process_ssdeep(self, task: Task) -> None:
        sha256 = task.get_payload("sha256")
        chunksize = task.get_payload("chunksize")
        ssdeep_hash = task.get_payload("ssdeep")

        ssdeep_data_list = get_ssdeep_hashes(self.config.aurora_config["url"], chunksize)

        for ssdeep_data in ssdeep_data_list:
            if ssdeep_data["sample"]["sha256"] == sha256:
                continue

            ssdeep_coefficient = (
                ssdeep.compare(ssdeep_hash, ssdeep_data["ssdeep"]) / 100.0
            )

            if ssdeep_coefficient > 0.5:
                post_relation(self.config.aurora_config["url"], sha256, ssdeep_data["sample"]["sha256"], "SSDEEP", ssdeep_coefficient)
