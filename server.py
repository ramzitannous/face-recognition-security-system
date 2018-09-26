from flask import Flask

from constants import DBTYPES
from train import Trainer

app = Flask(__name__)
app.secret_key = "841578451845asdasdasfasf"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
# app.config['UPLOAD_FOLDER'] = Paths.UPLOAD_FOLDER

whiteListTrainer = Trainer(DBTYPES.WHITELIST)
blackListTrainer = Trainer(DBTYPES.BLACKLIST)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS \
 \
           @ app.route("/names/<dbType>")


def getNames(dbType):
    if dbType == DBTYPES.WHITELIST:
        return whiteListTrainer.readNames()
    else:
        return blackListTrainer.readNames()


# @app.route("/images/<name>",methods=['POST'])
# def upload_file(name):
#     path=os.path.join(app.config["UPLOAD_FOLDER"],name)
#     if not os.path.exists(path):
#         os.mkdir(path)
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#         file = request.files['file']
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename) and os.path.exists(path):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(path,filename))
#             return Response(status=200)
#         else:
#             return Response(status=404)
#
# @app.route("/name",methods=['POST'])
# def addUser():
#     if request.method=="POST":
#         try:
#             name=request.json["name"]
#             os.mkdir(Paths.UPLOAD_FOLDER+"/"+name)
#             names=trainer.readNames()
#             names.append(name)
#             saved_names = np.array(names)
#             np.savetxt(Paths.KNOWN_NAME_FILE, saved_names, delimiter=",", fmt="%s")
#             return Response(status=200)
#         except :
#             return Response(status=500)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
