import cv2
import numpy as np
from project.mediapipe_compat import PoseCompat, DrawingCompat
from project.util import calculate_angle

def gen():
    mp_draw = DrawingCompat()
    pose_comp = PoseCompat(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    PoseLandmark = pose_comp.PoseLandmark

    down_pos = None
    squat_counter = 0

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frames = cap.read()
        if not ret:
            break
        frames = cv2.flip(frames, 1)
        image = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)
        result = pose_comp.process(image)

        if result.pose_landmarks:
            lm = result.pose_landmarks.landmark
            Left_hip    = [lm[PoseLandmark.LEFT_HIP.value].x,    lm[PoseLandmark.LEFT_HIP.value].y]
            Right_hip   = [lm[PoseLandmark.RIGHT_HIP.value].x,   lm[PoseLandmark.RIGHT_HIP.value].y]
            Left_knee   = [lm[PoseLandmark.LEFT_KNEE.value].x,   lm[PoseLandmark.LEFT_KNEE.value].y]
            Right_knee  = [lm[PoseLandmark.RIGHT_KNEE.value].x,  lm[PoseLandmark.RIGHT_KNEE.value].y]
            Left_ankle  = [lm[PoseLandmark.LEFT_ANKLE.value].x,  lm[PoseLandmark.LEFT_ANKLE.value].y]
            Right_ankle = [lm[PoseLandmark.RIGHT_ANKLE.value].x, lm[PoseLandmark.RIGHT_ANKLE.value].y]

            left_leg_angle  = int(calculate_angle(Left_hip,  Left_knee,  Left_ankle))
            right_leg_angle = int(calculate_angle(Right_hip, Right_knee, Right_ankle))

            if left_leg_angle < 100 and right_leg_angle < 100:
                down_pos = 'Down'
            if left_leg_angle > 160 and right_leg_angle > 160 and down_pos == 'Down':
                squat_counter += 1
                down_pos = None

            mp_draw.draw_landmarks(frames, result.pose_landmarks)

        cv2.putText(frames, str(int(squat_counter)), (15, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3, cv2.LINE_AA)
        frame = cv2.imencode('.jpg', frames)[1].tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
