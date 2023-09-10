from flask import Flask, request, send_file, render_template

import ezdxf
from ezdxf.enums import TextEntityAlignment
from PIL import Image, ImageDraw, ImageFont

import qrcode

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def generate_dxf():
    referring_url = request.referrer
    if referring_url and referring_url.startswith("https://ramzarznegaran.com") and request.method == "POST":
    # if request.method == "POST":
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
        
        # Add the QR code to the DXF file with filled squares
        qr_x_offset = 108  # X-coordinate offset for the QR code
        qr_y_offset = 27  # Y-coordinate offset for the QR code
        square_size = 0.5
        
        for y in range(qr_size):
            for x in range(qr_size):
                if qr_matrix[y][x]:
                    msp.add_solid(
                        [
                            (x * square_size + qr_x_offset, y * square_size + qr_y_offset),
                            ((x + 1) * square_size + qr_x_offset, y * square_size + qr_y_offset),
                            ((x + 1) * square_size + qr_x_offset, (y + 1) * square_size + qr_y_offset),
                            (x * square_size + qr_x_offset, (y + 1) * square_size + qr_y_offset),
                        ],
                        dxfattribs={"layer": "QRCode", "color": 0},  # Set color to black (0)
                    )

            modelText = msp.add_text(
                model,
                dxfattribs={
                    "layer": "Text",
                    "height": 3,
                    "width": 0.8,
                    },
            )
            modelText.set_placement((70, 58), align=TextEntityAlignment.MIDDLE_CENTER)
            
            if len(serial) > 18:
                first_line = serial[:18]
                second_line = serial[18:]

                first_lineText = msp.add_text(
                    first_line,
                    dxfattribs={
                        "layer": "Text",
                        "height": 2.5,
                        "width": 0.8,  # Adjust the spacing between letters (0.8 is the default value)
                    },
                )
                second_lineText = msp.add_text(
                second_line,
                dxfattribs={
                    "layer": "Text",
                    "height": 2.5,
                    "width": 0.8,  # Adjust the spacing between letters (0.8 is the default value)
                    },
                )
                first_lineText.set_placement((70, 51), align=TextEntityAlignment.LEFT)
                second_lineText.set_placement((70, 47), align=TextEntityAlignment.LEFT)

            else:
                serialText = msp.add_text(
                    serial,
                    dxfattribs={
                        "layer": "Text",
                        "height": 2.5,
                        "width": 0.8,  # Adjust the spacing between letters (0.8 is the default value)
                    },
                )
                serialText.set_placement((70, 49.5), align=TextEntityAlignment.MIDDLE_CENTER)
        
        # Save the modified DXF file
        output_file_path = serial + ".dxf"
        doc.saveas(output_file_path)

        return send_file(output_file_path, as_attachment=True)
    else:
        return render_template("denied.html")

@app.route('/png',methods=["GET", "POST"])
def generate_png():
    referring_url = request.referrer
    if referring_url and referring_url.startswith("https://ramzarznegaran.com") and request.method == "POST":
    # if request.method == "POST":
        url = request.form.get("url")
        model = request.form.get("model")
        serial = request.form.get("serial")

        # Load the original image
        original_image = Image.open('1.jpg')

        # Create a QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=5,
            border=0,
        )
        qr.add_data(url)  # Replace with your desired URL or data
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Create a drawing context
        draw = ImageDraw.Draw(original_image)

        # Load a font (you may need to specify the font file path)
        font = ImageFont.truetype("bold.ttf", size=30)
        fnt = ImageFont.truetype("bold.ttf", size=28)

        if len(serial) > 20:
            first_line = serial[:20]
            second_line = serial[20:]
            draw.text((700,355), first_line, fill="black", font=fnt)
            draw.text((700, 385), second_line, fill="black", font=fnt)
        else:
            draw.text((700, 370), serial, fill="black", font=font)
        
        draw.text((700, 277), model, fill="black", font=font)

        # Paste the QR code onto the image
        original_image.paste(qr_image, (1105, 430))

        # Save the modified image as a temporary file
        temp_file = serial + '.jpg'
        original_image.save(temp_file)

        # Send the generated image as a response
        return send_file(temp_file, mimetype='image/jpg', as_attachment=True)
    else:
        return render_template("denied.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
