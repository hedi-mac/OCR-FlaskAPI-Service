from flask import Blueprint, request, jsonify
from constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
import cv2
import numpy as np
import os
import easyocr 
from pytesseract import pytesseract, image_to_data, Output

pytesseract.tesseract_cmd = r'D:\00__WORK__ZONE\PFE\Tesseract-OCR\tesseract.exe'
config = "--psm 11 --oem 3"
lang = "eng+fr"

def ocr_img_pytessercat(image):
    img_data = image_to_data(
        image,
        lang = lang,
        config = config,
        output_type = Output.DATAFRAME
    )
    img_conf_text = img_data[["conf", "text"]]
    return img_conf_text[img_conf_text["text"].notnull()]["text"].values.tolist() 

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
reader = easyocr.Reader(['en', 'fr'], gpu=True)

def ocr_img_easyocr(image):
    return [text for bbox, text, conf in reader.readtext(image) if text is not None]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}


mixedocr_service = Blueprint("mixedocr_service", __name__, url_prefix="/ocr")

@mixedocr_service.route('/mixedocr', methods=['POST'])
def upload():
    file = request.files['file']
    # check if the file is actually an image
    if file and allowed_file(file.filename):
        # read the image file
        img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        t = ocr_img_easyocr(img)
        t.extend(ocr_img_pytessercat(img))
        # do something with the image data
        return jsonify({'data': t}), HTTP_200_OK
    else:
        return jsonify({
                'error': 'Enter a valid file format'
        }), HTTP_400_BAD_REQUEST