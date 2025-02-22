import cv2
import numpy as np
from ultralytics import YOLO
from yolo_segmentation import YOLOSegmentation

from roboflow import Roboflow
rf = Roboflow(api_key="0orvzcC4ruCS4pZCHTZR")
project = rf.workspace().project("football-team-separation")
model = project.version(15).model

cap = cv2.VideoCapture('./data/pen.mp4')

model = YOLO("yolov8m.pt")
yolo_seg = YOLOSegmentation("yolov8m-seg.pt")

# identifies most average color
def get_average_color(a):
    return tuple(np.array(a).mean(axis=0).mean(axis=0).round().astype(int))

# identifies most common color
def unique_count_app(a):
    colors, count = np.unique(a.reshape(-1,a.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()]


while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame2 = np.array(frame)

    bboxes, classes, segmentations, socres = yolo_seg.detect(frame)

    # results = model(frame, device="mps")
    # result = results[0]
    # bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
    # classes = np.array(result.boxes.cls.cpu(), dtype="int")
    for cls, bbox in zip(classes, bboxes):
        if cls == 0:    
            (x, y, x2, y2) = bbox
            cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 225), 2)
            cv2.putText(frame, "Player", (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 225), 2)
        if cls == 32:
            (x, y, x2, y2) = bbox
            cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 225), 2)
            cv2.putText(frame, "Ball", (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 225), 2)

    cv2.imshow("Img", frame)

    key = cv2.waitKey(1)
    if key == 27 or cv2.getWindowProperty("Img", cv2.WND_PROP_VISIBLE) < 1:
        break

        
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(0)