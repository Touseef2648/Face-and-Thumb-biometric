import base64
import os

import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import face_recognition.face_recognize as fr
import cv2

load_dotenv()
APP_ROOT = os.getenv("APP_ROOT")
APP_VERSION = os.getenv("APP_VERSION")
CONTEXT_ROOT = APP_ROOT + APP_VERSION
# print(CONTEXT_ROOT)

app = FastAPI()


class ImagePayload(BaseModel):
    userId: int
    image: str
    oldFaceId: list


@app.post("/verify_face")
async def verify(payload: ImagePayload):
    """From_Db receives userID and encoded image in json from DB"""
    user_id = payload.userId
    oldfaceid = payload.oldFaceId
    encoded_image = payload.image
    decoded_image = base64.b64decode(encoded_image)
    with open("temp.jpg", "wb") as f:
        f.write(decoded_image)
    # img = cv2.imread("temp.jpg")
    # make embedding of the encoded image
    curr_embedding = fr.get_embeddings(["temp.jpg"])[0].tolist()
    response_item = {"verification": fr.is_match(curr_embedding, oldfaceid, 0.5)}
    return response_item


class ImagePayload2(BaseModel):
    image: str


@app.post("/get_face_id")
async def get_face_id(payload: ImagePayload2):
    """From_Db receives userID and encoded image in json from DB"""
    encoded_image = payload.image
    decoded_image = base64.b64decode(encoded_image)
    with open("temp.jpg", "wb") as f:
        f.write(decoded_image)
    # img = cv2.imread("temp.jpg")
    curr_embedding = fr.get_embeddings(["temp.jpg"])[0].tolist()
    return {"face_id": curr_embedding}


class ThumbPayload(BaseModel):
    userId: int
    image: str
    oldthumbid_descriptor: list


@app.post("/verify_fingerprint")
async def verify_fingerprint(payload: ThumbPayload):
    # Decode the base64 image
    image_data = base64.b64decode(payload.image)

    # Convert image data to numpy array
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    if image is None:
        return {"verification": False}

    # Convert the oldthumbid_descriptor to NumPy array
    old_descriptor = np.array(payload.oldthumbid_descriptor)

    # Initialize the FLANN matcher
    index_params = dict(algorithm=0, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Detect keypoints and compute descriptors using ORB
    orb = cv2.ORB_create()
    _, descriptors = orb.detectAndCompute(image, None)

    # Match descriptors using FLANN
    matches = flann.knnMatch(old_descriptor, descriptors, k=2)

    # Apply ratio test to filter good matches
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # Check if the number of good matches exceeds a predefined threshold
    min_match_count = 10
    verification_result = len(good_matches) >= min_match_count

    return {"verification": verification_result}


@app.get("/")
async def home():
    return "GTG"


@app.post("/get_finger_id")
async def get_finger_id(payload: ImagePayload2):
    # Decode the base64 image
    image_data = base64.b64decode(payload.image)

    # Convert image data to numpy array
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    if image is None:
        return {"descriptors": []}

    # Initialize the ORB feature detector and descriptor extractor
    orb = cv2.ORB_create()

    # Detect keypoints and compute descriptors
    keypoints, descriptors = orb.detectAndCompute(image, None)

    # Convert descriptors to list for JSON serialization
    descriptors_list = descriptors.tolist()

    return {"descriptors": descriptors_list}
