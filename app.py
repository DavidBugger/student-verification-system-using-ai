from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import hashlib

# ... Other code ...

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = hashlib.sha256(request.form['password'].encode()).hexdigest()
    
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    
    if user:
        response_data = {
            'status': 'success',
            'message': 'Login Successful!'
        }
    else:
        response_data = {
            'status': 'error',
            'message': 'Invalid credentials. Please try again.'
        }
    
    return jsonify(response_data)


from flask import Flask, render_template, Response, jsonify
import cv2
import numpy as np
import face_recognition
import json

app = Flask(__name__)

# Load the known_faces data from JSON file
with open('known_faces.json', 'r') as json_file:
    known_faces_data = json.load(json_file)

known_faces = known_faces_data["known_faces"]

camera = cv2.VideoCapture(0)

def gen_frames():
    while True:
        success, frame = camera.read()  # Read a frame from the camera
        
        if not success:
            break
        
        # Convert the frame to RGB for face recognition
        rgb_frame = frame[:, :, ::-1]
        
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if face_locations:
            face_encoding = face_recognition.face_encodings(rgb_frame, face_locations)[0]
            matches = face_recognition.compare_faces([np.array(face_data["face_encoding"]) for face_data in known_faces], face_encoding)
            
            if any(matches):
                matched_index = matches.index(True)
                name = known_faces[matched_index]["name"]
                gender = known_faces[matched_index]["gender"]
                criminal_status = known_faces[matched_index]["criminal_status"]
                
                response_data = {
                    'title': 'Face Recognized',
                    'message': f'Name: {name}, Gender: {gender}, Criminal Status: {criminal_status}'
                }
                return jsonify(response_data)  # Return response in JSON format
                
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Add content-type header

@app.route('/')
def index():
    return render_template('index.html')  # Updated HTML template

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
    



