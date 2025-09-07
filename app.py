from flask import Flask, request, send_file, render_template
from PIL import Image, ImageDraw, ImageFont
import ezdxf
from ezdxf.enums import TextEntityAlignment
import qrcode
import os

app = Flask(__name__)


def create_label_english(data, qr_url, template_path, font_path, output_path):
    """
    Generates a label with English text and a QR code.
    This version does not use RGBA conversion or print statements.
    """
    coordinates = {
        "device_name":   (720, 90),
        "serial_number": (720, 190),
        "product_id":    (720, 295),
        "tracking_id":   (720, 390),
    }
    qr_position = (150, 250)
    qr_size = (200, 200)
    font_size = 30
    text_color = "black"

    try:
        base_image = Image.open(template_path)
        draw = ImageDraw.Draw(base_image)
        font = ImageFont.truetype(font_path, font_size)
    except FileNotFoundError:
        return False

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(
        fill_color="black", back_color="white").resize(qr_size)

    base_image.paste(qr_img, qr_position)

    for key, text in data.items():
        draw.text(
            coordinates[key],
            text,
            font=font,
            fill=text_color,
            anchor="ra"
        )

    base_image.save(output_path)
    return True


@app.route("/", methods=["GET", "POST"])
def generate_dxf():
    # In debug mode, GET requests open the template.
    if app.debug and request.method == "GET":
        return render_template("dxf.html")

    # In production, only POST requests from the correct domain are allowed.
    if request.method == "POST":
        referring_url = request.referrer
        # Check referrer URL only if not in debug mode
        if not app.debug and (not referring_url or not referring_url.startswith("https://ramzarznegaran.com")):
            return render_template("denied.html")

        url = request.form.get("url")
        model = request.form.get("model")
        serial = request.form.get("serial")
        output_file_path = serial + ".dxf"

        doc = ezdxf.new()
        msp = doc.modelspace()

        modelText = msp.add_text(
            model,
            dxfattribs={"layer": "Text", "height": 3, "width": 0.8},
        )
        modelText.set_placement(
            (70, 58), align=TextEntityAlignment.MIDDLE_CENTER)

        if len(serial) > 18:
            first_line = serial[:18]
            second_line = serial[18:]

            first_lineText = msp.add_text(
                first_line,
                dxfattribs={"layer": "Text", "height": 2.5, "width": 0.8},
            )
            second_lineText = msp.add_text(
                second_line,
                dxfattribs={"layer": "Text", "height": 2.5, "width": 0.8},
            )
            first_lineText.set_placement(
                (70, 51), align=TextEntityAlignment.LEFT)
            second_lineText.set_placement(
                (70, 47), align=TextEntityAlignment.LEFT)
        else:
            serialText = msp.add_text(
                serial,
                dxfattribs={"layer": "Text", "height": 2.5, "width": 0.8},
            )
            serialText.set_placement(
                (70, 49.5), align=TextEntityAlignment.MIDDLE_CENTER)

        doc.saveas(output_file_path)
        return send_file(output_file_path, as_attachment=True)
    else:
        # Deny GET requests in production
        return render_template("denied.html")


@app.route('/png', methods=["GET", "POST"])
def generate_png():
    # In debug mode, GET requests open the template.
    if app.debug and request.method == "GET":
        return render_template("png.html")

    # In production, only POST requests from the correct domain are allowed.
    if request.method == "POST":
        referring_url = request.referrer
        # Check referrer URL only if not in debug mode
        if not app.debug and (not referring_url or not referring_url.startswith("https://ramzarznegaran.com")):
            return render_template("denied.html")

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

        original_image = Image.open('1.jpg')
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box,
            border=0,
        )
        qr.add_data(url)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        draw = ImageDraw.Draw(original_image)
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
        qr_width, qr_height = qr_image.size
        paste_box = (pos[0], pos[1], pos[0] + qr_width, pos[1] + qr_height)
        original_image.paste(qr_image, paste_box)
        original_image.save(temp_file)
        return send_file(temp_file, mimetype='image/jpg', as_attachment=True)
    else:
        # Deny GET requests in production
        return render_template("denied.html")


@app.route('/label', methods=["GET", "POST"])
def generate_new_label():
    # In debug mode, GET requests open the template.
    if app.debug and request.method == "GET":
        return render_template("label.html")

    # In production, only POST requests from the correct domain are allowed.
    if request.method == "POST":
        referring_url = request.referrer
        # Check referrer URL only if not in debug mode
        if not app.debug and (not referring_url or not referring_url.startswith("https://ramzarznegaran.com")):
            return render_template("denied.html")

        label_data = {
            "device_name": request.form.get("device_name"),
            "serial_number": request.form.get("serial_number"),
            "product_id": request.form.get("product_id"),
            "tracking_id": request.form.get("tracking_id"),
        }
        qr_code_url = request.form.get("qr_code_url")

        serial_num = label_data["serial_number"]
        if not all([serial_num, qr_code_url]):
            return "Missing form data (serial_number, qr_code_url)", 400

        template_file = "clean.jpg"
        font_file = "regular.ttf"
        output_file = f"{serial_num}_label.jpg"

        success = create_label_english(
            label_data, qr_code_url, template_file, font_file, output_file)

        if success:
            return send_file(output_file, mimetype='image/jpeg', as_attachment=True)
        else:
            return "Failed to create label image.", 500
    else:
        # Deny GET requests in production
        return render_template("denied.html")


if __name__ == "__main__":
    # Use 'flask run --debug' for development mode.
    # The debug flag will automatically be set to True.
    app.run(host="0.0.0.0", port=5000)
