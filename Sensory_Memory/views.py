from django.shortcuts import render
from djitellopy import Tello
import cv2
import os
import time
import base64

is_recording = False
out = None


def Tello_Takeoff():
	try:
		tello = Tello()
		tello.connect(False)
		tello.takeoff()
	except Exception as e:
		print("Error taking off:", e)

def Tello_Land():
	try:
		tello.land()
		tello.end()
	except Exception as e:
		print("Error landing:", e)

def take_picture():
	tello.streamon()
	frame_read = tello.get_frame_read()
	frame = frame_read.frame
	cv2.imwrite('tello_picture.jpg', frame)
	tello.streamoff()


def generate_drone_frames():
    tello.streamon()
    while True:
        frame = tello.get_frame_read().frame
        _, jpeg_frame = cv2.imencode('.jpg', frame)
        base64_frame = base64.b64encode(jpeg_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + base64_frame + b'\r\n')

def drone_video_feed(request):
    return StreamingHttpResponse(generate_drone_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


def start_recording():
    global is_recording, out
    
    tello = Tello(False)
    tello.connect()
    tello.streamon()

    frame_read = tello.get_frame_read()
    frame = frame_read.frame
    
    height, width, _ = frame.shape
    out = cv2.VideoWriter('tello_video.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (width, height))

    is_recording = True

def stop_recording():
    global is_recording, out
    is_recording = False
    if out is not None:
        out.release()
        out = None


def Move_Backward(x):
	try:
		move_back(x)
	except:
		Print('Error')

def Move_Forward(x):
	try:
		move_forward(x)
	except:
		Print('Error')

def Move_Left(x):
	try:
		move_left(x)
	except:
		Print('Error')

def Move_Right(x):
	try:
		move_right(x)
	except:
		Print('Error')