import os
from pathlib import Path
from config_probe import probe
import logging
RESOURCES_PATH = os.environ.get("RESOURCES_PATH", Path(__file__).parent.parent / "deploy/config")
ENV = os.environ.get("ENVIRONMENT", "local")


def load(environment):
    config_file = "common.yaml"
    env_config_file = "{}/config.yaml".format(environment)

    logging.info("Loading config {} and {}".format(config_file, env_config_file))

    config = probe(path=str(RESOURCES_PATH), patterns=[config_file, env_config_file])
    config.database.url = f"{config.database.host}:{config.database.port}/{config.database.api_version}"
    config.celery_broker.url = f"{config.celery_broker.host}:{config.celery_broker.port}"
    config.database.url_api_version = f"{config.database.host}:{config.database.port}/{config.database.api_version}"

    return config


config = load(ENV)
