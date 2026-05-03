from utils import read_video, write_video
from trackers import PlayerTracker, BallTracker
from drawer import PlayerDrawer, BallDrawer


def main() :
    frames, fps = read_video('input-videos/video_1.mp4')

    player_tracker = PlayerTracker('models/player.pt')
    player_tracks = player_tracker.get_object_tracks(frames, read_from_stub=True, stub_path='stubs/output_video1.pkl')
    player_drawer = PlayerDrawer()

    ball_tracker = BallTracker('models/player.pt')
    ball_tracks = ball_tracker.get_object_tracks(frames, read_from_stub=True, stub_path='stubs/ball_output_video1.pkl')
    ball_tracks = ball_tracker.filter_wrong_detections(ball_tracks)
    ball_drawer = BallDrawer()

    frames = player_drawer.draw(frames, player_tracks)
    frames = ball_drawer.draw(frames, ball_tracks)
    write_video(frames, fps, 'output/ouput_video1.mp4')

if __name__ == "__main__" :
    main()