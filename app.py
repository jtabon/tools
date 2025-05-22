from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
from requests.exceptions import RequestException
import validators

app = Flask(__name__)

# Enable CORS (restrict to your domain if desired)
CORS(app, origins=["https://tools-n0r2.onrender.com"])

# Add rate limiting: 10 requests per minute per IP
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/test-urls', methods=['POST'])
@limiter.limit("10 per minute")  # Extra layer: limit per route
def test_urls():
    data = request.get_json()
    urls = data.get('urls', [])
    results = []

    for url in urls:
        url = url.strip()

        # ✅ Input validation
        if not validators.url(url):
            results.append({'url': url, 'status': None, 'message': 'Invalid URL'})
            continue

        try:
            response = requests.get(url, timeout=10)
            status = response.status_code
            message = "OK" if status == 200 else "Not Loading"
        except RequestException as e:
            status = None
            message = str(e)
        results.append({'url': url, 'status': status, 'message': message})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

