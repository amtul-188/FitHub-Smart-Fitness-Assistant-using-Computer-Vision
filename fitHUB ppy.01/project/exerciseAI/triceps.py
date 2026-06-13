import cv2
import numpy as np
from project.mediapipe_compat import PoseCompat, DrawingCompat
from project.util import calculate_angle

def gen():
    mp_draw = DrawingCompat()
    pose_comp = PoseCompat(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    PoseLandmark = pose_comp.PoseLandmark

    up_pos = down_pos = None
    counter = 0

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
            Left_shoulder  = [lm[PoseLandmark.LEFT_SHOULDER.value].x,  lm[PoseLandmark.LEFT_SHOULDER.value].y]
            Left_elbow     = [lm[PoseLandmark.LEFT_ELBOW.value].x,     lm[PoseLandmark.LEFT_ELBOW.value].y]
            Left_wrist     = [lm[PoseLandmark.LEFT_WRIST.value].x,     lm[PoseLandmark.LEFT_WRIST.value].y]
            Right_shoulder = [lm[PoseLandmark.RIGHT_SHOULDER.value].x, lm[PoseLandmark.RIGHT_SHOULDER.value].y]
            Right_elbow    = [lm[PoseLandmark.RIGHT_ELBOW.value].x,    lm[PoseLandmark.RIGHT_ELBOW.value].y]
            Right_wrist    = [lm[PoseLandmark.RIGHT_WRIST.value].x,    lm[PoseLandmark.RIGHT_WRIST.value].y]

            left_arm_angle  = int(calculate_angle(Left_shoulder,  Left_elbow,  Left_wrist))
            right_arm_angle = int(calculate_angle(Right_shoulder, Right_elbow, Right_wrist))

            if left_arm_angle > 140 and right_arm_angle > 140:
                up_pos = 'Up'
            if left_arm_angle < 40 and right_arm_angle < 40 and up_pos == 'Up':
                down_pos = 'Down'
            if left_arm_angle > 140 and right_arm_angle > 140 and down_pos == 'Down':
                counter += 1
                up_pos = down_pos = None

            mp_draw.draw_landmarks(frames, result.pose_landmarks)

        cv2.putText(frames, str(int(counter)), (15, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3, cv2.LINE_AA)
        frame = cv2.imencode('.jpg', frames)[1].tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
