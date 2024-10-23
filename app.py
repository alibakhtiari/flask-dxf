from flask import Flask, request, send_file, render_template

import ezdxf
from ezdxf.enums import TextEntityAlignment
from PIL import Image, ImageDraw, ImageFont

import qrcode
import os

app = Flask(__name__)

def check_file_exists(filename):
    return os.path.isfile(filename)

@app.route("/", methods=["POST"])
def generate_dxf():
    referring_url = request.referrer
    if referring_url and referring_url.startswith("https://ramzarznegaran.com") and request.method == "POST":
    # if request.method == "POST":
        url = request.form.get("url")
        model = request.form.get("model")
        serial = request.form.get("serial")
        output_file_path = serial + ".dxf"

        # Read the existing DXF document
        file_path = "1.dxf"
        # doc = ezdxf.readfile(file_path)
        doc = ezdxf.new()
        msp = doc.modelspace()

        modelText = msp.add_text(
            model,
            dxfattribs={
                "layer": "Text",
                "height": 3,
                "width": 0.8,
            },
        )
        modelText.set_placement(
            (70, 58), align=TextEntityAlignment.MIDDLE_CENTER)

        if len(serial) > 18:
            first_line = serial[:18]
            second_line = serial[18:]

            first_lineText = msp.add_text(
                first_line,
                dxfattribs={
                    "layer": "Text",
                    "height": 2.5,
                    "width": 0.8,
                },
            )
            second_lineText = msp.add_text(
                second_line,
                dxfattribs={
                    "layer": "Text",
                    "height": 2.5,
                    "width": 0.8,
                },
            )
            first_lineText.set_placement(
                (70, 51), align=TextEntityAlignment.LEFT)
            second_lineText.set_placement(
                (70, 47), align=TextEntityAlignment.LEFT)

        else:
            serialText = msp.add_text(
                serial,
                dxfattribs={
                    "layer": "Text",
                    "height": 2.5,
                    "width": 0.8,
                },
            )
            serialText.set_placement(
                (70, 49.5), align=TextEntityAlignment.MIDDLE_CENTER)

        # Save the modified DXF file
        doc.saveas(output_file_path)

        return send_file(output_file_path, as_attachment=True)
    # elif request.method == "GET":
    #     return render_template("png.html")
    else:
        return render_template("denied.html")


@app.route('/png', methods=["GET", "POST"])
def generate_png():
    referring_url = request.referrer
    if referring_url and referring_url.startswith("https://ramzarznegaran.com") and request.method == "POST":
    # if request.method == "POST":

        url = request.form.get("url")
        if len(url) > 80:
            box = 4
            pos = (1120, 440)
        else:
            box = 5
            pos = (1105, 430)

        model = request.form.get("model")
        serial = request.form.get("serial")
        temp_file = serial + '.jpg'

        # if check_file_exists(temp_file):
        #     return send_file(temp_file, mimetype='image/jpg', as_attachment=True)

        # Load the original image
        original_image = Image.open('1.jpg')

        # Create a QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box,
            border=0,
        )
        qr.add_data(url)  # Replace with your desired URL or data
        # qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Create a drawing context
        draw = ImageDraw.Draw(original_image)

        # Load a font (you may need to specify the font file path)
        font = ImageFont.truetype("bold.ttf", size=30)
        fnt = ImageFont.truetype("bold.ttf", size=28)

        if len(serial) > 20:
            first_line = serial[:20]
            second_line = serial[20:]
            draw.text((700, 355), first_line, fill="black", font=fnt)
            draw.text((700, 385), second_line, fill="black", font=fnt)
        else:
            draw.text((700, 370), serial, fill="black", font=font)

        draw.text((700, 277), model, fill="black", font=font)

        # Paste the QR code onto the image
        original_image.paste(qr_image, pos)

        # Save the modified image as a temporary file
        original_image.save(temp_file)

        # Send the generated image as a response
        return send_file(temp_file, mimetype='image/jpg', as_attachment=True)
    # elif request.method == "GET":
    #     return render_template("png.html")
    else:
        return render_template("denied.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
