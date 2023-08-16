from flask import Flask, request, send_file, render_template


app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def generate_dxf():
    if request.method == "POST":
        url = request.form.get("url")
        model = request.form.get("model")
        serial = request.form.get("serial")
        
        
        return f'<p>URL:{url}</p><p>model:{model}</p><p>Serial:{serial}</p>'
    else:
        return '<p>GET</p>'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)