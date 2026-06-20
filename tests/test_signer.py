from app.services.pdf_signer import PDFSigner


def test_pdf_is_signed(sample_pdf, signature):
    signer = PDFSigner()

    result = signer.sign(sample_pdf.read_bytes(), signature.read_bytes())

    assert len(result) > 0
