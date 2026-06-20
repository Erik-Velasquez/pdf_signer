import pymupdf
import pytest

from app.models.signature import SignatureConfig
from app.services.pdf_signer import sign_pdf


def test_sign_pdf_success(
    sample_pdf_bytes: bytes,
    signature_bytes: bytes,
) -> None:
    config = SignatureConfig(
        x=50,
        y=50,
        width=100,
        height=50,
    )

    result = sign_pdf(
        sample_pdf_bytes,
        signature_bytes,
        config,
    )

    assert result.startswith(b"%PDF")

    with pymupdf.open(
        stream=sample_pdf_bytes,
        filetype="pdf",
    ) as original_doc:
        original_page_count = len(original_doc)
        original_image_count = len(original_doc[config.page].get_images())

    with pymupdf.open(
        stream=result,
        filetype="pdf",
    ) as signed_doc:
        signed_page_count = len(signed_doc)
        signed_image_count = len(signed_doc[config.page].get_images())

    assert signed_page_count == original_page_count
    assert signed_image_count == original_image_count + 1


def test_page_out_of_range(
    sample_pdf_bytes: bytes,
    signature_bytes: bytes,
) -> None:
    with pymupdf.open(
        stream=sample_pdf_bytes,
        filetype="pdf",
    ) as doc:
        invalid_page = len(doc)

    config = SignatureConfig(
        x=50,
        y=50,
        width=100,
        height=50,
        page=invalid_page,
    )

    with pytest.raises(
        ValueError,
        match="does not exist",
    ):
        sign_pdf(
            sample_pdf_bytes,
            signature_bytes,
            config,
        )


def test_signature_exceeds_page_width(
    sample_pdf_bytes: bytes,
    signature_bytes: bytes,
) -> None:
    with pymupdf.open(
        stream=sample_pdf_bytes,
        filetype="pdf",
    ) as doc:
        page_width = doc[0].rect.width

    config = SignatureConfig(
        x=int(page_width) + 1,
        y=50,
        width=100,
        height=50,
    )

    with pytest.raises(
        ValueError,
        match="page width",
    ):
        sign_pdf(
            sample_pdf_bytes,
            signature_bytes,
            config,
        )


def test_signature_exceeds_page_height(
    sample_pdf_bytes: bytes,
    signature_bytes: bytes,
) -> None:
    with pymupdf.open(
        stream=sample_pdf_bytes,
        filetype="pdf",
    ) as doc:
        page_height = doc[0].rect.height

    config = SignatureConfig(
        x=50,
        y=int(page_height) + 1,
        width=100,
        height=50,
    )

    with pytest.raises(
        ValueError,
        match="page height",
    ):
        sign_pdf(
            sample_pdf_bytes,
            signature_bytes,
            config,
        )


def test_invalid_pdf_bytes(
    signature_bytes: bytes,
) -> None:
    config = SignatureConfig(
        x=50,
        y=50,
        width=100,
        height=50,
    )

    with pytest.raises(pymupdf.FileDataError):
        sign_pdf(
            b"not a pdf",
            signature_bytes,
            config,
        )
