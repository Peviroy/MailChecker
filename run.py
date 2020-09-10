from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__,
            template_folder="./dist",
            static_folder="./dist",
            static_url_path='',
            )
cors = CORS(app, resources={r'/getMsg': {"origin": "*"}})


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
    response.headers['Access-Control-Expose-Headers'] = '*'
    return response


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/getMsg', methods=['GET'])
def predict():
    response = {
        'msg': 'Oops, predict unsupport now'
    }
    print(response)
    return jsonify(response)


@app.route('/postMsg', methods=['POST'])
def Test():
    data = json.loads(request.get_data(as_text=True))
    mailcontent = data['content']
    response = {
        'msg': mailcontent
    }
    print(data)
    return jsonify(response)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html'), 404
