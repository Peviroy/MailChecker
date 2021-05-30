from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from PIL import Image
import json
import base64
import io

from model.BAText_Wrapper import predict

app = Flask(
    __name__,
    template_folder="./dist",
    static_folder="./dist",
    static_url_path='',
)
cors = CORS(app, resources={r'/getMsg': {"origin": "*"}})


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers[
        'Access-Control-Allow-Headers'] = 'Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers[
        'Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, HEAD'
    response.headers['Access-Control-Expose-Headers'] = '*'
    return response


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/photos/upload', methods=['POST'])
def getImages():
    # get images
    images = request.files.getlist('images')

    encoded_picstring_list = []
    image_name_list = []
    for i, image in enumerate(images):
        print(f'Proccessing {i+1}th images')
        img = Image.open(image.stream)
        image_name_list.append(image.filename)

        img = batext_helper(img)

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        encoded_picstring_list.append(
            base64.b64encode(img_byte_arr).decode('utf-8'))

    # img.save('./tmp.jpg')
    # with open('./tmp.jpg', 'rb') as image_file:
    #     print(img_byte_arr == image_file.read())
    #     encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return {"images": encoded_picstring_list, "images_name": image_name_list}


def batext_helper(img):
    visualized_img, words = predict(img)
    return Image.fromarray(visualized_img).convert('RGB')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html'), 404
