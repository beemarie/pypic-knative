from PIL import Image,ImageFilter,ImageEnhance
from flask import Flask, request, send_file
from flask_cors import CORS, cross_origin
import numpy as np
from io import BytesIO
import os

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/*": {"origins": "*"}})

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'png', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route("/")
def hello():
    return "Hello World! POST images to other endpoints for some cool image manipulations"
 
@app.route('/grey', methods=['POST','OPTIONS'])
@cross_origin()
def grey():
    if request.method == 'POST':
        image = Image.open(request.files['file']).convert('LA')
        return serve_pil_image(image)

@app.route('/pixel', methods=['POST','OPTIONS'])
@cross_origin()
def pixels():
    if request.method == 'POST':
        image = Image.open(request.files['file']).filter(ImageFilter.SHARPEN)
        return serve_pil_image(image)


@app.route('/nochange', methods=['POST','OPTIONS'])
@cross_origin()
def nochange():
    if request.method == 'POST':
        image = Image.open(request.files['file'])
        return serve_pil_image(image)


@app.route('/crazydots', methods=['POST','OPTIONS'])
@cross_origin()
def crazydots():
    if request.method == 'POST':
        image = Image.open(request.files['file']).convert('P')
        palettedata = [0, 0, 0, 102, 102, 102, 176, 176, 176, 255, 255, 255]
        image.putpalette(palettedata * 64)        
        return serve_pil_image(image)

@app.route('/enhancecolor', methods=['POST','OPTIONS'])
@cross_origin()
def enhancecolor():
    if request.method == 'POST':
        image = Image.open(request.files['file'])
        enhancer = ImageEnhance.Color(image)
        enhanced = enhancer.enhance(3)
        image.paste(enhanced, (0,0))
        return serve_pil_image(image)

@app.route('/blur', methods=['POST','OPTIONS'])
@cross_origin()
def blur():
    if request.method == 'POST':
        image = Image.open(request.files['file']).filter(ImageFilter.BLUR)
        return serve_pil_image(image)

if __name__ == "__main__":
        app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))