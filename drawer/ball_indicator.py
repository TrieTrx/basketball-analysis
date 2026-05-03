import cv2
import numpy as np

def draw_rectangle(frame, ball) :
    x1, y1, x2, y2 = map(int, ball["box"])
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return frame

def draw_triangle(frame, ball):
    x1, y1, x2, y2 = map(int, ball["box"])
    
    mid_x = (x1 + x2) // 2
    
    triangle_size = 10
    tip = (mid_x, y1 - 5)
    left = (mid_x - triangle_size, y1 - 5 - triangle_size * 2)
    right = (mid_x + triangle_size, y1 - 5 - triangle_size * 2)
    
    points = np.array([tip, left, right], np.int32)
    
    cv2.drawContours(frame, [points], 0, (0, 255, 0), -1)
    cv2.drawContours(frame, [points], 0, (0, 0, 0), 2)
    
    return frame