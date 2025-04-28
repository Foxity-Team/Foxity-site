from flask import Flask, render_template, jsonify, Response, request
import json
from newsgen import renderNews
import json



app = Flask(__name__)
config = json.loads(open("config.json", "r").read())
man_content = {
    "Пока что заглушка": "Потом что нить добавим",
}


def renderPage(dir: str, args):
    try:    body = render_template(dir, args=args)
    except: body = None

    if body: return render_template("pattern.html", body=body)
    else:    return render_template("pattern.html", body=render_template("404.html")), 404


@app.route("/")
def index():
    return renderPage("pages/index.html", None)

@app.route("/<page>")
def pg(page):
    match page:
        case "news": args = renderNews()
        case _:      args = None
        
    return renderPage(f"pages/{page}.html", args)

@app.route('/api/', methods=['GET'])
def greet_man():
    return jsonify(man_content)


args = (app, config["host"], config["port"])
if not config["debug"]:
    from waitress import serve
    serve(*args)
else:
    Flask.run(*args)