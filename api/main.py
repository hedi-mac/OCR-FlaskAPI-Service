from flask import Flask,request
import pandas as pd
import cv2
import easyocr 
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
	return "HELLO from vercel use flask"

@app.route('/example', methods=['POST'])
def example():
    if request.method == 'POST':
        data = request.form['data']
        print(data)
        return f"The data you sent is: {data}"

@app.route("/about")
def about():
	return "HELLO test"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}


def easyocr_img(image):
    reader = easyocr.Reader(['en', 'fr'], gpu=True)
    result = reader.readtext(image)
    img_conf_text = pd.DataFrame(result, columns=['bbox','text','conf'])
    valid_text = img_conf_text[img_conf_text["text"].notnull()]   
    return valid_text['text']

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    # check if the file is actually an image
    if file and allowed_file(file.filename):
        # read the image file
        img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        t = easyocr_img(img)
        # do something with the image data
        return t.to_json(orient='records')
    else:
        return 'Invalid file'

if __name__ == '__main__':
    app.run()