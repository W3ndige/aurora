import random
import datasketch

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from aurora.database import Base

engine = create_engine(
    "postgresql://postgres:postgres@postgres:5432/aurora_test"
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def get_test_sample():
    filepath = "tests/testdata/random_262144_deea51994761de54aff0ef112ace7ce41503d8893998817e5801ae21a88cac7c"
    filename = filepath.split("/")[2]
    sha256 = filename.split("_")[2]
    size = int(filename.split("_")[1])

    return (filepath, filename, sha256, size)


def get_random_minhash():
    minhash = datasketch.MinHash()

    random_bytes = random.randbytes(256)
    minhash.update(random_bytes)

    lean_minhash = datasketch.LeanMinHash(minhash)

    return (lean_minhash.seed, lean_minhash.hashvalues.tolist())