import json
from typing import Any, Type
import cv2
import time
import numpy as np

NoneType = type(None)

GREEN = (0, 255, 0)
THICKNESS = 3


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

            if type(self.previous_frame) is not NoneType and self.previous_frame.all():
                difference = self.get_difference_between_frames(frame=frame)
                frame = self.detect_motion(
                    frame,
                    self.to_grayscale(difference),
                )

            self.previous_frame = frame
            return frame

        return self.previous_frame

    def get_image(self) -> Any:
        frame = self.get_frame()
        _, image = cv2.imencode(self.type, frame)
        return image.tobytes()

    def get_difference_between_frames(self, frame: Any) -> Any:
        return cv2.absdiff(frame, self.previous_frame)

    def zoom(self, frame: Any, coord=None) -> Any:
        h, w, _ = [self.zoom_factor * i for i in frame.shape]

        if coord is None:
            cx, cy = w/2, h/2
        else:
            cx, cy = [self.zoom_factor * c for c in coord]

        frame = cv2.resize(
            frame,
            (0, 0),
            fx=self.zoom_factor, fy=self.zoom_factor,
        )

        frame = frame[
            int(round(cy - h/self.zoom_factor * .5)): int(round(cy + h/self.zoom_factor * .5)),
            int(round(cx - w/self.zoom_factor * .5)): int(round(cx + w/self.zoom_factor * .5)),
            :]

        return frame

    def detect_motion(self, frame: Any, diffrence_gray: Any):
        diffrence_blur = cv2.GaussianBlur(diffrence_gray, (5, 5), 0)

        diffrence_threshold = cv2.threshold(
            diffrence_blur, 25, 255, cv2.THRESH_BINARY,
        )[1]

        diffrence_dilate = cv2.dilate(
            diffrence_threshold, None, iterations=4,
        )

        (contours, _) = cv2.findContours(
            diffrence_dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE,
        )

        if len(contours) > 0:
            for cnt in contours:
                (x, y, w, h) = cv2.boundingRect(cnt)
                if cv2.contourArea(cnt) > 700 and (x < 840) and (y > 150 and y < 350):
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  GREEN, THICKNESS)

        return frame

    def to_grayscale(self, frame: Any) -> Any:
        return cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    def to_color(self, frame: Any) -> Any:
        return cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
