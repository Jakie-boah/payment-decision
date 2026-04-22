

import pytest



def test_one(logger, config):
    logger.info("test")
    logger.info("test1")
    logger.info("test3")
    logger.info(config)
    assert True