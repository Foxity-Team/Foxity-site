from flask import Flask, jsonify, Response, request
import random
import json
import socket

app = Flask(__name__)

def readFileLines(filename: str) -> list[str]:
    with open(filename, encoding='utf-8') as f: return f.readlines()

def readFileJson(filename: str):
    with open(filename) as f: return json.load(f)

words_path = 'words.txt'
jokes_path = 'jokes.txt'
json_headers = {'Content-Type': 'application/json; charset=utf-8'}

words = dict(map(lambda v: (v[0].lower(), v[1]),
             map(lambda v: [el.strip() for el in v.split(':')], readFileLines(words_path))))

jokes = sorted(readFileJson(jokes_path), key=lambda v: v['id'])

man_content = {
    "Что бы вывести рандомную шутку": "foxity.freemyip.com/api/joke",
    "Что бы вывести лист шуток": "foxity.freemyip.com/api/jokes",
    "Что бы вывести лист слов": "foxity.freemyip.com/api/words",
    "Что бы перевести слово на родавский язык нужно к апи отправить POST запрос со словом которое нужно перевести": "foxity.freemyip.com/api/word"
}

@app.route('/api/word', methods=['POST'])
def get_noun():
    if not request.json or 'word' not in request.json: return

    word = words.get(request.json['word'].lower(), None)
    return (jsonify({'word': word}), 200, json_headers) if word else \
           (jsonify({'error': 'Word not found'}), 404, json_headers)

@app.route('/api/words', methods=['GET'])
def list_of_words():
    return jsonify(words), 200, json_headers

@app.route('/api/joke', methods=['GET'])
def get_random_joke():
    return jsonify(random.choice(jokes)), 200, json_headers

@app.route('/api/jokes', methods=['GET'])
def list_of_jokes():
    return jsonify(jokes), 200, json_headers

@app.route('/api/man', methods=['GET'])
def greet_man():
    return jsonify(man_content)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8000

    ip_address = socket.gethostbyname(socket.gethostname())

    app.run(host=host, port=port)