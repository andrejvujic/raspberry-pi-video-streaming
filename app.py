from flask import Flask, Response, render_template
from flask_ngrok import run_with_ngrok
from camera import VideoCamera

camera = VideoCamera()
app = Flask(__name__)
run_with_ngrok(app)


def _gen(camera: VideoCamera):
    while True:
        frame = camera.get_frame()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n"
        )


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/video", methods=["GET"])
def video():
    return Response(
        _gen(
            camera=camera,
        ),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    app.run()
