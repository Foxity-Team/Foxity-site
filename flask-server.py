from flask import Flask, render_template
import json

app = Flask(__name__)
config = json.loads(open("config.json", "r").read())

def renderPage(dir: str):
    try:    body = render_template(dir)
    except: return None

    return render_template("pattern.html", body=body)

@app.route("/")
def index():
    return renderPage("pages/index.html")

@app.route("/<page>")
def hello_world(page):
    rendered = renderPage(f"pages/{page}.html")

    if rendered: return rendered
    else:        return renderPage("404.html")

app.run(port=config["port"])