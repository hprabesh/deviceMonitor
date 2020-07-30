import os
import cv2
from base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Camera NotFound')
        face_cascade=cv2.CascadeClassifier("C:\\ProgramData\\Anaconda3\\Lib\\site-packages\\cv2\data\\haarcascade_frontalface_default.xml")
        eye_cascade=cv2.CascadeClassifier("C:\\ProgramData\\Anaconda3\\Lib\\site-packages\\cv2\\data\\haarcascade_eye_tree_eyeglasses.xml")
        while True:
            # read frame by frame
            _, img = camera.read()
            img=cv2.resize(img,(int(img.shape[1]),int(img.shape[0])))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces=face_cascade.detectMultiScale(gray,scaleFactor=1.05,minNeighbors=5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                roi_gray=gray[y:y+h,x:x+w]
                roi_color=img[y:y+h,x:x+w]
                eyes=eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(255,0,0),3)
            resized=cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2)))
            cv2.imshow('img', resized)
            #convert to jpg image file 
            yield cv2.imencode('.jpg', img)[1].tobytes()
