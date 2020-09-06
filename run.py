from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__,
            template_folder="./dist",
            static_folder="./dist",
            static_url_path='',
            )
cors = CORS(app, resources={r'/getMsg': {"origin": "*"}})


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/getMsg', methods=['GET', 'POST'])
def predict():
    response = {
        'msg': 'Oops, predict unsupport now'
    }
    return jsonify(response)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html'), 404
