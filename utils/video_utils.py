import cv2
import os

def read_video(input_path) :
    videoCap = cv2.VideoCapture(input_path)
    frames = []
    while True :
        ret, frame = videoCap.read()
        if not ret :
            break
        frames.append(frame)
    return frames, videoCap.get(cv2.CAP_PROP_FPS)

def write_video(frames, fps, output_path) :
    if not os.path.exists(os.path.dirname(output_path)) :
        os.mkdir(os.path.dirname(output_path))

    height, width, layers = frames[0].shape
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    for frame in frames :
        out.write(frame)
    out.release()