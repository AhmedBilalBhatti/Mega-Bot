from django.shortcuts import render
from djitellopy import Tello
import cv2
import os
import time

is_recording = False
out = None

def video_stream():
    global is_recording, out
    
    tello = Tello()
    tello.connect()
    tello.streamon()

    cap = tello.get_frame_read()

    while True:
        frame = cap.frame
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        
        # Handle video recording
        if is_recording and out is not None:
            out.write(cap.frame)
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    tello.streamoff()
    tello.end()

def take_picture():
    tello = Tello()
    tello.connect()
    tello.streamon()

    frame_read = tello.get_frame_read()
    frame = frame_read.frame
    cv2.imwrite('tello_picture.jpg', frame)

    tello.streamoff()
    tello.end()

def start_recording():
    global is_recording, out
    
    tello = Tello()
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
