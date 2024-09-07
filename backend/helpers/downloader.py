import uuid
from urllib import request
from helpers import path

CHUNK = 8 * 1024


def download_file(url: str):
    file_path = path.get_temp_path(uuid.uuid4().hex + ".tmp")
    with open(file_path, "wb") as file:
        with request.urlopen(url) as response:
            while True:
                chunk = response.read(CHUNK)
                if not chunk:
                    break
                file.write(chunk)
    return file_path
