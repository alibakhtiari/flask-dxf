from flask import Flask, request, send_file, render_template

import ezdxf
from ezdxf.enums import TextEntityAlignment

import qrcode

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def generate_dxf():
    if request.method == "POST":
        url = request.form.get("url")
        model = request.form.get("model")
        serial = request.form.get("serial")

        # Read the existing DXF document
        file_path = "1.dxf"
        doc = ezdxf.readfile(file_path)

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,  # Increase the box size to make the QR code larger
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_matrix = qr.get_matrix()
        qr_size = len(qr_matrix)

        # Add a new layer for the QR code
        doc.layers.new(name="QRCode", dxfattribs={"color": 7})

        # Add the QR code to the DXF file
        msp = doc.modelspace()
        
        font_path = "Arial.ttf"  # Replace with the actual font path
        font_name = "Arial"  # Name to use for the font
        doc.styles.new(font_name, dxfattribs={'font': font_path})

        
        qr_x_offset = 108  # X-coordinate offset for the QR code
        qr_y_offset = 27  # Y-coordinate offset for the QR code
        for y in range(qr_size):
            for x in range(qr_size):
                if qr_matrix[y][x]:
                    msp.add_polyline2d(
                        [(x * 0.5 + qr_x_offset, y * 0.5 + qr_y_offset),  # Increase the scale by multiplying with 10
                        ((x + 1) * 0.5 + qr_x_offset, y * 0.5 + qr_y_offset),
                        ((x + 1) * 0.5 + qr_x_offset, (y + 1) * 0.5 + qr_y_offset),
                        (x * 0.5 + qr_x_offset, (y + 1) * 0.5 + qr_y_offset),
                        (x * 0.5 + qr_x_offset, y * 0.5 + qr_y_offset)],
                        close=True,
                        # Adjust the insert point as needed
                        dxfattribs={"layer": "QRCode"},

                    )

            modelText = msp.add_text(
                model,
                dxfattribs={
                    "layer": "Text",
                    "height": 3,
                    "width": 0.6,
                    "style": "ariblk.ttf"
                    },
            )
            modelText.set_placement((88, 58), align=TextEntityAlignment.MIDDLE_CENTER)
            
            if len(serial) > 20:
                first_line = serial[:20]
                second_line = serial[20:]

                first_lineText = msp.add_text(
                    first_line,
                    dxfattribs={
                        "layer": "Text",
                        "style": "ariblk.ttf",
                        "height": 3,
                        "width": 0.6,  # Adjust the spacing between letters (0.8 is the default value)
                    },
                )
                second_lineText = msp.add_text(
                second_line,
                dxfattribs={
                    "layer": "Text",
                    "style": "ariblk.ttf",
                    "height": 3,
                    "width": 0.6,  # Adjust the spacing between letters (0.8 is the default value)
                    },
                )
                first_lineText.set_placement((70, 51), align=TextEntityAlignment.LEFT)
                second_lineText.set_placement((70, 48), align=TextEntityAlignment.LEFT)

            else:
                serialText = msp.add_text(
                    serial,
                    dxfattribs={
                        "layer": "Text",
                        "style": "ariblk.ttf",
                        "height": 2.5,
                        "width": 0.5,  # Adjust the spacing between letters (0.8 is the default value)
                    },
                )
                serialText.set_placement((88, 49.5), align=TextEntityAlignment.MIDDLE_CENTER)
        
        # Save the modified DXF file
        output_file_path = "2.dxf"
        doc.saveas(output_file_path)

        return send_file(output_file_path, as_attachment=True)
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
