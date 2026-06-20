from pathlib import Path

from fastapi.testclient import TestClient

DEFAULT_FORM = {
    "x": "50",
    "y": "50",
    "width": "100",
    "height": "50",
    "page": "0",
}


def test_sign_pdf_success(
    client: TestClient,
    sample_pdf: Path,
    signature: Path,
) -> None:
    with (
        sample_pdf.open("rb") as pdf_file,
        signature.open("rb") as signature_file,
    ):
        response = client.post(
            "/sign",
            files={
                "pdf": (
                    sample_pdf.name,
                    pdf_file,
                    "application/pdf",
                ),
                "signature": (
                    signature.name,
                    signature_file,
                    "image/png",
                ),
            },
            data=DEFAULT_FORM,
        )

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert (
        response.headers["content-disposition"]
        == 'attachment; filename="signed.pdf"'
    )
    assert response.content.startswith(b"%PDF")


def test_rejects_non_pdf_file(client: TestClient, signature: Path) -> None:
    with signature.open("rb") as signature_file:
        response = client.post(
            "/sign",
            files={
                "pdf": (
                    "document.txt",
                    b"not a pdf",
                    "text/plain",
                ),
                "signature": (
                    signature.name,
                    signature_file,
                    "image/png",
                ),
            },
            data=DEFAULT_FORM,
        )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Uploaded file must be a PDF."
    }


def test_rejects_non_png_signature(client: TestClient, sample_pdf: Path) -> None:
    with sample_pdf.open("rb") as pdf_file:
        response = client.post(
            "/sign",
            files={
                "pdf": (
                    sample_pdf.name,
                    pdf_file,
                    "application/pdf",
                ),
                "signature": (
                    "signature.jpg",
                    b"not a png",
                    "image/jpeg",
                ),
            },
            data=DEFAULT_FORM,
        )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Signature must be a PNG image."
    }


def test_rejects_invalid_dimensions(
    client: TestClient,
    sample_pdf: Path,
    signature: Path,
) -> None:
    with (
        sample_pdf.open("rb") as pdf_file,
        signature.open("rb") as signature_file,
    ):
        response = client.post(
            "/sign",
            files={
                "pdf": (
                    sample_pdf.name,
                    pdf_file,
                    "application/pdf",
                ),
                "signature": (
                    signature.name,
                    signature_file,
                    "image/png",
                ),
            },
            data={
                **DEFAULT_FORM,
                "width": "0",
            },
        )

    assert response.status_code == 422

    detail = response.json()["detail"]

    assert any(
        error["loc"] == ["width"]
        and error["type"] == "greater_than"
        for error in detail
    )


def test_rejects_page_out_of_range(
    client: TestClient,
    sample_pdf: Path,
    signature: Path,
) -> None:
    with (
        sample_pdf.open("rb") as pdf_file,
        signature.open("rb") as signature_file,
    ):
        response = client.post(
            "/sign",
            files={
                "pdf": (
                    sample_pdf.name,
                    pdf_file,
                    "application/pdf",
                ),
                "signature": (
                    signature.name,
                    signature_file,
                    "image/png",
                ),
            },
            data={
                **DEFAULT_FORM,
                "page": "999",
            },
        )

    assert response.status_code == 400
    assert "does not exist" in response.json()["detail"]
