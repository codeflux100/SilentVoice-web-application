from flask import Flask, render_template, request, jsonify, redirect, flash, url_for, Response
from flask_sqlalchemy import SQLAlchemy

# --- ML IMPORTS ---
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
# ------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sign_word_database.db'
app.config['SQLALCHEMY_BINDS'] = {
    'signs': "sqlite:///sign_word_database.db",
    'contacts': "sqlite:///contact_database.db",
    'quiz': "sqlite:///quiz_database.db"
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class sign_database(db.Model):
    __bind_key__ = 'signs'
    id = db.Column(db.String(length=2), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    image_name = db.Column(db.String(length=50), nullable=False, unique=True)
    description = db.Column(db.String(length=200), nullable=False)
    
    def __repr__(self):
        return f"<SignDatabase {self.name}>"
    
class contact_database(db.Model):
    __bind_key__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<ContactDatabase {self.name}>"

class quiz_database(db.Model):
    __bind_key__ = 'quiz'
    id = db.Column(db.Integer)
    image_name = db.Column(db.String(50), primary_key=True)
    option_1 = db.Column(db.String(50), nullable=False)
    option_2 = db.Column(db.String(50), nullable=False)
    option_3 = db.Column(db.String(50), nullable=False)
    option_4 = db.Column(db.String(50), nullable=False)
    correct_answer = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return f"<ContactDatabase {self.name}>"

# --- ML MODEL INITIALIZATION ---
# Initialize cap as None globally so we can control it later
cap = None 
detector = HandDetector(maxHands=1)

# NOTE: Ensure these paths are 100% correct on your system
try:
    classifier = Classifier("C:/Users/acer/Desktop/converted_keras1/keras_model.h5", 
                            "C:/Users/acer/Desktop/converted_keras1/labels.txt")
    print("ML Model Loaded Successfully!")
except Exception as e:
    print(f"Error loading ML Model: {e}")

offset = 20
imgSize = 300
labels = ["Hello", "I Love You", "No", "Okay", "Please", "Thank You", "Yes"]
offset = 20
imgSize = 300
labels = ["Hello", "I Love You", "No", "Okay", "Please", "Thank You", "Yes"]

def generate_frames():
    """
    This function captures frames, runs the ML prediction, 
    and yields them as a video stream for the browser.
    """
    while True:
        success, img = cap.read()
        if not success:
            break
        
        imgOutput = img.copy()
        hands, img = detector.findHands(img)
        
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            
            # Clip values to ensure we don't crash if hand is at edge of screen
            y1, y2 = max(0, y - offset), min(img.shape[0], y + h + offset)
            x1, x2 = max(0, x - offset), min(img.shape[1], x + w + offset)
            
            imgCrop = img[y1:y2, x1:x2]

            if imgCrop.size == 0:
                continue

            aspectRatio = h / w

            try:
                # --- Your Resizing Logic ---
                if aspectRatio > 1:
                    k = imgSize / h
                    wCal = math.ceil(k * w)
                    imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                    wGap = math.ceil((imgSize - wCal) / 2)
                    imgWhite[:, wGap:wCal + wGap] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)
                else:
                    k = imgSize / w
                    hCal = math.ceil(k * h)
                    imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                    hGap = math.ceil((imgSize - hCal) / 2)
                    imgWhite[hGap:hCal + hGap, :] = imgResize
                    prediction, index = classifier.getPrediction(imgWhite, draw=False)

                # --- Draw UI ---
                cv2.rectangle(imgOutput, (x - offset, y - offset - 50), (x - offset + 90, y - offset - 50 + 50), (0, 255, 0), cv2.FILLED)
                cv2.putText(imgOutput, labels[index], (x, y - 26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
                cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (0, 255, 0), 4)
            
            except Exception as e:
                # If resizing fails momentarily, just skip drawing
                pass

        # --- Encode for Web ---
        ret, buffer = cv2.imencode('.jpg', imgOutput)
        frame = buffer.tobytes()
        
        # Multipart streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# --- ROUTES ---

@app.route('/video_feed')
def video_feed():
    """Route that streams the video frames"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# --- ADDED ROUTE TO SHUTDOWN CAMERA ---
@app.route('/release_camera')
def release_camera():
    global cap
    if cap.isOpened():
        cap.release()
        print("Camera released successfully.")
        return jsonify({"status": "success", "message": "Camera released"})
    return jsonify({"status": "error", "message": "Camera was already closed"})
# ---------------------------------------

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    new_contact = contact_database(name=name, email=email)
    db.session.add(new_contact)
    db.session.commit()
    return redirect('/home_page')

@app.route('/')
@app.route('/home_page')
def home_page():
    return render_template('Home_page.html')

@app.route('/main_page')
def main_page():
    return render_template('Main_page.html')

@app.route('/learn_page')
def learn_page():
    return render_template('learn_page.html')

@app.route('/translate_page')
def translate_page():
    global cap
    # Check if the camera is off (because it was released)
    if cap is None or not cap.isOpened():
        print("Reinitializing Camera...")
        cap = cv2.VideoCapture(0) # Reopen the camera!
    
    # Render the page which requests the video stream
    return render_template('Translate_page.html')

@app.route('/sign_name/<name>')
def sign_name_page(name):
    return render_template('sign_word.html', name=name)

@app.route("/api/signs")
def database():
    all_signs = sign_database.query.all()
    data = [
        {
            "id": sign.id,
            "name": sign.name,
            "image": sign.image_name,
            "description": sign.description
        }
        for sign in all_signs
    ]
    return jsonify(data)

@app.route("/api/quiz")
def question_database():
    quiz_option = quiz_database.query.all()
    data = [
        {
            "image_name": quiz.image_name,
            "option_1": quiz.option_1,
            "option_2": quiz.option_2,
            "option_3": quiz.option_3,
            "option_4": quiz.option_4,
            "correct_answer": quiz.correct_answer
        }
        for quiz in quiz_option
    ]
    return jsonify(data)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)