import json
from typing import Any
import cv2
import time
import numpy as np


class VideoCamera:
    def __init__(self, type: str = ".jpg", index: int = -1) -> None:
        self.CONFIG_FILE = "camera.json"
        self.index = index
        self.cap = cv2.VideoCapture(self.index)
        self.type = type

        config = self._load_config()
        self.flip_h = config["flip_h"]
        self.flip_v = config["flip_v"]

        time.sleep(2.0)

    def _load_config(self) -> Any:
        with open(self.CONFIG_FILE, "r") as f:
            return json.loads(f)

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
