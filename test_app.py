from flask import Flask, request, jsonify, render_template
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import face_recognition
import json

app = Flask(__name__)

# Load the trained face recognition model
face_recognition_model = load_model('face_recognition_model.h5')

# Load known faces data from JSON file
with open('known_faces.json', 'r') as json_file:
    known_faces_data = json.load(json_file)

known_faces = known_faces_data["known_faces"]

@app.route('/')
def index():
    return render_template('index.html')  # Basic HTML form for image upload

@app.route('/recognize', methods=['POST'])
def recognize():
    uploaded_file = request.files['image']
    
    # Load the uploaded image
    img = image.load_img(uploaded_file, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    # Perform face recognition
    face_locations = face_recognition.face_locations(img_array[0])
    
    if len(face_locations) == 0:
        return jsonify({'message': 'No face detected'})
    
    face_encoding = face_recognition.face_encodings(img_array[0], face_locations)[0]
    
    # Compare the face encoding with known face encodings
    matches = face_recognition.compare_faces([face_data["face_encoding"] for face_data in known_faces], face_encoding)
    
    if any(matches):
        matched_index = matches.index(True)
        name = known_faces[matched_index]["name"]
        gender = known_faces[matched_index]["gender"]
        criminal_status = known_faces[matched_index]["criminal_status"]
        
        return jsonify({
            'name': name,
            'gender': gender,
            'criminal_status': criminal_status
        })
    else:
        return jsonify({'message': 'Face not recognized'})

if __name__ == '__main__':
    app.run()
