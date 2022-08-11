from urllib import request
import webbrowser
from flask import Flask, Response, render_template, request
from camera import VideoCamera
import RPi.GPIO as GPIO

camera = VideoCamera()
app = Flask(__name__)


def _gen(camera: VideoCamera):
    while True:
        frame = camera.get_image()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
        )


@app.route("/", methods=["GET"])
def index():
    _ = request.url
    if _[-1] == "/":
        _ = _[:-1]

    return render_template("index.html", video_feed_url=f"{_}/video")


@app.route("/video", methods=["GET"])
def video():
    return Response(
        _gen(
            camera=camera,
        ),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    try:
        webbrowser.open(
            f"http://0.0.0.0:{camera.port}",
        )

        app.run(
            host="0.0.0.0", port=camera.port,
            debug=False,
        )
    finally:
        GPIO.cleanup()
