# PDF Signer

A lightweight REST API for stamping transparent PNG signatures onto PDF documents.

Built with FastAPI and PyMuPDF, the service is designed to run locally with Docker or be deployed to Google Cloud Run. It integrates easily with Google Apps Script or any client capable of sending multipart/form-data requests.

---

## Features

- Stamp transparent PNG signatures onto PDF documents
- Adjustable signature position and size
- Support for signing any page in a PDF
- REST API built with FastAPI
- PyMuPDF backend for fast PDF processing
- Docker support
- Google Cloud Run ready
- Compatible with Google Apps Script

---

## Project Structure

```text
.
├── app
│   ├── api
│   ├── core
│   ├── models
│   └── services
├── tests
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

```bash
pip install -r requirements.txt
```

---

## Running locally

```bash
uvicorn app.api.main:app --reload
```

The API will be available at:

```
http://localhost:8000
```

Swagger documentation:

```
http://localhost:8000/docs
```

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

The API will then be available at:

```
http://localhost:8080
```

---

## API

### POST /sign

Uploads a PDF and a PNG signature and returns a signed PDF.

Coordinates are in PDF points (72 points = 1 inch).

- x → distance from left edge  
- y → distance from bottom edge  

### Form fields

| Field     | Type    | Description |
|----------|--------|-------------|
| pdf       | File    | PDF document |
| signature | File    | PNG signature (transparent background recommended) |
| x         | Integer | Distance from left (points) |
| y         | Integer | Distance from bottom (points) |
| width     | Integer | Signature width (points) |
| height    | Integer | Signature height (points) |
| page      | Integer | Page index (starts at 0) |

### Response

application/pdf

Returns the signed PDF as a binary file.

---

## Health Endpoints

### GET /

Returns basic service information.

### GET /health

Returns service health status.

---

## Testing

```bash
pytest
```

---

## Google Apps Script

Compatible with UrlFetchApp.fetch using multipart/form-data.

Example payload:

```javascript
payload: {
  pdf: pdfBlob,
  signature: signatureBlob,
  x: 100,
  y: 100,
  width: 120,
  height: 50,
  page: 0,
}
```

---

## Libraries

- FastAPI
- PyMuPDF
- Pytest
- Docker

---

## License

MIT License
