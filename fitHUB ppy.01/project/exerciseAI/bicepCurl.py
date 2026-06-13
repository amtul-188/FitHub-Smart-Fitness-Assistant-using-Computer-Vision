import cv2
import numpy as np
from project.mediapipe_compat import PoseCompat, DrawingCompat
from project.util import calculate_angle

def gen():
    mpDraw = DrawingCompat()
    my_pose = PoseCompat(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    PoseLandmark = my_pose.PoseLandmark

    counter = 0
    stage = None
    flag = False

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = my_pose.process(imgRGB)

        if result.pose_landmarks:
            flag = (counter % 2 == 0)
            landmarks = result.pose_landmarks.landmark

            if flag:
                shoulder = [landmarks[PoseLandmark.LEFT_SHOULDER.value].x,  landmarks[PoseLandmark.LEFT_SHOULDER.value].y]
                elbow    = [landmarks[PoseLandmark.LEFT_ELBOW.value].x,     landmarks[PoseLandmark.LEFT_ELBOW.value].y]
                wrist    = [landmarks[PoseLandmark.LEFT_WRIST.value].x,     landmarks[PoseLandmark.LEFT_WRIST.value].y]
            else:
                shoulder = [landmarks[PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[PoseLandmark.RIGHT_SHOULDER.value].y]
                elbow    = [landmarks[PoseLandmark.RIGHT_ELBOW.value].x,    landmarks[PoseLandmark.RIGHT_ELBOW.value].y]
                wrist    = [landmarks[PoseLandmark.RIGHT_WRIST.value].x,    landmarks[PoseLandmark.RIGHT_WRIST.value].y]

            angle = calculate_angle(shoulder, elbow, wrist)
            if angle > 160:
                stage = "down"
            if angle < 30 and stage == 'down':
                stage = "up"
                counter += 1

            cv2.putText(img, str(int(angle)),
                        tuple(np.multiply(elbow, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 180, 255), 2, cv2.LINE_AA)
            mpDraw.draw_landmarks(img, result.pose_landmarks)

        label = "Good Job!" if (counter != 0 and counter % 20 == 0) else str(int(counter))
        color  = (0, 0, 255) if "Good" in label else (255, 0, 0)
        cv2.putText(img, label, (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, color, 3)

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
