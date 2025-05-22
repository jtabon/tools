from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from requests.exceptions import RequestException

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/test-urls', methods=['POST'])
def test_urls():
    data = request.get_json()
    urls = data.get('urls', [])
    results = []

    for url in urls:
        try:
            response = requests.get(url.strip(), timeout=10)
            status = response.status_code
            message = "OK" if status == 200 else "Not Loading"
        except RequestException as e:
            status = None
            message = str(e)
        results.append({'url': url, 'status': status, 'message': message})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
