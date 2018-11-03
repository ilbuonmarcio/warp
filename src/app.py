from flask import Flask, request, Response, render_template, redirect, send_from_directory, session
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import json
import time
import random

UPLOAD_FOLDER = './uploads/'
TEMPLATE_FOLDER = './templates/'

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)  # Set to a fixed value when putting into production environment
app.config['SESSION_COOKIE_NAME'] = 'session_warp'
app.config['SESSION_COOKIE_PATH'] = '/'


@app.route('/', methods=["GET"])
def root():
    return render_template('index.html')


@app.route('/getfile/<path:path>', methods=["GET"])
def getfile(path):
    return render_template('file.html', file_properties={
        "filename": session["filename"],
        "filepath": session["filepath"],
        "password": session["password"]
    })


@app.route('/uploadfile', methods=["POST"])
def uploadfile():
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect('/')

        uploaded_file = request.files['file']

        if uploaded_file.filename == '':
            return redirect('/')

        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(
                os.path.join(app.config['UPLOAD_FOLDER'], filename)
            )

            json_response = {
                'filepath': '1234'
            }

            session['filename'] = uploaded_file.filename
            session['filepath'] = '1234'
            session['password'] = '5678'

            return json.dumps(json_response)


if __name__ == "__main__":
    CORS(app)
