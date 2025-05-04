#!/usr/bin/env python

from flask import Flask, render_template, jsonify, Response, request
from newsgen import renderNews
import json, os

HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5555))
DEBUG = bool(os.environ.get('DEBUG'))

app = Flask(__name__)
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

@app.route("/healthz")
def healthz():
    return {'status': 'ok'}

@app.route("/<page>")
def pg(page):
    match page:
        case "news": args = renderNews()
        case _:      args = None
        
    return renderPage(f"pages/{page}.html", args)

@app.route('/api/', methods=['GET'])
def greet_man():
    return jsonify(man_content)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
