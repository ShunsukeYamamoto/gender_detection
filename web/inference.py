from pprint import pprint
import tensorflow as tf
import numpy as np
import cv2

model_path = "/home/asilla/gender_detection/model/frozen_inference_graph.pb"
threshold = 0.8
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]

class Inference():

  def __init__(self):
    self.sess, self.graph = self._init_inference()
    self.image_tensor = self.graph.get_tensor_by_name("image_tensor:0")
    self.boxes = self.graph.get_tensor_by_name("detection_boxes:0")
    self.scores = self.graph.get_tensor_by_name("detection_scores:0")
    self.classes = self.graph.get_tensor_by_name("detection_classes:0")

  def _init_inference(self):
    detection_graph = tf.Graph()
    with detection_graph.as_default():
      graph_def = tf.GraphDef()
      with tf.gfile.GFile(model_path,"rb") as f:
        serialized_graph = f.read()
        graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(graph_def,name="")
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(graph=detection_graph,config=config)
    return sess, detection_graph
  
  def _inference(self,img):
    img = np.expand_dims(img,axis=0)
    boxes, scores, classes = self.sess.run(
      [self.boxes, self.scores, self.classes],
      feed_dict={self.image_tensor: img}
    )
    return boxes[0], scores[0], classes[0]

  def _write_boxes(self,img, boxes, scores, classes):
    for i,box in enumerate(boxes):
      height = img.shape[0]
      width = img.shape[1]
      ymin = int(height * box[0])
      xmin = int(width * box[1])
      ymax = int(height * box[2])
      xmax = int(width * box[3])
      if classes[i] == 1.0:
        color = (255,0,0)
      else:
        color = (0,0,255)
      writed_img = cv2.rectangle(img, (xmin,ymin), (xmax,ymax), color, thickness=2)
      _, encoded_img = cv2.imencode(".jpeg", writed_img, encode_param)
      return encoded_img

  def detect(self, raw_img):
    img_array = np.asarray(bytearray(raw_img),dtype=np.uint8)
    img = cv2.imdecode(img_array,-1)
    boxes, scores, classes = self._inference(img)
    detected_img = self._write_boxes(img, boxes, scores, classes)
    return detected_img



