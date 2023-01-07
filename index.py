import os
import uuid
from flask import Flask, flash, request, redirect, send_file, render_template, abort
from werkzeug.utils import secure_filename
import sankey_gen
import threading
import shutil
import time


UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'dying-worm-weather-chance'

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

@app.route("/<session_id>/<filename>")
def session(session_id, filename):
    mime = 'html'
    if filename.rsplit('.', 1)[1].lower() == 'png':
        mime = 'image/png'
    else:
        mime = 'text/html'
    try:
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], session_id, filename), mimetype=mime)
    except FileNotFoundError as e:
        abort(404)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/generate", methods=["POST"])
def generate():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        session_id = str(uuid.uuid4())
        try:
            os.mkdir(os.path.join(app.config['UPLOAD_FOLDER'], session_id))
        except OSError as _:
            pass
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], session_id, "input.csv"))
        img, html, sankeymatic = sankey_gen.main(session_id=session_id)
        with open(os.path.join(app.config['UPLOAD_FOLDER'], session_id, "sankey.png"), "wb") as bf:
            bf.write(img)
        with open(os.path.join(app.config['UPLOAD_FOLDER'], session_id, "sankey.html"), "w") as f:
            f.write(html)
        
        th = threading.Thread(target=cleanup, args=(os.path.join(app.config['UPLOAD_FOLDER'], session_id),))
        th.start()
        return render_template('generate.html', sessionid=session_id, sankeymatic=sankeymatic)

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(404)
def internal_server_error(e):
    return render_template('404.html'), 404

def cleanup(path):
    time.sleep(1 * 3600)
    shutil.rmtree(path)
    print(path, "cleaned up")

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=10080)
