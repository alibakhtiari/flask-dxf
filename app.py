from flask import Flask, request, send_file, render_template


app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def generate_dxf():
    
    return '<p>New Server</p>'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)