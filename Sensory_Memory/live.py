from djitellopy import tello
import cv2

from django.http import StreamingHttpResponse
import cv2

def video_feed(request):
    def generate():
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

    return StreamingHttpResponse(generate(), content_type="multipart/x-mixed-replace;boundary=frame")
