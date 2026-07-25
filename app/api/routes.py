import logging
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response
from pydantic import ValidationError

from app.models.signature import SignatureConfig
from app.services.pdf_signer import sign_pdf

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/sign", summary="Sign a PDF")
async def sign(
    pdf: Annotated[UploadFile, File()],
    signature: Annotated[UploadFile, File()],
    x: Annotated[int, Form()],
    y: Annotated[int, Form()],
    width: Annotated[int, Form()],
    height: Annotated[int, Form()],
    page: Annotated[int, Form()] = 0,
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

    logger.info("Received signing request: %s", pdf.filename)

    try:
        config = SignatureConfig(
            x=x,
            y=y,
            width=width,
            height=height,
            page=page,
        )
        signed_pdf = sign_pdf(
            await pdf.read(),
            await signature.read(),
            config,
        )

    except ValidationError as exc:
        raise HTTPException(
            status_code=422,
            detail=exc.errors(include_url=False),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception("Signing failed.")

        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        ) from exc

    logger.info("PDF signed successfully.")

    return Response(
        content=signed_pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": 'attachment; filename="signed.pdf"',
        },
    )
