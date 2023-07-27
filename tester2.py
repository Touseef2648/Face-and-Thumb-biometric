import base64
import requests

# Define the API endpoint URLs
verify_url = "http://localhost:8000/verify_face"
get_face_id_url = "http://localhost:8000/get_face_id"

# Helper function to read an image file and encode it as base64
def encode_image(image_path):
    with open(image_path, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode("utf-8")
    return encoded_image


# Test the /verify_face endpoint
def test_verify_face():
    image_path = "/home/touseef/PycharmProjects/Joyn-Biometric-main/test/self5.jpg"
    encoded_image = encode_image(image_path)

    payload = {
        "userId": 123,
        "image": encoded_image,
        "oldFaceId": old_face_id
    }

    response = requests.post(verify_url, json=payload)
    response_json = response.json()
    print(response_json)


# Test the /get_face_id endpoint
def test_get_face_id():
    image_path = "/home/touseef/PycharmProjects/Joyn-Biometric-main/test/self7.jpg"
    encoded_image = encode_image(image_path)

    payload = {
        "image": encoded_image
    }

    response = requests.post(get_face_id_url, json=payload)
    response_json = response.json()
    return response_json

# Run the tests
old_face_id = test_get_face_id()["face_id"]
test_verify_face()