import tensorflow as tf
import numpy as np
import cv2

model_path = "/home/asilla/gender_detection/model/frozen_inference_graph.pb"

def init_tf():
  detection_graph = tf.Graph()
  with detection_graph.as_default():
    graph_def = tf.GraphDef()
    with tf.gfile.GFile(model_path,"rb") as f:
      seriarized_graph = f.read()
      graph_def.ParseFromString(seriarized_graph)
      tf.import_graph_def(graph_def,name="")
  config = tf.ConfigProto()
  config.gpu_options.allow_growth = True
  sess = tf.Session(graph=detection_graph,config=config)
  return sess, detection_graph

def get_tensor(graph):
  image_tensor = graph.get_tensor_by_name("image_tensor:0")
  detection_boxes = graph.get_tensor_by_name("detection_boxes:0")
  detection_scores = graph.get_tensor_by_name("detection_scores:0")
  detection_classes = graph.get_tensor_by_name("detection_classes:0")
  return image_tensor, detection_boxes, detection_scores, detection_classes

def inference(img, sess, image_tensor, detection_boxes, detection_scores, detection_classes):
  img = np.expand_dims(img,axis=0)
  boxes, scores, classes = sess.run(
    [detection_boxes, detection_scores, detection_classes],
    feed_dict = {image_tensor:img}
  )
  return boxes[0], scores[0], classes[0]

def rectangle_cordinate(img,box):
  height = img.shape[0]
  width = img.shape[1]
  ymin = int(height * box[0])
  xmin = int(width * box[1])
  ymax = int(height * box[2])
  xmax = int(width * box[3])
  return ymin, xmin, ymax, xmax

def main():
  sess, detection_graph = init_tf()
  image_tensor, detection_boxes, detection_scores, detection_classes = get_tensor(detection_graph)
  cap = cv2.VideoCapture("/dev/video0")

  while True:
    _, img = cap.read()

    boxes, scores, genders = inference(img, sess, image_tensor, detection_boxes, detection_scores, detection_classes)

    for i,box in enumerate(boxes):
      if scores[i] > 0.8:
        ymin, xmin, ymax, xmax = rectangle_cordinate(img, box)
        if genders[i] == 1.0:
          color = (255,0,0)
        else:
          color = (0,0,255)
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), color, thickness=2)
        print(scores[i])
    
    cv2.imshow("test", img)
    if cv2.waitKey(1) & 0xff == 27:
      break

  cap.release()
  cv2.destroyAllWindow()
  sess.close()


if __name__ == "__main__":
  main()
