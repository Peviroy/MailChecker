from flask import Flask, render_template, jsonify, request
from backend.model_bilstm import BILSTM_Controller
from backend.model_generator import LSTMG_Controller
from backend.model_nb import MultiNB_Controller
from flask_cors import CORS
import json

app = Flask(__name__,
            template_folder="./dist",
            static_folder="./dist",
            static_url_path='',
            )
cors = CORS(app, resources={r'/getMsg': {"origin": "*"}})

bc = BILSTM_Controller()
lgc_h = LSTMG_Controller(model_type='model_ham')
lgc_s = LSTMG_Controller(model_type='model_spam')
nbc = MultiNB_Controller()


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


@app.route('/getPredict', methods=['POST'])
def Test():
    data = json.loads(request.get_data(as_text=True))
    mailcontent = data['content']
    model_type = data['model']
    img_path = ''
    prob = ''
    if model_type == 2:
        prediction, img_path = bc.predict(mailcontent)
    else:
        prediction, prob = nbc.predict(mailcontent)
    response = {
        'msg': prediction,
        'imgPath': img_path,
        'prob': prob
    }
    print(data)
    return jsonify(response)


@app.route('/getContent', methods=['POST'])
def Test():
    data = json.loads(request.get_data(as_text=True))
    mailcontent = data['content']
    mailtype = data['type']
    nextwords = data['nextwords']

    if mailtype == 'ham':
        content_generated = lgc_h.predict(mailcontent, nextwords)
    else:
        content_generated = lgc_s.predict(mailcontent, nextwords)

    response = {
        'msg': content_generated,
    }
    print(data)
    return jsonify(response)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html'), 404
