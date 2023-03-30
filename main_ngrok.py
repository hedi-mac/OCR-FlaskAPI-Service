from flask import Flask, Blueprint, request
from flask_ngrok import run_with_ngrok
import cv2
import numpy as np
import services.easyocr as easyocr
import services.pytesseract as pytesseract
import services.mixedocr as mixedocr

app = Flask(__name__)
run_with_ngrok(app)
app.register_blueprint(easyocr.easyocr_service)
app.register_blueprint(pytesseract.pytesseract_service)
app.register_blueprint(mixedocr.mixedocr_service)

if __name__ == '__main__':
    app.run()
