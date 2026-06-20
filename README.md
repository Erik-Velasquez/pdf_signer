# PDF Signer

A lightweight REST API for stamping transparent PNG signatures onto PDF documents.

Built with **FastAPI** and **PyMuPDF**, the service is designed to run locally with Docker or be deployed to **Google Cloud Run**. It integrates easily with **Google Apps Script** or any client capable of sending `multipart/form-data` requests.

---

## Features

- Stamp transparent PNG signatures onto PDF documents
- Adjustable signature position and size
- Sign any page in a PDF
- Automatic request validation with Pydantic
- REST API built with FastAPI
- Fast PDF processing with PyMuPDF
- Docker support
- Google Cloud Run ready
- Compatible with Google Apps Script

---

## Project Structure

```text
.
├── app
│   ├── api          # FastAPI routes
│   ├── core         # Configuration
│   ├── models       # Pydantic models
│   └── services     # PDF signing logic
├── tests            # API and service tests
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.12+
- pip

---

## Installation

Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Running Locally

Start the development server:

```bash
uvicorn app.api.main:app --reload
```

The application will be available at:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Docker

Build the image:

```bash
docker build -t pdf-signer .
```

Run the container:

```bash
docker run -p 8080:8080 pdf-signer
```

The API will be available at:

```
http://localhost:8080
```

---

# API

## POST /sign

Uploads a PDF and a transparent PNG signature and returns the signed PDF.

Coordinates are measured in **PDF points** (`72 points = 1 inch`).

- `x` → distance from the left edge
- `y` → distance from the bottom edge

### Form Fields

| Field | Type | Description |
|-------|------|-------------|
| pdf | File | PDF document |
| signature | File | PNG signature (transparent background recommended) |
| x | Integer | Distance from the left edge (points) |
| y | Integer | Distance from the bottom edge (points) |
| width | Integer | Signature width (points) |
| height | Integer | Signature height (points) |
| page | Integer | Zero-based page index |

### Response

Returns the signed PDF.

```
Content-Type: application/pdf
```

---

## Example Request

```bash
curl -X POST http://localhost:8000/sign \
  -F "pdf=@sample.pdf" \
  -F "signature=@signature.png" \
  -F "x=100" \
  -F "y=100" \
  -F "width=120" \
  -F "height=50" \
  -F "page=0" \
  --output signed.pdf
```

---

## Validation

Incoming requests are validated before the PDF is processed.

Validation includes:

- Uploaded file is a PDF
- Signature is a PNG image
- Non-negative coordinates
- Positive signature dimensions
- Valid page index

---

## Health Endpoints

### GET /

Returns basic service information.

Example:

```json
{
  "service": "PDF Signer",
  "version": "1.0.0",
  "docs": "/docs"
}
```

---

### GET /health

Returns the application health status.

Example:

```json
{
  "status": "healthy"
}
```
---

## Testing

Run the complete test suite:

```bash
pytest
```

The tests cover:

- API endpoints
- Request validation
- PDF signing logic
- Error handling

---

## Google Apps Script

This API is compatible with `UrlFetchApp.fetch()` using `multipart/form-data`.

Example payload:

```javascript
const response = UrlFetchApp.fetch(API_URL, {
  method: "post",
  payload: {
    pdf: pdfBlob,
    signature: signatureBlob,
    x: 100,
    y: 100,
    width: 120,
    height: 50,
    page: 0,
  },
});
```

---

## Tech Stack

- FastAPI
- Pydantic
- PyMuPDF
- Pytest
- Docker

---

## License

This project is licensed under the MIT License.
