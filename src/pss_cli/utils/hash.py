import hashlib


def get_hash(file_name: str) -> str:
    """Return md5 hash of a file"""

    with open(file_name, "rb") as f:
        data = f.read()
        md5 = hashlib.md5(data).hexdigest()

    return md5
