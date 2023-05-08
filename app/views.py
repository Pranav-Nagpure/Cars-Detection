import os
import cv2
import numpy as np
from app import app
from PIL import Image
from flask import render_template, request

app.config['GENERATED_FILE'] = 'app/static/generated'


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        # Get Uploaded Image
        file = request.files['file_upload']
        img = Image.open(file)
        img = np.array(img)

        # Preprocess Image
        img_processed = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img_processed = cv2.GaussianBlur(img_processed, (5, 5), 0)
        img_processed = cv2.dilate(img_processed, np.ones((3, 3)))

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        img_processed = cv2.morphologyEx(img_processed, cv2.MORPH_CLOSE, kernel)

        # Detect Cars with cascade
        cascade = cv2.CascadeClassifier('app/static/cascade/cars.xml')
        cars = cascade.detectMultiScale(img_processed, 1.1, 1)

        # Drawing Rectangles in original image
        for (x, y, w, h) in cars:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Return results
        img = Image.fromarray(img)
        filepath = os.path.join(app.config['GENERATED_FILE'], 'image.jpg')
        img.save(filepath)
        return render_template('index.html', result_img='static/generated/image.jpg', result_count=f'{len(cars)} Cars Detected')
