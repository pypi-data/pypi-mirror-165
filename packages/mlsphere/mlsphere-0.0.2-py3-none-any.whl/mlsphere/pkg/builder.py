import os
from typing import Dict

import requests
from loguru import logger
from spython.main import Client


class Builder:
    def __init__(self) -> None:
        self.client = Client

    def build(self, config: Dict) -> None:
        build_folder = os.path.abspath(os.path.dirname(config['recipe']))
        print(build_folder)
        self.client.build(
            recipe=config['recipe'],
            image=config['target'],
            sudo=False,
            build_folder=build_folder,
            options=["--fakeroot"],
        )
        if config['sign']:
            logger.info("Signing image with your pgp key")
        os.system(f"singularity sign {config['target']}")

    def download(self, config: Dict) -> None:
        get_response = requests.get(config['pull'], stream=True)
        file_name = config['pull'].split("/")[-1]
        with open(file_name, 'wb') as f:
            for chunk in get_response.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        # renaming the file_name to config['target']
        os.rename(file_name, config['target'])