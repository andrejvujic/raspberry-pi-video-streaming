from flask import Flask, Response, render_template, request
from camera import VideoCamera

camera = VideoCamera()
app = Flask(__name__)


def _gen(camera: VideoCamera, flip_h: bool, flip_v: bool):
    while True:
        frame = camera.get_frame(flip_h=flip_h, flip_v=flip_v)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
        )


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/video", methods=["GET"])
def video():
    args = request.args
    flip_h = args.get("flip_h", default=False)
    flip_v = args.get("flip_v", default=False)

    return Response(
        _gen(
            camera=camera, flip_h=flip_h, flip_v=flip_v,
        ),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
