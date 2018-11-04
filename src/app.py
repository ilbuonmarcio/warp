from flask import Flask, request, Response, render_template, redirect, send_from_directory, session
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import json
import time
import random
import hashlib
import uuid
import string
import base64

UPLOAD_FOLDER = './uploads/'
TEMPLATE_FOLDER = './templates/'
PASSWORD_LENGTH = 32
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
SECRET_KEY_LENGTH = 24

app = Flask(__name__, template_folder=TEMPLATE_FOLDER)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.secret_key = os.urandom(SECRET_KEY_LENGTH)  # Set to a fixed value when putting into production environment
app.config['SESSION_COOKIE_NAME'] = 'session_warp'
app.config['SESSION_COOKIE_PATH'] = '/'


@app.route('/', methods=["GET"])
def root():
    return render_template('index.html')


@app.route('/getfile/<path:path>', methods=["GET"])
def getfile(path):
    if session and session["filename"] and session["filepath"] and session["password"]:
        return render_template('file.html',
            file_properties = {
                "filename": session["filename"],
                "filepath": session["filepath"],
                "password": session["password"]
            }
        )
    else:
        return redirect('/')


@app.route('/uploadfile', methods=["POST"])
def uploadfile():
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect('/')

        uploaded_file = request.files['file']

        if uploaded_file.filename == '':
            return redirect('/')

        if uploaded_file:
            original_filename = uploaded_file.filename

            obscured_filename = base64.b64encode(
                str.encode(
                    str(uuid.uuid4())
                )
            ).decode('utf-8')

            uploaded_file.save(
                os.path.join(app.config['UPLOAD_FOLDER'], obscured_filename)
            )

            password = ''.join(
                random.choice(
                    string.ascii_uppercase +
                    string.ascii_lowercase +
                    string.digits
                )
                for _ in range(PASSWORD_LENGTH)
            )

            json_response = {
                'filepath': obscured_filename
            }

            session['filename'] = original_filename
            session['filepath'] = obscured_filename
            session['password'] = password

            return json.dumps(json_response)


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


if __name__ == "__main__":
    CORS(app)
