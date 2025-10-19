# Flask-DXF

A Flask web application that generates DXF files, PNG images, and labels with QR codes based on user-provided data via POST requests.

## Features

- **DXF Generation**: Creates CAD files with model and serial number text.
- **PNG Generation**: Produces images with embedded QR codes, model, and serial information.
- **Label Generation**: Generates formatted labels with device details and QR codes.
- **Security**: In production mode, restricts POST requests to a specific domain for security.
- **Debug Mode**: Allows GET requests to view forms during development.

## Prerequisites

- Python 3.6+
- pip

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/alibakhtiari/flask-dxf.git
   cd flask-dxf
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Development Mode

Run the application in debug mode:
```bash
flask --app app --debug run
```

In debug mode, navigate to the root URL to access the forms.

### Production Mode

For production deployment, use:
```bash
gunicorn app:app
```

### Docker

Build and run with Docker:
```bash
docker build -t flask-dxf-app .
docker run -d --restart always -p 127.0.0.1:5000:5000 --name dxf_container flask-dxf-app
```

### API Endpoints

#### GET /

In debug mode, displays the DXF generation form.  
In production, returns access denied.

#### POST /

Generates a DXF file with model and serial number.

**Parameters:**
- `url`: Not used (legacy)
- `model`: Device model
- `serial`: Serial number

**Response:** Downloads the generated DXF file.

#### GET /png

In debug mode, displays the PNG generation form.

#### POST /png

Generates a PNG image with model, serial, and QR code.

**Parameters:**
- `url`: URL for QR code
- `model`: Device model
- `serial`: Serial number

**Response:** Downloads the generated JPG file.

#### GET /label

In debug mode, displays the label generation form.

#### POST /label

Generates a label image with device details and QR code.

**Parameters:**
- `device_name`: Device name
- `serial_number`: Serial number
- `product_id`: Product ID
- `tracking_id`: Tracking ID
- `qr_code_url`: URL for QR code

**Response:** Downloads the generated label image.

## Dependencies

- Flask: Web framework
- ezdxf: DXF file manipulation
- qrcode: QR code generation
- Pillow (PIL): Image processing
- requests: HTTP requests (used internally)

## License

See LICENSE file for details.
