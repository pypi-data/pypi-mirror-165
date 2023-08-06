import os
from typing import Dict

from spython.main import Client


class Runner:
    def __init__(self):
        self.client = Client
        self.apps = None

    def run_command(self, config: Dict, command: str):
        build_folder = os.path.abspath(os.path.dirname(config['recipe']))
        print(os.path.join(build_folder, config['target']))
        bind = []
        for key, value in config['bind'].items():
            src_dir = os.path.join(build_folder, key)
            bind.append(f"{src_dir}:{value}")
        
        self.client.load(os.path.join(build_folder, config['target']))

        for line in self.client.execute(
            config['scripts'][command].split(" "),
            bind=bind,
            options=['--pwd', '/app'],
            stream=True,
        ):
            print(line, end='')