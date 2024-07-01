from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.http import StreamingHttpResponse
from datetime import datetime, timedelta
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


def warmup(para=None):
    tello = Tello()
    try:
        tello.connect()
        tello.turn_motor_on()
        if para:
            time.sleep(para)
        else:
            time.sleep(15)
        tello.turn_motor_off()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        tello.end()









def fetch_drone_data(tello):
    tello = Tello()
    tello.connect()
    def query_temperature(tello):
        response = tello.send_read_command('temp?')
        return response

    def query_barometer(tello):
        response = tello.send_read_command('baro?')
        return response

    def query_attitude(tello):
        response = tello.send_read_command('attitude?')
        return response

    def query_speed(tello):
        response = tello.send_read_command('speed?')
        return response

    def query_height(tello):
        response = tello.send_read_command('height?')
        return response

    def query_flight_time(tello):
        response = tello.get_flight_time()
        return response

    def query_distance_tof(tello):
        response = tello.get_distance_tof()
        return response

    temperature_range = query_temperature(tello)
    battery = tello.query_battery()
    barometer = query_barometer(tello)
    attitude = query_attitude(tello)
    speed = query_speed(tello)
    height = query_height(tello)
    flight_time = query_flight_time(tello)
    distance_tof = query_distance_tof(tello)

    temperatures = temperature_range.replace('C', '').split('~')
    lowest_temp = min(int(temperatures[0]), int(temperatures[1]))
    highest_temp = max(int(temperatures[0]), int(temperatures[1]))

    return {'temperature_range': temperature_range,'lowest_temperature': lowest_temp,'highest_temperature': highest_temp,'battery': battery,
            'barometer': barometer,'attitude': attitude,'speed': speed,'height': height,'flight_time':flight_time,'distance_tof': distance_tof}


















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

def create_parts(text_node,session,parts):
    part_u = CommandPart(part=parts).save()
    text_node.text_part.connect(part_u)

def get_command(message,session):
    if message and session:
        text_node = CommandText(sentence = message).save()
        n = TextSensor.nodes.filter(uid=session).first()
        n.text_sense.connect(text_node)
        splitted = message.split()
        for i in splitted:
            create_parts(text_node,session,i)

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


def update_sensor(request):
    session = request.session.get('user_id')    
    drone_data = fetch_drone_data(tello)
    agent = Sensor.nodes.get(uid = session,name='DJI-TELLO')
    existing_flights_count=""
    try:
        existing_flights_count = Sense.nodes.filter(sense_name__startswith="FLIGHT").count()
    except:
        existing_flights_count = 0

    flight_number = existing_flights_count + 1

    sensor_node = ""
    try:   
        sensor_node = Sense.nodes.filter(created_at__gte=datetime.now() - timedelta(minutes=15)).order_by('-created_at').first()
        sensor_node.updated_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sensor_node.save()
    except:
        sensor_node = Sense()
        

    sensor_node.sense_name = f"FLIGHT {flight_number}"
    sensor_node.temperature_range = f"{drone_data['temperature_range']}°C"
    sensor_node.lowest_temperature = f"{drone_data['lowest_temperature']}°C"
    sensor_node.highest_temperature = f"{drone_data['highest_temperature']}°C"
    sensor_node.battery = f"{drone_data['battery']}%"
    sensor_node.barometer = f"{drone_data['barometer']} mbar"
    sensor_node.attitude = f"{drone_data['attitude']}"
    sensor_node.speed = f"{drone_data['speed']} cm/s"
    sensor_node.height = f"{drone_data['height']}"
    sensor_node.flight_time = f"{drone_data['flight_time']} seconds"
    sensor_node.distance_tof = f"{drone_data['distance_tof']} cm" 
    sensor_node.save()

    agent.sense.connect(sensor_node)

        



def generate_video_frames(request):
    check_for = get_current_wifi_name()
    if check_for:
        from Memory.views import make_sensory_and_link
        make_sensory_and_link(request)
        update_sensor(request)
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