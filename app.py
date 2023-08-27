import sqlite3
import hashlib
from flask import Flask, render_template, Response, jsonify, request, redirect, url_for
import cv2
import numpy as np
import face_recognition
import json


app = Flask(__name__)
# # SQLite database setup
# conn = sqlite3.connect('users.db')
# cursor = conn.cursor()
# # Create the 'users' table
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         username TEXT NOT NULL,
#         password TEXT NOT NULL
#     )
# ''')

# # username = 'admin'
# # password = 'admin123'
# # password_hash = hashlib.sha256(password.encode()).hexdigest()

# # cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password_hash))
# # conn = sqlite3.connect('users.db')
# # cursor = conn.cursor()

# conn.commit()
# conn.close()

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     username = request.form['username']
#     entered_password = request.form['password']
#     entered_password_hash = hashlib.sha256(entered_password.encode()).hexdigest()

#     cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, entered_password_hash))
#     user = cursor.fetchone()

#     if user:
#         return redirect(url_for('dashboard'))  # Redirect to dashboard upon successful login
#     else:
#         response_data = {
#             'status': 'error',
#             'message': 'Invalid credentials. Please try again.'
#         }
#         return jsonify(response_data)

# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')  # Render the dashboard template


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
        
        response_data = None  # Initialize response_data
        
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
                    'message': 'Name: {}, Gender: {}, Criminal Status: {}'.format(name, gender, criminal_status)
                }
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        if response_data:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
                   b'Content-Type: application/json\r\n\r\n' + json.dumps(response_data).encode() + b'\r\n')
        else:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            




@app.route('/recognize', methods=['GET', 'POST'])
def recognize_face():
    if request.method == 'POST':
        uploaded_file = request.files['image']
        
        # Load the known_faces data from JSON file
        with open('known_faces.json', 'r') as json_file:
            known_faces_data = json.load(json_file)

        known_faces = known_faces_data["known_faces"]

        # Load the uploaded image
        img = image.load_img(uploaded_file, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)

        face_locations = face_recognition.face_locations(img_array[0])

        response_data = None  # Initialize response_data

        if face_locations:
            face_encoding = face_recognition.face_encodings(img_array[0], face_locations)[0]
            matches = face_recognition.compare_faces([np.array(face_data["face_encoding"]) for face_data in known_faces], face_encoding)

            if any(matches):
                matched_index = matches.index(True)
                name = known_faces[matched_index]["name"]
                gender = known_faces[matched_index]["gender"]
                criminal_status = known_faces[matched_index]["criminal_status"]

                response_data = {
                    'title': 'Face Recognized',
                    'message': 'Name: {}, Gender: {}, Criminal Status: {}'.format(name, gender, criminal_status)
                }

        if response_data:
            return jsonify(response_data)
        else:
            return jsonify({'title': 'Face Not Recognized', 'message': 'No records found.'})
    
    return render_template('index.html')  # Render the upload form


# # Define your Flask routes here...



@app.route('/')
def index():
    return render_template('recognize.html')  # Updated HTML template

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)



    



