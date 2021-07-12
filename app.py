# -*- coding: utf-8 -*- 

import cv2
from datetime import datetime
from flask import Flask, render_template, Response

app = Flask(__name__, template_folder="templates")

class Project(object):
    def __init__(self, *args):
        self.loop = True
        self.cam = cv2.VideoCapture("rtsp:.../") # uri frame rtsp 
        self.log = "log.txt"

    """ Get frame rtsp and convert for image jpg """ 
    def generate_frame(self):
        try:
            while self.loop is True:

                sucess, frame = self.cam.read()
                
                if not sucess:
                    with open(self.log, "wr") as log:
                        log.write(f"Date: {datetime.now() | Error: sucess}")
                        log.close()
                        continue

                else:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        except Exception as error:
            print(f"Error: {error}")

    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/video_feed", methods=["GET"])
    def video_feed():
        return Response(Project().generate_frame(), mimetype="multipart/x-mixed-replace; boundary=frame")
