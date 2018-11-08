import os
import lzma
import tarfile
import urllib.request


class DataDownloader:

    USERAGENT: str = 'Dostoevsky / 1.0'
    STORAGE_BASE_URL: str = 'https://storage.b-labs.pro/'
    DATA_BASE_PATH: str = os.path.dirname(os.path.abspath(__file__))
    CHUNK_SIZE: int = 1024 * 32

    def download(self, source: str, destination: str) -> int:
        destination_path: str = os.path.join(self.DATA_BASE_PATH, destination)
        url: str = os.path.join(self.STORAGE_BASE_URL, source)
        request = urllib.request.Request(url)
        request.add_header('User-Agent', self.USERAGENT)
        response = urllib.request.urlopen(request)
        with open(destination_path, 'wb') as output:
            filesize: int = 0
            while source:
                chunk = response.read(self.CHUNK_SIZE)
                if not chunk:
                    break
                filesize += len(chunk)
                output.write(chunk)
        # assume that we always distribute data as .tar.xz archives
        with lzma.open(destination_path) as f:
            with tarfile.open(fileobj=f) as tar:
                tar.extractall(os.path.dirname(destination_path))
        # remove original file
        os.remove(destination_path)
        return filesize
