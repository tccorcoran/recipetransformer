import pytest
import pathlib


@pytest.fixture()
def resources_dir():
    return pathlib.Path(__file__).parent / "resources"
