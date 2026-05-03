import supervision as sv
from ultralytics import YOLO
import sys
from utils import save_stub, read_stub
sys.path.append('../')



class PlayerTracker :
    def __init__(self, model_path, batch_size=16) :
        self.model = YOLO(model_path)
        self.tracker = sv.ByteTrack()
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
            result_sv = sv.Detections.from_ultralytics(result)
            detection_tracks = self.tracker.update_with_detections(result_sv)
            tracks.append({})
            for frame_detection in detection_tracks :
                bbox = frame_detection[0].tolist()
                idx = frame_detection[3]
                id = frame_detection[4]
                if idx == names_to_idx['Player'] :
                    tracks[-1][id] = {'box' : bbox}
                 

        if stub_path is not None :
            save_stub(tracks, stub_path)
        return tracks



            



             
            

        
