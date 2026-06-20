from io import BytesIO
import logging

import fitz

from app.models.signature import SignatureConfig

logger = logging.getLogger(__name__)


def sign_pdf(
    pdf_bytes: bytes,
    signature_bytes: bytes,
    config: SignatureConfig,
) -> bytes:
    """
    Stamps a signature image onto a PDF.

    Parameters
    ----------
    pdf_bytes : bytes
        Original PDF.
    signature_bytes : bytes
        PNG signature image.
    config : SignatureConfig
        Signature placement configuration.

    Returns
    -------
    bytes
        Signed PDF.
    """

    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    if config.page >= len(doc):
        raise ValueError("Page number out of range.")

    page = doc[config.page]

    page_width = page.rect.width
    page_height = page.rect.height

    y = page_height - config.y - config.height

    if config.x + config.width > page_width:
        raise ValueError("Signature exceeds page width.")

    if config.y + config.height > page_height:
        raise ValueError("Signature exceeds page height.")

    if config.x < 0 or config.x + config.width > page_width:
        raise ValueError("Signature exceeds page width.")

    if config.y < 0 or config.y + config.height > page_height:
        raise ValueError("Signature exceeds page height.")

    logger.info(
        "Signing page %d at (%d, %.2f)",
        config.page,
        config.x,
        y,
    )

    rect = fitz.Rect(
        config.x,
        y,
        config.x + config.width,
        y + config.height,
    )

    page.insert_image(
        rect,
        stream=signature_bytes,
        keep_proportion=True,
    )

    output = BytesIO()

    doc.save(output)
    doc.close()

    return output.getvalue()
