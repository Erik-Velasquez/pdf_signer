import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from app.models.signature import SignatureConfig
from app.services.pdf_signer import sign_pdf

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/sign", summary="Sign a PDF")
async def sign(
    pdf: UploadFile = File(...),
    signature: UploadFile = File(...),
    x: int = Form(...),
    y: int = Form(...),
    width: int = Form(...),
    height: int = Form(...),
    page: int = Form(0),
):
    if pdf.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must be a PDF.",
        )

    if signature.content_type not in (
        "image/png",
        "image/x-png",
    ):
        raise HTTPException(
            status_code=400,
            detail="Signature must be a PNG image.",
        )

    if width <= 0 or height <= 0:
        raise HTTPException(
            status_code=400,
            detail="Width and height must be positive.",
        )

    if page < 0:
        raise HTTPException(
            status_code=400,
            detail="Page number cannot be negative.",
        )

    logger.info("Received signing request: %s", pdf.filename)

    config = SignatureConfig(
        x=x,
        y=y,
        width=width,
        height=height,
        page=page,
    )

    try:
        signed_pdf = sign_pdf(
            await pdf.read(),
            await signature.read(),
            config,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception:
        logger.exception("Signing failed.")

        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        )

    logger.info("PDF signed successfully.")

    return Response(
        content=signed_pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="signed.pdf"',
        },
    )
