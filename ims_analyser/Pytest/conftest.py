    # conftest.py
import pytest
import logging
logging.basicConfig(
    filename=r"C:\Saroj\Pratice\ims_analyser\Pytest\log\test.log",
    level = logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force= True
)
def pytest_sessionstart(session):
    logging.info("=======Test started==========")

def pytest_runtest_setup(item):
#    print ({item.iter_markers()})
#    print(f"Starting {item.name}")
    for marker in item.iter_markers():
        print(f"Marker : {marker.name}")
@pytest.fixture(scope="session")
def login():
    client ="https://testapi.fr/en/about-us/who-we-are/"
    yield client

    print("\n logout")
def pytest_sessionfinish(session):
    logging.info("=======Test ended=======")