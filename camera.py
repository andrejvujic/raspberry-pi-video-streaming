from typing import Any
import cv2
import time
import numpy as np


class VideoCamera:
    def __init__(self, type: str = ".jpg", index: int = -1, flip_h: bool = False, flip_v: bool = False) -> None:
        self.index = index
        self.cap = cv2.VideoCapture(self.index)
        self.type = type
        self.flip_h = flip_h
        self.flip_v = flip_v
        time.sleep(2.0)

    def __del__(self) -> None:
        self.cap.release()

    def apply_flips(self, frame: Any) -> Any:
        if self.flip_h:
            frame = np.fliplr(frame)

        if self.flip_v:
            frame = np.flip(frame, 0)

        return frame

    def get_frame(self) -> Any:
        _, frame = self.cap.read()
        frame = self.apply_flips(frame=frame)
        _, image = cv2.imencode(self.type, frame)

        return image.tobytes()
