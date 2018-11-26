import os
import sys
import typing

from dostoevsky.data import DataDownloader, DATA_BASE_PATH, AVAILABLE_FILES


if __name__ == '__main__':
    command: str = sys.argv[1]
    arguments: typing.List[str] = sys.argv[2:]
    if command == 'download':
        downloader = DataDownloader()
        for filename in arguments:
            if filename not in AVAILABLE_FILES:
                raise ValueError(f'Unknown package: {filename}')
            source, destination = AVAILABLE_FILES[filename]
            destination_path: str = os.path.join(DATA_BASE_PATH, destination)
            if os.path.exists(destination_path):
                continue
            downloader.download(source=source, destination=destination)
    else:
        raise ValueError('Unknown command')
