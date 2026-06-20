import pytest
from pathlib import Path


@pytest.fixture
def sample_pdf():
    return Path("tests/files/sample.pdf")


@pytest.fixture
def signature():
    return Path("tests/files/signature.png")
