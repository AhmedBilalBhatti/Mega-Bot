# import os
# import cv2
# from djitellopy import tello
# import cvzone
# from django.conf import settings
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent

# # BASE_DIR = settings.BASE_DIR

# thres = 0.50
# nmsThres = 0.2

# # Code for webcam
# # cap = cv2.VideoCapture(0)
# # cap.set(3, 640)
# # cap.set(4, 480)

# classNames = []
# classFile = os.path.join(BASE_DIR, 'Obj_Detection', 'ss.names')
# with open(classFile, 'rt') as f:
#     classNames = f.read().split('\n')


# # print(classNames)
# configPath = Path(settings.BASE_DIR, 'Obj_Detection', 'sd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
# # configPath = os.path.join(BASE_DIR, 'Obj_Detection', 'sd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
# weightsPath = Path(settings.BASE_DIR, 'Obj_Detection', 'frozen_inference_graph.pb')
# # weightsPath = os.path.join(BASE_DIR, 'Obj_Detection', 'frozen_inference_graph.pb')

# # weightsPath = str(weightsPath)
# # configPath = str(configPath)

# # net = cv2.dnn_DetectionModel(weightsPath, configPath)
# net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
# net.setInputSize(320, 320)
# net.setInputScale(1.0 / 127.5)
# net.setInputMean((127.5, 127.5, 127.5))
# net.setInputSwapRB(True)

# me = tello.Tello()
# me.connect()
# print(me.get_battery())
# me.streamoff()
# me.streamon()


# while True:
#     img = me.get_frame_read().frame
#     classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nmsThres)
#     try:
#         for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
#             cvzone.cornerRect(img, box)
#             cv2.putText(img, f'{classNames[classId - 1].upper()} {round(conf * 100, 2)}',
#                         (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
#                         1, (0, 255, 0), 2)
#     except:
#         pass

#     # me.send_rc_control(0, 0, 0, 0)

#     cv2.imshow("Image", img)
#     cv2.waitKey(1)



import os
import cv2
from djitellopy import tello
import cvzone
from django.conf import settings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


weightsPath = os.path.join(BASE_DIR,'Obj_Detection','frozen_inference_graph.pb')
configPath = os.path.join(BASE_DIR,'Obj_Detection','ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')


thres = 0.50
nmsThres = 0.2

classNames = []
classFile = os.path.join(BASE_DIR, 'Obj_Detection', 'ss.names')
with open(classFile, 'rt') as f:
    classNames = f.read().strip().split('\n')


# net = cv2.dnn.readNetFromTensorflow(weightsPath, configPath)
net = cv2.dnn_DetectionModel(weightsPath, configPath)

net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# me = tello.Tello()
# me.connect()
# print(me.get_battery())
# me.streamoff()
# me.streamon()

# def detection():
#     while True:
#         img = me.get_frame_read().frame
#         classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nmsThres)
#         try:
#             for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
#                 cvzone.cornerRect(img, box)
#                 cv2.putText(img, f'{classNames[classId - 1].upper()} {round(conf * 100, 2)}',
#                             (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
#                             1, (0, 255, 0), 2)
#         except:
#             pass

#         cv2.imshow("Image", img)
#         cv2.waitKey(1)
