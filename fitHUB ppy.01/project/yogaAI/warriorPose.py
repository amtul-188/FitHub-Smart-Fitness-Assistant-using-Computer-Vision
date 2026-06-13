import cv2
import numpy as np
from project.mediapipe_compat import PoseCompat, DrawingCompat
from project.util import calculate_angle

def gen():
    mp_draw = DrawingCompat()
    pose_comp = PoseCompat(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    PoseLandmark = pose_comp.PoseLandmark
    label = "Unknown Pose"

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
            left_shoulder  = [lm[PoseLandmark.LEFT_SHOULDER.value].x,  lm[PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow     = [lm[PoseLandmark.LEFT_ELBOW.value].x,     lm[PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist     = [lm[PoseLandmark.LEFT_WRIST.value].x,     lm[PoseLandmark.LEFT_WRIST.value].y]
            right_shoulder = [lm[PoseLandmark.RIGHT_SHOULDER.value].x, lm[PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow    = [lm[PoseLandmark.RIGHT_ELBOW.value].x,    lm[PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist    = [lm[PoseLandmark.RIGHT_WRIST.value].x,    lm[PoseLandmark.RIGHT_WRIST.value].y]
            left_hip       = [lm[PoseLandmark.LEFT_HIP.value].x,       lm[PoseLandmark.LEFT_HIP.value].y]
            right_hip      = [lm[PoseLandmark.RIGHT_HIP.value].x,      lm[PoseLandmark.RIGHT_HIP.value].y]
            left_knee      = [lm[PoseLandmark.LEFT_KNEE.value].x,      lm[PoseLandmark.LEFT_KNEE.value].y]
            right_knee     = [lm[PoseLandmark.RIGHT_KNEE.value].x,     lm[PoseLandmark.RIGHT_KNEE.value].y]
            left_ankle     = [lm[PoseLandmark.LEFT_ANKLE.value].x,     lm[PoseLandmark.LEFT_ANKLE.value].y]
            right_ankle    = [lm[PoseLandmark.RIGHT_ANKLE.value].x,    lm[PoseLandmark.RIGHT_ANKLE.value].y]

            left_shoulder_angle  = calculate_angle(left_elbow,  left_shoulder,  left_hip)
            right_shoulder_angle = calculate_angle(right_hip,   right_shoulder, right_elbow)
            left_knee_angle      = calculate_angle(left_hip,    left_knee,      left_ankle)
            right_knee_angle     = calculate_angle(right_hip,   right_knee,     right_ankle)

            shoulders_ok  = (80 < left_shoulder_angle < 110) and (80 < right_shoulder_angle < 110)
            one_straight  = (155 < left_knee_angle < 205) or  (155 < right_knee_angle < 205)
            one_bent      = (90  < left_knee_angle < 120) or  (90  < right_knee_angle < 120)

            if shoulders_ok and one_straight and one_bent:
                label = "Warrior Pose - CORRECT ✓"
            else:
                label = "Unknown Pose"

            mp_draw.draw_landmarks(frames, result.pose_landmarks)

        color = (0, 200, 0) if "CORRECT" in label else (255, 0, 0)
        cv2.putText(frames, label, (40, 50), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
        frame = cv2.imencode('.jpg', frames)[1].tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
