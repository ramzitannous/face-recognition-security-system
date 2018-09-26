import concurrent.futures as Processor
import os

from flask import Flask, request, flash, redirect, Response, jsonify
from werkzeug.utils import secure_filename

from constants import DBTYPES
from train import Trainer

app = Flask(__name__)
app.secret_key = "841578451845asdasdasfasf"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

whiteListTrainer = Trainer(DBTYPES.WHITELIST)
blackListTrainer = Trainer(DBTYPES.BLACKLIST)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/<dbType>/names")
def getNames(dbType):
    if dbType == DBTYPES.WHITELIST:
        return jsonify(whiteListTrainer.readNames())
    else:
        return jsonify(blackListTrainer.readNames())


@app.route("/<dbType>/<name>/images", methods=['POST'])
def upload_file(name,dbType):
    print(dbType,)
    if dbType == DBTYPES.WHITELIST:
        path = whiteListTrainer.imagesPath % name
    else:
        path=blackListTrainer.imagesPath % name
    if not os.path.exists(path):
        os.mkdir(path)

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename) and os.path.exists(path):
            filename = secure_filename(file.filename)
            file.save(os.path.join(path, filename))
            return Response(status=200)
        else:
            return Response(status=404)


@app.route("/<dbType>/add_name", methods=['POST'])
def addUser(dbType):
    if request.method == "POST":
        try:
            name = request.json["name"]
            if dbType == DBTYPES.WHITELIST:
                whiteListTrainer.addName(name)
            else:
                blackListTrainer.addName(name)
            return Response(status=200)
        except:
            return Response(status=500)


@app.route("/<dbType>/remove_name", methods=['POST'])
def removeUser(dbType):
    if request.method == "POST":
        try:
            name = request.json["name"]
            if dbType == DBTYPES.WHITELIST:
                whiteListTrainer.removeName(name)
            else:
                blackListTrainer.removeName(name)
            return Response(status=200)
        except:
            return Response(status=500)


@app.route("/<dbType>/train", methods=['POST'])
def train(dbType):
    if request.method == "POST":
        try:
            name = request.json["name"]
            if dbType == DBTYPES.WHITELIST:
                whiteListTrainer.trainPerson(name)
            else:
                blackListTrainer.trainPerson(name)
            return Response(status=200)
        except:
            return Response(status=500)


@app.route("/<dbType>/train_image", methods=['POST'])
def trainImage(dbType):
    if request.method == "POST":
        try:
            name = request.json["name"]
            image = request.json["image"]
            if dbType == DBTYPES.WHITELIST:
                with Processor.ProcessPoolExecutor() as Executor:
                    Executor.map(whiteListTrainer.trainImage(name, image))
            else:
                with Processor.ProcessPoolExecutor() as Executor:
                    Executor.map(blackListTrainer.trainImage(name, image))
            return Response(status=200)
        except:
            return Response(status=500)


if __name__ == '__main__':
    app.run(host="0.0.0.0")