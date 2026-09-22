import hashlib


def calculate_file_hash(file_path: str):

    sha256 = hashlib.sha256()

    with open(
        file_path,
        "rb"
    ) as f:

        while True:

            chunk = f.read(
                1024 * 1024
            )

            if not chunk:
                break

            sha256.update(chunk)


    return sha256.hexdigest()