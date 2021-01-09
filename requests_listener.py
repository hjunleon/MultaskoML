# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

import parseApiInput


"""
set FLASK_APP=requests_listener.py
"""
app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello World!"

@app.route('/api/categorise', methods=['GET', 'POST'])
@cross_origin()
def get_categorised_data():
    method = request.method
    if method == 'GET':
        categories = parseApiInput.get_from_backend()
        response = jsonify(result=categories)
        return response
if __name__ == "__main__":
    app.run()