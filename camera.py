import json
from typing import Any
import cv2
import time
import numpy as np

GREEN = (0, 255, 0)
THICKNESS = 2


class VideoCamera:
    def __init__(self, type: str = ".jpg") -> None:
        self.CONFIG_FILE = "camera.json"

        config = self._load_config()
        self.flip_h = config["flip_h"]
        self.flip_v = config["flip_v"]
        self.index = config["camera_index"]
        self.zoom_factor = config["zoom_factor"]
        self.port = config["port"]

        self.cap = cv2.VideoCapture(self.index)

        self.type = type
        self.previous_frame = None

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
            frame = self.zoom(frame=frame)
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

        frame = self.to_color(frame=frame)
        return frame

    def zoom(self, frame: Any, coord=None) -> Any:
        h, w, _ = [self.zoom_factor * i for i in frame.shape]

        if coord is None:
            cx, cy = w/2, h/2
        else:
            cx, cy = [self.zoom_factor * c for c in coord]

        frame = cv2.resize(
            frame, (0, 0), fx=self.zoom_factor, fy=self.zoom_factor)
        frame = frame[int(round(cy - h/self.zoom_factor * .5)): int(round(cy + h/self.zoom_factor * .5)),
                      int(round(cx - w/self.zoom_factor * .5)): int(round(cx + w/self.zoom_factor * .5)),
                      :]

        return frame

    def to_grayscale(self, frame: Any) -> Any:
        return cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    def to_color(self, frame: Any) -> Any:
        return cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
