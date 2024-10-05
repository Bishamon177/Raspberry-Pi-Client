import io
import socket
import struct
import time
import picamera

#create client side socket object and connect to port 8000
client_socket = socket.socket()
client_socket.connect(('172.16.25.149',8000))

#makes a file like object for writing binary data
connection = client_socket.makefile('wb')

try:
    # correct orientation of camera and set resolution
    camera = picamera.PiCamera()
    camera.vflip = True
    camera.resolution = (500, 480)

    #start camera preview and wait for 2 seconds
    camera.start_preview()
    time.sleep(2)

    # records start time and makes temporary storage
    start = time.time()
    stream = io.BytesIO()

    #iterates over the stream and sends data as jpeg
    for f in camera.capture_continuous(stream, 'jpeg'):
        #returns size of image in bytes and immidiately writes to connection
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()

        #set pointer to start and send image to server as binary
        stream.seek(0)
        connection.write(stream.read())

        #for testing
        if time.time() - start > 60:
            break

        #resets stream
        stream.seek(0)
        stream.truncate()
    
    #signals End Of Stream as 0 to server
    connection.write(struct.pack('<L', 0))

#closing connection and socket
finally:
    connection.close()
    client_socket.close()


