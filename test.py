import cv2
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

im = picam2.capture_array()

cv2.imwrite("image.jpg", im)
print("image saved successfully")
