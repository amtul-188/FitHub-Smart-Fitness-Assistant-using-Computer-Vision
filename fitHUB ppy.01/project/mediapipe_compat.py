"""
mediapipe_compat.py  —  works with mediapipe 0.10.18 on Windows
Uses mediapipe.python.solutions (the correct path for this version)
"""

import cv2
import numpy as np
from mediapipe.python.solutions import pose as _pose
from mediapipe.python.solutions import drawing_utils as _drawing_utils

# ── Public API ───────────────────────────────────────────────────────────────

class _PoseLandmarkEnum:
    LEFT_SHOULDER  = _pose.PoseLandmark.LEFT_SHOULDER
    RIGHT_SHOULDER = _pose.PoseLandmark.RIGHT_SHOULDER
    LEFT_ELBOW     = _pose.PoseLandmark.LEFT_ELBOW
    RIGHT_ELBOW    = _pose.PoseLandmark.RIGHT_ELBOW
    LEFT_WRIST     = _pose.PoseLandmark.LEFT_WRIST
    RIGHT_WRIST    = _pose.PoseLandmark.RIGHT_WRIST
    LEFT_HIP       = _pose.PoseLandmark.LEFT_HIP
    RIGHT_HIP      = _pose.PoseLandmark.RIGHT_HIP
    LEFT_KNEE      = _pose.PoseLandmark.LEFT_KNEE
    RIGHT_KNEE     = _pose.PoseLandmark.RIGHT_KNEE
    LEFT_ANKLE     = _pose.PoseLandmark.LEFT_ANKLE
    RIGHT_ANKLE    = _pose.PoseLandmark.RIGHT_ANKLE


class PoseCompat:
    """Drop-in replacement for the old mp.solutions.pose.Pose()"""
    PoseLandmark = _PoseLandmarkEnum

    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self._pose = _pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def process(self, rgb_image):
        return self._pose.process(rgb_image)

    def close(self):
        self._pose.close()


class DrawingCompat:
    """Drop-in replacement for mp.solutions.drawing_utils"""

    def draw_landmarks(self, image, pose_landmarks, connections=None,
                       landmark_drawing_spec=None, connection_drawing_spec=None):
        if pose_landmarks is None:
            return
        _drawing_utils.draw_landmarks(
            image,
            pose_landmarks,
            _pose.POSE_CONNECTIONS
        )