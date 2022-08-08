from urllib import request
from flask import Flask, Response, render_template, request
from camera import VideoCamera

camera = VideoCamera()
app = Flask(__name__)


def _gen(camera: VideoCamera):
    while True:
        frame = camera.get_frame()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
        )


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", video_feed_url="/video")


@app.route("/video", methods=["GET"])
def video():
    return Response(
        _gen(
            camera=camera,
        ),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0", debug=False,
    )
