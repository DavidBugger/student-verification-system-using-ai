import face_recognition
import os
import json

# Path to your dataset folder
dataset_folder = 'images'

known_faces = []

for root, dirs, files in os.walk(dataset_folder):
    for dir_name in dirs:
        person_folder = os.path.join(root, dir_name)
        images = [img for img in os.listdir(person_folder) if img.endswith('.jpg')]
        if images:
            face_encodings = []
            for img in images:
                img_path = os.path.join(person_folder, img)
                image = face_recognition.load_image_file(img_path)
                face_encoding = face_recognition.face_encodings(image)
                
                # Check if a face was found in the image
                if len(face_encoding) > 0:
                    # Store the first detected face encoding
                    face_encodings.append(face_encoding[0].tolist())
            
            if face_encodings:
                face_data = {
                    "name": dir_name,
                    "gender": "Male",  # Replace with actual gender data
                    "criminal_status": "No",  # Replace with actual criminal status
                    "face_encoding": face_encodings
                }
                known_faces.append(face_data)

# Save known_faces to JSON file
data = {"known_faces": known_faces}
with open('known_faces.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)
