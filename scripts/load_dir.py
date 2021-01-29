import sys
import requests

from pathlib import Path


def upoad_file(url, filename):
    files = {'file': open(filename, 'rb')}
    r = requests.post(url, files=files)

    print(r.json())


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:\tpython load_dir.py <url> <dir_path>")
        sys.exit()

    host = sys.argv[1]
    dir_path = Path(sys.argv[2])

    for entry in dir_path.iterdir():
        if entry.is_file():
            upoad_file(host, entry)
