from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_sign_endpoint():
    with open("tests/files/sample.pdf", "rb") as pdf:
        with open("tests/files/signature.png", "rb") as sig:

            response = client.post(
                "/sign",
                files={
                    "pdf": ("sample.pdf", pdf, "application/pdf"),
                    "signature": ("signature.png", sig, "image/png"),
                },
                data={
                    "x": 100,
                    "y": 100,
                    "width": 120,
                    "height": 50,
                    "page": 0,
                },
            )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 0


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_reject_non_pdf():
    response = client.post(
        "/sign",
        files={
            "pdf": ("file.txt", b"hello", "text/plain"),
            "signature": ("signature.png", b"abc", "image/png"),
        },
        data={
            "x": 100,
            "y": 100,
            "width": 120,
            "height": 50,
            "page": 0,
        },
    )

    assert response.status_code == 400
