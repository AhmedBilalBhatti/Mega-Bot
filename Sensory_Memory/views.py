from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import StreamingHttpResponse
from djitellopy import Tello
from .object_detect import *
from Memory.models import *
import cv2
import os
import time
import base64
import logging
import pywifi
from pywifi import PyWiFi, const



is_recording = False
out = None

def get_current_wifi_name():
    wifi = PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(2)
    scan_results = iface.scan_results()
    for network in scan_results:
        if network.ssid == "DJI-TELLO":
            return True
    return False


logging.basicConfig(level=logging.INFO)


def Tello_Takeoff():
	try:
		tello = Tello()
		tello.connect()
		tello.takeoff()
	except Exception as e:
		print("Error taking off:", e)

def Tello_Land():
	try:
		tello.land()
		tello.end()
	except Exception as e:
		print("Error landing:", e)


# def generate_video_frames():
#     tello = Tello()
#     tello.connect()
#     tello.streamon()
    
#     try:
#         while True:
#             frame = tello.get_frame_read().frame
#             _, jpeg = cv2.imencode('.jpg', frame)
#             yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
#     except KeyboardInterrupt:
#         tello.streamoff()
#         tello.land()
#         tello.end()
#         exit(1)


# def drone_video_feed(request):
#     return StreamingHttpResponse(generate_video_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


# def generate_video_frames():
#     tello = Tello()
#     tello.connect()
#     tello.streamon()

#     try:
#         while True:
#             frame_read = tello.get_frame_read()
#             if frame_read.stopped:
#                 tello.streamoff()
#                 tello.end()
#                 break
            
#             frame = frame_read.frame
#             if frame is not None:
#                 _, jpeg = cv2.imencode('.jpg', frame)
#                 yield (b'--frame\r\n'
#                        b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
#             else:
#                 logging.error("Frame is None")
#                 continue
            
#             time.sleep(0.1)  # Sleep to prevent high CPU usage
#     except Exception as e:
#         logging.error(f"Error during video stream handling: {e}")
#     finally:
#         tello.streamoff()
#         tello.end()

def get_command(message):
    return message

def make_sensory_and_link(request):
    session = request.session.get('user_id')
    user = Signups.nodes.filter(uid=session).first()
    try:
        sensor_node = SensoryMemory.nodes.get(uid = session,name='Sensor')
    except:
        sensor_node = SensoryMemory(uid = session,name='Sensor').save()
        user.sense.connect(sensor_node)

    try:
        text_node = TextSensor.nodes.get(uid = session,name='Text Sensor')
    except:
        text_node = TextSensor(uid = session,name='Text Sensor').save()
        sensor_node.textsense.connect(text_node)

    try:
        agent = Sensor.nodes.get(uid = session,name='DJI-TELLO')
    except:
        agent = Sensor(uid = session,name='DJI-TELLO').save()
        sensor_node.sensor.connect(agent)




def generate_video_frames(request):
    check_for =True
    if check_for:
        from Memory.views import make_sensory_and_link
        make_sensory_and_link(request)
        tello = Tello()
        tello.connect()
        tello.streamon()

        try:
            while True:
                frame_read = tello.get_frame_read()
                if frame_read.stopped:
                    tello.streamoff()
                    tello.end()
                    break
                
                frame = frame_read.frame
                if frame is not None:
                    # Object detection logic
                    classIds, confs, bbox = net.detect(frame, confThreshold=thres, nmsThreshold=nmsThres)
                    try:
                        for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
                            cvzone.cornerRect(frame, box)
                            cv2.putText(frame, f'{classNames[classId - 1].upper()} {round(conf * 100, 2)}',
                                        (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                        1, (0, 255, 0), 2)
                    except Exception as e:
                        logging.error(f"Error during object detection: {e}")

                    _, jpeg = cv2.imencode('.jpg', frame)
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
                else:
                    logging.error("Frame is None")
                    continue
                
                time.sleep(0.1)  
        except Exception as e:
            logging.error(f"Error during video stream handling: {e}")
        finally:
            tello.streamoff()
            tello.end()

@require_GET
def drone_video_feed(request):
    return StreamingHttpResponse(generate_video_frames(request), content_type='multipart/x-mixed-replace; boundary=frame')








# def generate_video_frames():
#     tello = Tello()
#     try:
#         tello.connect()
#         tello.streamon()

    
#         while True:
#             frame_read = tello.get_frame_read()
#             if frame_read.stopped:
#                 tello.streamoff()
#                 tello.end()
#                 break
            
#             frame = frame_read.frame
#             if frame is not None:
#                 # Object detection logic
#                 classIds, confs, bbox = net.detect(frame, confThreshold=thres, nmsThreshold=nmsThres)
#                 try:
#                     for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
#                         cvzone.cornerRect(frame, box)
#                         cv2.putText(frame, f'{classNames[classId - 1].upper()} {round(conf * 100, 2)}',
#                                     (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
#                                     1, (0, 255, 0), 2)
#                 except Exception as e:
#                     logging.error(f"Error during object detection: {e}")

#                 _, jpeg = cv2.imencode('.jpg', frame)
#                 yield (b'--frame\r\n'
#                        b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
#             else:
#                 logging.error("Frame is None")
#                 continue
            
#             time.sleep(0.1)  
#     except Exception as e:
#         logging.error(f"Error during video stream handling: {e}")
#     # finally:
#     #     tello.streamoff()
#     #     tello.end()

# @require_GET
# def drone_video_feed(request):
#     return StreamingHttpResponse(generate_video_frames(), content_type='multipart/x-mixed-replace; boundary=frame')










def take_picture(request):
    try:
        # Connect to Tello and start video stream
        tello.connect()
        tello.streamon()

        # Capture frame from the video stream
        frame_read = tello.get_frame_read()
        frame = frame_read.frame

        if frame is not None:
            # Save image to 'static' folder (ensure 'static' folder exists in your project)
            file_path = os.path.join(settings.BASE_DIR, 'static', 'tello_picture.jpg')
            cv2.imwrite(file_path, frame)

            # Convert image to base64 (optional)
            with open(file_path, 'rb') as img_file:
                img_str = base64.b64encode(img_file.read()).decode('utf-8')

            return JsonResponse({'status': 'success', 'image': img_str})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to capture frame from drone'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    finally:
        # Clean up: Stop video stream and disconnect from Tello
        tello.streamoff()
        tello.end()

        
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