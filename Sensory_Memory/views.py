from django.shortcuts import render
from djitellopy import Tello
import cv2
import os
import time
from django.http import StreamingHttpResponse
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


def generate_video_frames():
    tello = Tello()
    tello.connect()
    tello.streamon()
    
    try:
        while True:
            frame = tello.get_frame_read().frame
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
    except KeyboardInterrupt:
        tello.streamoff()
        tello.land()
        tello.end()
        exit(1)


def drone_video_feed(request):
    return StreamingHttpResponse(generate_video_frames(), content_type='multipart/x-mixed-replace; boundary=frame')





		

def take_picture():
	tello.streamon()
	frame_read = tello.get_frame_read()
	frame = frame_read.frame
	cv2.imwrite('tello_picture.jpg', frame)
	tello.streamoff()






# def start_recording():
#     global is_recording, out
    
#     tello = Tello(False)
#     tello.connect()
#     tello.streamon()

#     frame_read = tello.get_frame_read()
#     frame = frame_read.frame
    
#     height, width, _ = frame.shape
#     out = cv2.VideoWriter('tello_video.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (width, height))

#     is_recording = True

# def stop_recording():
#     global is_recording, out
#     is_recording = False
#     if out is not None:
#         out.release()
#         out = None


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