from flask import Flask, jsonify, Response, request
import random
import json
import socket

words = {}
app = Flask(__name__)

with open('words.txt', 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        word, word2 = map(str.strip, line.split(':'))
        words[word.lower()] = word2

def load_jokes_from_file():
    try:
        with open('jokes.txt', 'r') as file:
            jokes_data = json.load(file)
        return jokes_data
    except FileNotFoundError:
        return []

jokes = load_jokes_from_file()

@app.route('/api/word', methods=['POST'])
def get_noun():
    if request.json and 'word' in request.json:
        word = request.json['word'].lower()
        word2 = words.get(word, None)
        if word2:
            return jsonify({'word': word2}), 200, {'Content-Type': 'application/json; charset=utf-8'}
        else:
            return jsonify({'error': 'Word not found'}), 404, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api/words', methods=['GET'])
def list_of_words():
    return jsonify(words), 200, {'Content-Type': 'application/json; charset=utf-8'}

@app.route('/api/joke', methods=['GET'])
def get_random_joke():
    random_joke = random.choice(jokes)
    ordered_joke = {
        "title": random_joke["title"],
        "content": random_joke["content"],
        "id": random_joke["id"]
    }
    response = Response(json.dumps(ordered_joke, indent=4), content_type='application/json')
    return response

@app.route('/api/jokes', methods=['GET'])
def list_of_jokes():
    ordered_jokes = [{"title": joke["title"], "content": joke["content"], "id": joke["id"]} for joke in jokes]
    response = Response(json.dumps(ordered_jokes, indent=4), content_type='application/json')
    return response

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8000

    ip_address = socket.gethostbyname(socket.gethostname())
    
    print(f"Server running at {ip_address}:{port}")

    app.run(host=host, port=port)
