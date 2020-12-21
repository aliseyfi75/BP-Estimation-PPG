import os
import jsonpickle
from flask import Flask, request, flash, url_for
from werkzeug.utils import secure_filename, redirect
import logging

log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
app = Flask(__name__)
UPLOAD_FOLDER = 'C:/Users/Parsa/Desktop/flask_sever/Uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
isAvailable = True

queue = []
pmode = 1  # 1 is pen , 2 is brush, 3 is save brush , 4 is save pen
flagm = 1


class SimpleResponse:
    def __init__(self, code):
        self.code = code


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)
        if file.filename == '':
            print('yes4')
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'vid.mp4'))
            return redirect(url_for('upload_file',
                                    filename=filename))
    else:
        return jsonpickle.encode(SimpleResponse(1))


if __name__ == '__main__':
    app.secret_key = 'dhgiuwehiuwehiughewiu'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=5000)
