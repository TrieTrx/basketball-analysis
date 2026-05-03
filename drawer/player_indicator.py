import cv2

def draw_rectangle(frame, track_id, player) :
    x1, y1, x2, y2 = map(int, player["box"])
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.putText(frame, f"Player {track_id}", (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    return frame

def get_ellipse_rectangle(center, axes) :
    rec_center = (center[0], center[1] + axes[1])
    rec_size = (20, 10)
    return ((rec_center[0] - rec_size[0], rec_center[1] - rec_size[1]),
           (rec_center[0] + rec_size[0], rec_center[1] + rec_size[1]))
def draw_ellipse(frame, track_id, player) :
    x1, y1, x2, y2 = map(int, player["box"])
    center = ((x1 + x2) // 2, y2)
    width = (x2 - x1) // 2 + 10 
    axes = (width, max(width // 4, 20))
    cv2.ellipse(frame, center, axes, 0, 0 - 20, 180 + 20, (0, 0, 255), 2)

    rec_box = get_ellipse_rectangle(center, axes)
    cv2.rectangle(frame, rec_box[0], rec_box[1], (0, 0, 255), -1)

    text = f"{track_id}"
    (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    text_x = rec_box[0][0] + (rec_box[1][0] - rec_box[0][0] - text_w) // 2
    text_y = rec_box[0][1] + (rec_box[1][1] - rec_box[0][1] + text_h) // 2
    cv2.putText(frame, text, (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    return frame