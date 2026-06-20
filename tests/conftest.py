from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.api.main import app

TEST_FILES = Path(__file__).parent / "files"


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def sample_pdf() -> Path:
    return TEST_FILES / "sample.pdf"


@pytest.fixture
def signature() -> Path:
    return TEST_FILES / "signature.png"


@pytest.fixture
def sample_pdf_bytes(sample_pdf: Path) -> bytes:
    return sample_pdf.read_bytes()


@pytest.fixture
def signature_bytes(signature: Path) -> bytes:
    return signature.read_bytes()
