#!python
import os
import json
import typer
import shutil
from loguru import logger
from typing import Optional

from mlsphere.pkg.builder import Builder
from mlsphere.pkg.runner import Runner
from mlsphere.pkg.utils import upload

app = typer.Typer()

@app.command()
def build(src_path: Optional[str] = './'):
    """
    Build the image from mlsphere.json
    """
    src_path = os.path.join(src_path, "mlsphere.json")
    logger.info(f"Source Code Path: {src_path}")

    with open(src_path, 'r') as fp:
        config = json.load(fp)

    builder = Builder()
    builder.build(config)


@app.command()
def run(command: str, image_path: str):
    """
    Run a specific command defined in mlsphere.json
    """
    src_path="./"
    if command.strip() == "":
        logger.error("Please provide a command to run")
        return
    logger.info(f"Running command {command}")
    src_path = os.path.join(src_path, "mlsphere.json")
    with open(src_path, 'r') as fp:
        config = json.load(fp)
    runner = Runner()
    runner.run_command(config, command=command, image_path=image_path)


@app.command()
def run_pipeline(image_path: Optional[str] = './'):
    """
    Run the pipeline defined in mlsphere.json
    """
    src_path = os.path.join(".", "mlsphere.json")
    logger.info(f"Source Code Path: {src_path}")
    with open(src_path, 'r') as fp:
        config = json.load(fp)
    runner = Runner()
    runner.run_pipeline(config, image_path=image_path)

@app.command()
def pull(src_path: Optional[str] = './'):
    """
    Pull the image from mlsphere.json
    """
    src_path = os.path.join(src_path, "mlsphere.json")
    logger.info(f"Source Code Path: {src_path}")

    with open(src_path, 'r') as fp:
        config = json.load(fp)

    builder = Builder()
    builder.download(config)

@app.command()
def distribute(command: str):
    """
    Distribute a specific command defined in mlsphere.json to TOMA
    """
    src_path="./"
    if command.strip() == "":
        logger.error("Please provide a command to run")
        return
    logger.info(f"Distributing command {command}")
    src_path = os.path.join(src_path, "mlsphere.json")
    with open(src_path, 'r') as fp:
        config = json.load(fp)
    runner = Runner()
    runner.push_toma(config, command=command)

@app.command()
def upload_results(src_path: Optional[str] = './', bucket: Optional[str] = 'mlsphere', filename: Optional[str] = 'results.json'):
    """
    Pull the image from mlsphere.json
    """
    src_path = os.path.join(src_path, "mlsphere.json")
    logger.info(f"Source Code Path: {src_path}")

    with open(src_path, 'r') as fp:
        config = json.load(fp)
    logger.info(f"Archiving {config['upload']}")
    shutil.make_archive(filename, 'zip', config['upload'])
    logger.info(f"Uploading results to {bucket}")
    upload(filename + ".zip", bucket)
    
if __name__ == "__main__":
    app()
