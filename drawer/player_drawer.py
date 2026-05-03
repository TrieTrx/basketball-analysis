import cv2
from .player_indicator import draw_ellipse, draw_rectangle

class PlayerDrawer :
    def __init__(self):
        pass
    def draw(self, frames, trackers) :
        output_frames = []
        for frame_num, frame in enumerate(frames) :
            frame = frame.copy()
            tracker = trackers[frame_num]
            for track_id, player in tracker.items() :
                frame = draw_ellipse(frame, track_id, player)
            output_frames.append(frame)
        return output_frames
    