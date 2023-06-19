from flask import Flask, request, jsonify, render_template, redirect
import numpy as np
from PIL import Image
import cv2 as cv
from tensorflow import keras
import os
from gtts import gTTS

import uuid

app = Flask(__name__)

# Load the model
model = keras.models.load_model('Model_fullData_32bs_50epochs_64x64.h5')

def aslr(img, model):
    label_dict = {0: 'عين', 1: 'ال', 2: 'ألف', 3: 'باء', 4: 'ضاض', 5: 'دال', 6: 'فاء', 7: 'غين', 8: 'حاء', 9: 'هاء', 10: 'جيم', 11: 'كاف', 12: 'خاء', 13: 'لا', 14: 'لام', 15: 'ميم', 16: 'نون', 17: 'قاف', 18: 'راء', 19: 'Sad', 20: 'سين', 21: 'شين', 22: 'طاء', 23: 'تاء', 24: 'تاء مربوطة', 25: 'ذال', 26: 'ثاء', 27: 'واو', 28: 'ياء', 29: 'زاي', 30: 'زين'}


    # Resize the input image to match the expected input shape of the model
    img = cv.resize(img, (64, 64))
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = np.expand_dims(img, axis=0)
    img = np.expand_dims(img, axis=3)
    img = img.astype('float32') / 255.0

    # Make predictions using the model
    prediction = model.predict(img)
    predicted_label = np.argmax(prediction)

    # Get the predicted label
    predicted_label = label_dict[predicted_label]

    return predicted_label

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/home', methods=['GET'])
def go_home():
    return redirect('/')

@app.route('/samples')
def samples():
    return render_template('samples.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Check if an image file was provided in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'})

    image = request.files['image']

    # Load the image using PIL (Pillow)
    img = Image.open(image)
    img = np.array(img)

    # Perform ASLR prediction
    predicted_label = aslr(img, model)

    return jsonify({'prediction': predicted_label})

@app.route('/generate_audio', methods=['POST'])
def generate_audio():
    # Check if text was provided in the request
    if 'text' not in request.json:
        return jsonify({'error': 'No text provided'})

    text = request.json['text']

    try:
        # Generate a unique filename for this request to prevent caching issues
        unique_filename = str(uuid.uuid4()) + '.mp3'
        audio_file_path = os.path.join('static', unique_filename)

        # Generate the audio using gTTS
        tts = gTTS(text=text, lang='ar')
        tts.save(audio_file_path)
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to generate audio'})

    # Return the audio file path
    audio_url = f"{request.host_url}{audio_file_path}"
    return jsonify({'audio_url': audio_url})

if __name__ == '__main__':
    app.run(debug=True)
