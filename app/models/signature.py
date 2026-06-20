from pydantic import BaseModel, Field


class SignatureConfig(BaseModel):
    """
    Configuration for placing a signature image on a PDF.
    """

    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)

    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)

    page: int = Field(default=0, ge=0)
