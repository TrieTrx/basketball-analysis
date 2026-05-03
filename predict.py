import cv2
import random
from ultralytics import YOLO
from video_utils import *

CONF_PLAYER_THRESHOLD = 0.4
CONF_BALL_THRESHOLD = 0.3

def getColor(cls_num) :
    random.seed(cls_num)
    return tuple(random.randint(0, 255) for _ in range(3))

model_player = YOLO('models/player.pt')
model_ball = YOLO('models/ball_detector_model.pt')
def predict(frame_lst) :
    ignore_class = ['Time Remaining', 'Shot Clock', 'Team Name', 'Period', 'Team Points', 'Ball']
    for frame in frame_lst : # Only iterate once
        results = model_player.track(frame, stream=True, persist=True)
        for result in results :
            class_names = result.names
            for box in result.boxes :
                if box.conf[0] < CONF_PLAYER_THRESHOLD:
                    continue
                cls = int(box.cls[0])
                class_name = class_names[cls]
                if class_name in ignore_class :
                    continue
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                color = getColor(cls)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, max(y1 - 10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        results = model_ball.track(frame, persist=True)
        for result in results :
            class_names = result.names
            for box in result.boxes :
                if box.conf[0] < CONF_BALL_THRESHOLD:
                    continue
                cls = int(box.cls[0])
                class_name = class_names[cls]
                if class_name != 'Ball':
                    continue
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                color = getColor(cls)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, max(y1 - 10, 20)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return frame_lst

frame_lst, fps = read_video('input-videos/video_1.mp4')
frame_lst = predict(frame_lst)
write_video(frame_lst, fps, "output.mp4")



