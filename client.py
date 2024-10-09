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


def send_video():
    uri = "http://192.168.6.74:8000"  # Replace with your server's IP address
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

        # Convert to black and white
        # gray_frame = cv2.cvtColor(im, cv2.COLOR_XRGB2GRAY)

        # Encode the frame as JPEG
        _, buffer = cv2.imencode(".jpg", gray_frame)
        jpg_as_text = base64.b64encode(buffer).decode("utf-8")

        # Send the frame over Socket.IO
        sio.emit("video_frame", jpg_as_text)
        time.sleep(1)

    picam2.stop()
    sio.disconnect()


# Run the video sending function
send_video()
# import cv2
# from picamera2 import Picamera2
#
# picam2 = Picamera2()
# picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
# picam2.start()
#
# im = picam2.capture_array()
#
# cv2.imwrite("image.jpg", im)
# print("image saved successfully")
# import io
# import socket
# import struct
# import time
# import picamera
#
# #create client side socket object and connect to port 8000
# client_socket = socket.socket()
# client_socket.connect(('172.16.25.149',8000))
#
# #makes a file like object for writing binary data
# connection = client_socket.makefile('wb')
#
# try:
#     # correct orientation of camera and set resolution
#     camera = picamera.PiCamera()
#     camera.vflip = True
#     camera.resolution = (500, 480)
#
#     #start camera preview and wait for 2 seconds
#     camera.start_preview()
#     time.sleep(2)
#
#     # records start time and makes temporary storage
#     start = time.time()
#     stream = io.BytesIO()
#
#     #iterates over the stream and sends data as jpeg
#     for f in camera.capture_continuous(stream, 'jpeg'):
#         #returns size of image in bytes and immidiately writes to connection
#         connection.write(struct.pack('<L', stream.tell()))
#         connection.flush()
#
#         #set pointer to start and send image to server as binary
#         stream.seek(0)
#         connection.write(stream.read())
#
#         #for testing
#         if time.time() - start > 60:
#             break
#
#         #resets stream
#         stream.seek(0)
#         stream.truncate()
#
#     #signals End Of Stream as 0 to server
#     connection.write(struct.pack('<L', 0))
#
# #closing connection and socket
# finally:
#     connection.close()
#     client_socket.close()
#
#
