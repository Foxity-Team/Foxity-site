from flask import Flask, render_template, jsonify, Response, request
import json
from newsgen import renderNews
import random
import json
import socket


app = Flask(__name__)
config = json.loads(open("config.json", "r").read())



def readFileLines(filename: str) -> list[str]:
    with open(filename, encoding='utf-8') as f: return f.readlines()

def readFileJson(filename: str):
    with open(filename) as f: return json.load(f)

def renderPage(dir: str, args):
    try:    body = render_template(dir, args=args)
    except: body = None

    if body: return render_template("pattern.html", body=body)
    else:    return render_template("pattern.html", body=render_template("404.html"))


jokes_path = 'static/jokes.txt'
json_headers = {'Content-Type': 'application/json; charset=utf-8'}

jokes = sorted(readFileJson(jokes_path), key=lambda v: v['id'])

man_content = {
    "Что бы вывести рандомную шутку": "foxity.freemyip.com/api/joke",
    "Что бы вывести лист шуток": "foxity.freemyip.com/api/jokes"
}


@app.route("/")
def index():
    return renderPage("pages/index.html", None)

@app.route("/<page>")
def pg(page):
    match page:
        case "news": args = renderNews()
        case _:      args = None
        
    return renderPage(f"pages/{page}.html", args)

@app.route('/api/joke', methods=['GET'])
def get_random_joke():
    return jsonify(random.choice(jokes)), 200, json_headers

@app.route('/api/jokes', methods=['GET'])
def list_of_jokes():
    return jsonify(jokes), 200, json_headers

@app.route('/api/', methods=['GET'])
def greet_man():
    return jsonify(man_content)


args = (app, config["host"], config["port"])
if not config["debug"]:
    from waitress import serve
    serve(*args)
else:
    Flask.run(*args)