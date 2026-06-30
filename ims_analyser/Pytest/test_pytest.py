import logging

logging.basicConfig(
    filename="C:/Saroj/Pratice/ims_analyser/Pytestexecution.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()

def test_login():

    logger.info("Launching browser")

    logger.info("Entering credentials")

    logger.info("Clicking login button")

    assert True

    logger.info("Login successful")
    
