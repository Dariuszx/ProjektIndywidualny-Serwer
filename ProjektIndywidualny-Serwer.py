from flask import Flask
from flask.ext.cors import CORS
from database import Database

app = Flask(__name__)
db = Database()
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/file')
def get_files():
    return db.get_all_files()


@app.route('/file/<file_id>')
def get_file(file_id):
    return db.get_file(file_id)


@app.route('/file/shared', methods=['GET'])
def get_shared_files():
    return db.get_shared_files()


@app.route('/file/share/<file_id>/<user_id>')
def share_file(file_id, user_id):
    return db.share_file(file_id, user_id)


@app.route('/user/login', methods=['POST'])
def user_login():
    return db.user_login()


@app.route('/user/principal', methods=['GET'])
def user_principal():
    return db.user_principal()


@app.route('/user/logout', methods=['GET'])
def user_logout():
    return db.user_logout()


@app.route('/user/list', methods=['GET'])
def user_list():
    return db.user_list()


@app.route('/user/create', methods=['POST'])
def create_account():
    return NotImplemented


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
