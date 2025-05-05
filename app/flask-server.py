#!/usr/bin/env python

from flask import Flask, render_template, jsonify, abort
from newsgen import render_news
import json, os
from typing import Any

HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5555))
DEBUG = bool(os.environ.get('DEBUG'))

app = Flask(__name__)
man_content = {
    "Пока что заглушка": "Потом что нить добавим",
}

@app.errorhandler(404)
def page_not_found(e):
    return render_template("pattern.html", body=render_template("404.html"))

def render_page(dir: str, args: any = None):
    if dir in app.jinja_env.list_templates():
        return render_template("pattern.html", body=render_template(dir, args=args))
    else:
        abort(404)

@app.route("/")
def index():
    return render_page("pages/index.html")

@app.route("/healthz")
def healthz():
    return {'status': 'ok'}

@app.route("/<page>")
def pg(page):
    match page:
        case "news": args = render_news()
        case _:      args = None
        
    return render_page(f"pages/{page}.html", args)

@app.route('/api/', methods=['GET'])
def greet_man():
    return jsonify(man_content)

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
