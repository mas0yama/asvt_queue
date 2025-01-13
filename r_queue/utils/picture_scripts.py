import cv2
from deepface import DeepFace

def is_face_on_picture(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = cv2.imread(image_path)
    if image is None:
        return False
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    return len(faces) > 0


def is_similar(paths, picture_path):
    print(paths)
    print(picture_path)
    for path in paths:
        res = DeepFace.verify(path, picture_path)
        if not res['verified']:
            continue
        return True
    return False
