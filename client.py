import socketio
import cv2
from picamera2 import Picamera2
import base64
import time

# Create a Socket.IO client
sio = socketio.Client()


@sio.event
def connect():
    print("Connected to server")


@sio.event
def disconnect():
    print("Disconnected from server")


@sio.event
def connect_error(data):
    print("Connection failed:", data)


def send_video():
    uri = "http://192.168.6.74:8000"
    sio.connect(uri)

    picam2 = Picamera2()
    picam2.configure(
        picam2.create_preview_configuration(
            main={"format": "RGB888", "size": (640, 480)}
        )
    )
    picam2.start()

    while True:
        # Capture a frame
        im = picam2.capture_array()
        im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

        # Encode the frame as JPEG
        _, buffer = cv2.imencode(".jpg", im)
        jpg_encoded = base64.b64encode(buffer).decode("utf-8")

        # Send the frame over Socket.IO
        sio.emit("video_frame", jpg_encoded)
        time.sleep(0.5)

    picam2.stop()
    sio.disconnect()


# Run the video sending function
send_video()
