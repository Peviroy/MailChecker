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

nbc = MultiNB_Controller()
bc = BILSTM_Controller()
lgc_h = LSTMG_Controller(model_type='model_ham')
lgc_s = LSTMG_Controller(model_type='model_spam')


def test():
    print(1, nbc.predict(
        'Even my brother is not like to speak with me. They treat me like aids patent'))
    print(2, bc.predict(
        'Even my brother is not like to speak with me. They treat me like aids patent'))
    print(3, lgc_h.predict(
        'Even my brother is not like to speak with me. They treat me like aids patent'))
    print(4, lgc_s.predict(
        'Even my brother is not like to speak with me. They treat me like aids patent'))


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


@app.route('/getPredict', methods=['POST'])
def predict():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    mailcontent = data['content']
    model_type = data['model']
    img_path = ''
    prob = ''
    if model_type == 'Model1':
        prediction, prob = nbc.predict(mailcontent)
    else:
        prediction, img_path = bc.predict(mailcontent)
    response = {
        'msg': prediction,
        'imgPath': img_path,
        'prob': prob
    }
    print(response)
    return jsonify(response)


@app.route('/getContent', methods=['POST'])
def generator():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    mailcontent = data['content']
    mailtype = data['type']
    nextwords = 50

    if mailtype == 'ham':
        content_generated = lgc_h.predict(mailcontent, nextwords)
    else:
        content_generated = lgc_s.predict(mailcontent, nextwords)

    response = {
        'msg': content_generated,
    }
    return jsonify(response)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html'), 404
