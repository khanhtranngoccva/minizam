from flask import Flask
from flask_cors import CORS

app = Flask("minizam")
app.config['MAX_CONTENT_LENGTH'] = 128 * 1000 * 1000
CORS(app)
