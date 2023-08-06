import os
from typing import Dict
from loguru import logger
import requests
from spython.main import Client

class Runner:
    def __init__(self):
        self.client = Client
        self.apps = None

    def run_command(self, config: Dict, command: str, image_path=None):
        build_folder = os.path.abspath(os.path.dirname(config['recipe']))
        print(os.path.join(build_folder, config['target']))
        bind = []
        for key, value in config['bind'].items():
            src_dir = os.path.join(build_folder, key)
            bind.append(f"{src_dir}:{value}")
        if image_path is None:
            self.client.load(os.path.join(build_folder, config['target']))
        else:
            self.client.load(os.path.join(image_path, config['target']))
            
        for line in self.client.execute(
            config['scripts'][command].split(" "),
            bind=bind,
            options=['--pwd', '/app'],
            stream=True,
        ):
            print(line, end='')

    def push_toma(self, config, command: str) -> str:
        logger.info("Pushing image to Toma Job Queue")
        res = requests.post("http://planetd.shift.ml/jobs", json={
            "type": "general",
            "payload": {
                "config": config,
                "command": command,
            },
            "returned_payload": {},
            "status": "finished",
            "source": "dataperf",
            "processed_by":"",
        })
        print(res.text)