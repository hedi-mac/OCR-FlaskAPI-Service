from flask import Blueprint, request, jsonify
from constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST
import cv2
import numpy as np
import os
import easyocr 

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
reader = easyocr.Reader(['en', 'fr'], gpu=True)

def ocr_img(image):
    return [text for bbox, text, conf in reader.readtext(image) if text is not None]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}


easyocr_service = Blueprint("easyocr_service", __name__, url_prefix="/ocr")

@easyocr_service.route('/easyocr', methods=['POST'])
def upload():
    file = request.files['file']
    # check if the file is actually an image
    if file and allowed_file(file.filename):
        # read the image file
        img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        t = ocr_img(img)
        # do something with the image data
        return jsonify({'data': t}), HTTP_200_OK
    else:
        return jsonify({
                'error': 'Enter a valid file format'
        }), HTTP_400_BAD_REQUEST