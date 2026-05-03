import supervision as sv
from ultralytics import YOLO
import sys
from utils import save_stub, read_stub
sys.path.append('../')



class BallTracker :
    def __init__(self, model_path, batch_size=16) :
        self.model = YOLO(model_path)
        self.batch_size = batch_size
    def predict_frames(self, frames) :
        results = []
        for i in range(0, len(frames), self.batch_size) :
            frame_batch = frames[i : i + self.batch_size]
            result_batch = self.model.predict(frame_batch, conf=0.5)
            results += result_batch
        return results
    def get_object_tracks(self, frames, read_from_stub=False, stub_path=None) :
        stub = read_stub(read_from_stub, stub_path)
        if stub is not None :
            return stub
        
        results = self.predict_frames(frames)
        tracks = []
        for result in results :
            idx_to_names = result.names
            names_to_idx = {n:i for i,n in idx_to_names.items()}
            detection_tracks = sv.Detections.from_ultralytics(result)
            tracks.append({})
            for frame_detection in detection_tracks :
                bbox = frame_detection[0].tolist()
                idx = frame_detection[3]
                conf_score = frame_detection[2]
                max_conf_score = 0
                if idx == names_to_idx['Ball'] :
                    if max_conf_score < conf_score:
                        tracks[-1][0] = {"box": bbox}
                        max_conf_score = conf_score

        if stub_path is not None :
            save_stub(tracks, stub_path)
        return tracks
    def filter_wrong_detections(self, tracks) :
        growth_rate = 20
        current_allowed_distance = 0
        previous_x, previous_y = -1, -1
        filtered_tracks = []
        for frame_num, frame in enumerate(tracks) :
            current_allowed_distance += growth_rate

            filtered_tracks.append({})

            if 0 not in frame:
                continue

            bbox = frame[0]["box"]
            x1, y1, x2, y2 = map(int, bbox)
            current_x, current_y = (x1 + x2) // 2, y1
            dist = abs(current_x - previous_x) + abs(current_y - previous_y)

            if previous_x == -1 or dist <= current_allowed_distance:
                current_frame = frame_num
                filtered_tracks[-1][0] = {"box":bbox}
                previous_x, previous_y = current_x, current_y
        return filtered_tracks