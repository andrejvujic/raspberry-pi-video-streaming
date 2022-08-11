import json
from typing import Any
import cv2
import time
import numpy as np

GREEN = (0, 255, 0)
THICKNESS = 2


class VideoCamera:
    def __init__(self, type: str = ".jpg", index: int = -1) -> None:
        self.CONFIG_FILE = "camera.json"
        self.index = index
        self.cap = cv2.VideoCapture(self.index)
        self.type = type
        self.previous_frame = None

        config = self._load_config()
        self.flip_h = config["flip_h"]
        self.flip_v = config["flip_v"]

        time.sleep(2.0)

    def _load_config(self) -> Any:
        with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

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
        if _:
            frame = self.apply_flips(frame=frame)
            frame = self.detect_people(frame=frame)

            _, image = cv2.imencode(self.type, frame)

            self.previous_frame = frame

            return image.tobytes()

        _, image = cv2.imencode(self.type, self.previous_frame)
        return image.tobytes()

    def detect_people(self, frame: Any) -> Any:
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(
            cv2.HOGDescriptor_getDefaultPeopleDetector(),
        )

        frame = self.to_grayscale(frame=frame)
        boxes, _ = hog.detectMultiScale(frame, winStride=(8, 8))
        boxes = np.array(
            [[x, y, x + w, y + h] for (x, y, w, h) in boxes]
        )

        for (xA, yA, xB, yB) in boxes:
            cv2.rectangle(
                frame,
                (xA, yA), (xB, yB),
                color=GREEN,
                thickness=THICKNESS,
            )

        return self.to_color(frame=frame)

    def to_grayscale(self, frame: Any) -> Any:
        return cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    def to_color(self, frame: Any) -> Any:
        return cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
