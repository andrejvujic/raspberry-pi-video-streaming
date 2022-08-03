from typing import Any
import cv2
import time
import numpy as np


class VideoCamera:
    def __init__(self, type: str = ".jpg", index: int = -1) -> None:
        self.index = index
        self.cap = cv2.VideoCapture(self.index)
        self.type = type
        time.sleep(2.0)

    def __del__(self) -> None:
        self.cap.release()

    def apply_flips(self, frame: Any, flip_h: bool = False, flip_v: bool = False) -> Any:
        if flip_h:
            frame = np.fliplr(frame)

        if flip_v:
            frame = np.flip(frame, 0)

        return frame

    def get_frame(self, flip_h=True, flip_v=True) -> Any:
        _, frame = self.cap.read()
        frame = self.apply_flips(frame=frame, flip_h=flip_h, flip_v=flip_v)
        _, image = cv2.imencode(self.type, frame)

        return image.tobytes()
