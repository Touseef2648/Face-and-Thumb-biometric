import base64
from main import app, get_face_id, verify
from pydantic import BaseModel

with open("/home/touseef/PycharmProjects/Joyn-Biometric-main/test/self4.jpg", "rb") as image_file:
    image_data = image_file.read()


class FaceItem(BaseModel):
    uid: int
    name: str
    image: str
    face_id: list


def test_get_faceid():
    face_item = FaceItem(uid=64, name="Touseef", image=base64.b64encode(image_data).decode(), face_id=[])
    response1 = get_face_id(face_item)
    print("return of getface-ID = ", response1)
    print("Test Get face ID")


def test_verify_via_faceid():
    # Sample input data
    item = {
        "curr_face_id": [0.1, 0.2, 0.3],
        "prev_face_id": [0.4, 0.5, 0.6]
    }
    response2 = verify(item)
    print("return of Verify-VIA-faceID = ", response2)
    print("test Verify face ID")


test_get_faceid()
test_verify_via_faceid()
