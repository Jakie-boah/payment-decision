


import pytest
from src.infrastructure.config.config_loader import load_config_from_env
from src.infrastructure.config.config_storage import Config


@pytest.fixture(scope="session")
def config(logger) -> Config:
    config = load_config_from_env()
    logger.info(config)
    return config
