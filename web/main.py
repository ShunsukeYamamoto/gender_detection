from flask import Flask, render_template, request, Response, g
from pprint import pprint
from flask.helpers import url_for
import numpy as np
import cv2, base64
from inference import *


app = Flask(__name__)

infer = Inference()

@app.route("/")
def index():
  # g.infer = Inference()
  return render_template("index.html")

@app.route("/get_frame",methods=["POST"])
def get_frame():
  raw_img = request.files["video"].read()
  detected_img = infer.detect(raw_img)
  encoded_img = base64.b64encode(detected_img)
  return encoded_img

@app.route("/img")
def img():
  return Response(detect(), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/detect")
def detect():
  with open("frame.jpeg","rb") as f:
    frame = f.read()
  return base64.b64encode(frame)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000,ssl_context=("../ssl/server.crt", "../ssl/server.key"), threaded=True, debug=True)