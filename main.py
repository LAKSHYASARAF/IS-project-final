from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import hashlib
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET', 'dev-secret')

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
CHECKSUM_FILE = os.path.join(BASE_DIR, 'checksums.json')
ALLOWED_EXTENSIONS = None 

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def load_checksums():
    if not os.path.exists(CHECKSUM_FILE):
        return {}
    with open(CHECKSUM_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except Exception:
            return {}


def save_checksums(d):
    with open(CHECKSUM_FILE, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2)


def sha256_fileobj(fileobj):
    fileobj.seek(0)
    h = hashlib.sha256()
    for chunk in iter(lambda: fileobj.read(8192), b""):
        h.update(chunk)
    fileobj.seek(0)
    return h.hexdigest()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if 'file' not in request.files:
        flash('No file part in request', 'error')
        return redirect(url_for('index'))

    f = request.files['file']
    if f.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))

    filename = secure_filename(f.filename)
    checksum = sha256_fileobj(f.stream)

    save_path = os.path.join(UPLOAD_FOLDER, filename)
    f.save(save_path)

    data = load_checksums()
    data[filename] = {
        'checksum': checksum,
        'registered_at': datetime.utcnow().isoformat() + 'Z'
    }
    save_checksums(data)

    flash(f'Registered {filename} with SHA256 {checksum}', 'success')
    return redirect(url_for('index'))


@app.route('/verify', methods=['POST'])
def verify():
    if 'file' not in request.files:
        flash('No file part in request', 'error')
        return redirect(url_for('index'))

    f = request.files['file']
    if f.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))

    filename = secure_filename(f.filename)
    checksum = sha256_fileobj(f.stream)

    data = load_checksums()
    if filename not in data:
        flash(f'No registered checksum found for {filename}', 'error')
        return redirect(url_for('index'))

    registered = data[filename]['checksum']
    match = (registered == checksum)

    if match:
        flash(f'Verified {filename}: OK (checksums match)', 'success')
    else:
        flash(f'Verified {filename}: MISMATCH! Registered={registered} Current={checksum}', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=8000)