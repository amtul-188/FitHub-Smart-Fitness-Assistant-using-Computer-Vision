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

            Left_shoulder = [lm[PoseLandmark.LEFT_SHOULDER.value].x, lm[PoseLandmark.LEFT_SHOULDER.value].y]
            Left_elbow    = [lm[PoseLandmark.LEFT_ELBOW.value].x,    lm[PoseLandmark.LEFT_ELBOW.value].y]
            Left_wrist    = [lm[PoseLandmark.LEFT_WRIST.value].x,    lm[PoseLandmark.LEFT_WRIST.value].y]
            Left_hip      = [lm[PoseLandmark.LEFT_HIP.value].x,      lm[PoseLandmark.LEFT_HIP.value].y]

            Right_shoulder = [lm[PoseLandmark.RIGHT_SHOULDER.value].x, lm[PoseLandmark.RIGHT_SHOULDER.value].y]
            Right_elbow    = [lm[PoseLandmark.RIGHT_ELBOW.value].x,    lm[PoseLandmark.RIGHT_ELBOW.value].y]
            Right_wrist    = [lm[PoseLandmark.RIGHT_WRIST.value].x,    lm[PoseLandmark.RIGHT_WRIST.value].y]
            Right_hip      = [lm[PoseLandmark.RIGHT_HIP.value].x,      lm[PoseLandmark.RIGHT_HIP.value].y]

            Left_elbowAngle     = calculate_angle(Left_shoulder,  Left_elbow,  Left_wrist)
            Right_elbowAngle    = calculate_angle(Right_shoulder, Right_elbow, Right_wrist)
            left_shoulder_angle = calculate_angle(Left_elbow,     Left_shoulder,  Left_hip)
            right_shoulder_angle= calculate_angle(Right_hip,      Right_shoulder, Right_elbow)

            if (155 < Left_elbowAngle < 205) and (155 < Right_elbowAngle < 205):
                if (80 < left_shoulder_angle < 110) and (80 < right_shoulder_angle < 110):
                    label = "T Pose - CORRECT"
                else:
                    label = "Unknown Pose"
            else:
                label = "Unknown Pose"

            mpDraw.draw_landmarks(img, result.pose_landmarks)

        color = (0, 200, 0) if "CORRECT" in label else (255, 0, 0)
        cv2.putText(img, label, (40, 50), cv2.FONT_HERSHEY_PLAIN, 3, color, 3)
        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')