from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import base64
import io
from PIL import Image
import numpy as np
import mediapipe as mp

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageData(BaseModel):
    image: str

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.5
)


@app.get("/")
def home():
    return {"message": "Backend is running"}


# Helper function: check if finger is open
def is_finger_open(tip, base):
    return tip["y"] < base["y"]


# Helper function: check if finger is closed
def is_finger_closed(tip, base):
    return tip["y"] > base["y"]


@app.post("/predict")
def predict(data: ImageData):
    try:
        # Remove "data:image/jpeg;base64,"
        image_data = data.image.split(",")[1]

        # Decode image
        image_bytes = base64.b64decode(image_data)

        # Convert image to RGB
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img = np.array(image)

        # Process image with MediaPipe
        results = hands.process(img)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            # Store all landmarks
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.append({
                    "x": lm.x,
                    "y": lm.y,
                    "z": lm.z
                })

            # Important points
            thumb_tip = landmarks[4]
            thumb_ip = landmarks[3]

            index_tip = landmarks[8]
            middle_tip = landmarks[12]
            ring_tip = landmarks[16]
            pinky_tip = landmarks[20]

            index_base = landmarks[5]
            middle_base = landmarks[9]
            ring_base = landmarks[13]
            pinky_base = landmarks[17]

            wrist = landmarks[0]

            # Finger states
            index_open = is_finger_open(index_tip, index_base)
            middle_open = is_finger_open(middle_tip, middle_base)
            ring_open = is_finger_open(ring_tip, ring_base)
            pinky_open = is_finger_open(pinky_tip, pinky_base)

            index_closed = is_finger_closed(index_tip, index_base)
            middle_closed = is_finger_closed(middle_tip, middle_base)
            ring_closed = is_finger_closed(ring_tip, ring_base)
            pinky_closed = is_finger_closed(pinky_tip, pinky_base)

            # ==================================================
            # 1. HELLO -> Open palm
            # ==================================================
            if (
                index_open and
                middle_open and
                ring_open and
                pinky_open
            ):
                return {"prediction": "Hello"}

            # ==================================================
            # 2. BYE -> Closed fist
            # ==================================================
            elif (
                index_closed and
                middle_closed and
                ring_closed and
                pinky_closed
            ):
                return {"prediction": "Bye"}

            # ==================================================
            # 3. YES -> Thumbs up
            # ==================================================
            elif (
                thumb_tip["y"] < thumb_ip["y"] and
                index_closed and
                middle_closed
            ):
                return {"prediction": "Yes"}

            # ==================================================
            # 4. NO -> Index finger only
            # ==================================================
            elif (
                index_open and
                middle_closed and
                ring_closed and
                pinky_closed
            ):
                return {"prediction": "No"}

            # ==================================================
            # 5. OK -> Thumb up + fingers closed
            # ==================================================
            elif (
                thumb_tip["y"] < thumb_ip["y"] and
                index_closed and
                middle_closed and
                ring_closed
            ):
                return {"prediction": "OK"}

            # ==================================================
            # 6. THANK YOU -> Open palm near mouth (approximation)
            # ==================================================
            elif (
                index_open and
                middle_open and
                ring_open and
                pinky_open and
                wrist["y"] < 0.7
            ):
                return {"prediction": "Thank You"}

            # ==================================================
            # 7. PLEASE -> Open palm
            # ==================================================
            elif (
                index_open and
                middle_open and
                ring_open and
                pinky_open
            ):
                return {"prediction": "Please"}

            # ==================================================
            # 8. SORRY -> Fist
            # ==================================================
            elif (
                index_closed and
                middle_closed and
                ring_closed and
                pinky_closed
            ):
                return {"prediction": "Sorry"}

            # ==================================================
            # 9. I LOVE YOU
            # Thumb + index + pinky open
            # ==================================================
            elif (
                index_open and
                not middle_open and
                not ring_open and
                pinky_open
            ):
                return {"prediction": "I Love You"}

            # ==================================================
            # 10. GOOD -> Open palm
            # ==================================================
            elif (
                index_open and
                middle_open and
                ring_open and
                pinky_open
            ):
                return {"prediction": "Good"}

            # ==================================================
            # 11. BAD -> Closed hand
            # ==================================================
            elif (
                index_closed and
                middle_closed and
                ring_closed and
                pinky_closed
            ):
                return {"prediction": "Bad"}

            # ==================================================
            # 12. STOP -> Open palm
            # ==================================================
            elif (
                index_open and
                middle_open and
                ring_open and
                pinky_open
            ):
                return {"prediction": "Stop"}

            # ==================================================
            # 13. PEACE -> Index + middle open
            # ==================================================
            elif (
                index_open and
                middle_open and
                ring_closed and
                pinky_closed
            ):
                return {"prediction": "Peace"}

            # ==================================================
            # 14. CALL ME
            # Thumb + pinky open
            # ==================================================
            elif (
                not index_open and
                not middle_open and
                not ring_open and
                pinky_open
            ):
                return {"prediction": "Call Me"}

            # ==================================================
            # 15. HELP
            # Thumb up
            # ==================================================
            elif (
                thumb_tip["y"] < thumb_ip["y"] and
                index_closed
            ):
                return {"prediction": "Help"}

            # ==================================================
            # Default if hand detected but gesture unknown
            # ==================================================
            else:
                return {"prediction": "Gesture Detected"}

        # No hand found
        return {"prediction": "No Hand"}

    except Exception as e:
        print("Error:", e)
        return {"prediction": f"ERROR: {str(e)}"}