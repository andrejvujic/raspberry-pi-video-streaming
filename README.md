# raspberry-pi-video-streaming

An example on how to stream live video from RaspberryPi camera
to a Flask server.

This project was heavily inspired by Eben Kouao's project on making a RaspberryPi camera stream: https://github.com/EbenKouao/pi-camera-stream-flask.

Unfortunately his proejct uses the `pi_camera` module which isn't available on 64bit RaspberryPi operating systems.
This project implements video streaming using the `opencv-python` module and it works for both 32 and 64bit operating systems.

# Dependencies

This project depends on the following packages:

- `flask`
- `opencv-python`
- `numpy`

# Hardware

This project was tested with the RaspberryPi 4B running 64bit RaspberryPi OS and the v1.3 RaspberryPi camera. It should work on any RaspberryPi and camera model.

# Contact

Get in touch with me: <a href="mailto:vujicandrej366@gmail.com">vujicandrej366@gmail.com</a>
