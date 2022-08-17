# -*- coding: utf-8 -*-

import cv2
import traceback
from datetime import datetime
from flask import Flask, render_template, make_response, Response, abort

app = Flask(__name__, template_folder="templates")

class Project(object):
    def __init__(self, *args):
        self.loop = True
        self.cam = cv2.VideoCapture("rtsp://rtsp.stream/pattern") # uri frame rtsp
        self.log = "log.txt"

    def generate_frame_jpg(self) -> cv2.imencode:
        """ Get frame rtsp and convert to frame jpg """
        try:
            while self.loop:
                sucess, frame = self.cam.read()
                if not sucess:
                    with open(self.log, "a") as log:
                        log.write(f"Date: {datetime.now() | Error: sucess}")
                        continue
                else:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception:
            traceback.print_exc()
            self.loop = False

@app.route("/", methods=["GET"])
def index() -> make_response:
    try:
        return make_response(render_template("index.html"), 200)
    except Exception as error:
        traceback.print_exc()
        return abort(503)

@app.route("/video_feed", methods=["GET"])
def video_feed() -> make_response:
    try:
        return make_response(
            Response(Project().generate_frame_jpg(),
            mimetype="multipart/x-mixed-replace; boundary=frame"), 200)
    except Exception:
        traceback.print_exc()
        abort(503)
