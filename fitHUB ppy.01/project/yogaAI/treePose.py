import cv2
import numpy as np
from project.mediapipe_compat import PoseCompat, DrawingCompat
from project.util import calculate_angle

def gen():
    mpDraw = DrawingCompat()
    my_pose = PoseCompat(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    PoseLandmark = my_pose.PoseLandmark
    label = "Unknown Pose"

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = my_pose.process(imgRGB)

        if result.pose_landmarks:
            lm = result.pose_landmarks.landmark
            left_knee_angle = calculate_angle(
                [lm[PoseLandmark.LEFT_HIP.value].x,   lm[PoseLandmark.LEFT_HIP.value].y],
                [lm[PoseLandmark.LEFT_KNEE.value].x,  lm[PoseLandmark.LEFT_KNEE.value].y],
                [lm[PoseLandmark.LEFT_ANKLE.value].x, lm[PoseLandmark.LEFT_ANKLE.value].y])
            right_knee_angle = calculate_angle(
                [lm[PoseLandmark.RIGHT_HIP.value].x,   lm[PoseLandmark.RIGHT_HIP.value].y],
                [lm[PoseLandmark.RIGHT_KNEE.value].x,  lm[PoseLandmark.RIGHT_KNEE.value].y],
                [lm[PoseLandmark.RIGHT_ANKLE.value].x, lm[PoseLandmark.RIGHT_ANKLE.value].y])

            one_straight = (165 < left_knee_angle < 195) or (165 < right_knee_angle < 195)
            one_bent     = (315 < left_knee_angle < 335) or (25  < right_knee_angle < 45)

            if one_straight and one_bent:
                label = "Tree Pose - CORRECT ✓"
            else:
                label = "Unknown Pose"

            mpDraw.draw_landmarks(img, result.pose_landmarks)

        color = (0, 200, 0) if "CORRECT" in label else (255, 0, 0)
        cv2.putText(img, label, (40, 50), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
