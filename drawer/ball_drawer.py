import cv2
from .ball_indicator import draw_rectangle, draw_triangle

class BallDrawer :
    def __init__(self):
        pass
    def draw(self, frames, trackers) :
        output_frames = []
        for frame_num, frame in enumerate(frames) :
            frame = frame.copy()
            tracker = trackers[frame_num]
            for _, ball in tracker.items() :
                if ball["box"] is None :
                    continue
                x1, y1, x2, y2 = map(int, ball["box"])         
                frame = draw_triangle(frame, ball)
            output_frames.append(frame)
        return output_frames