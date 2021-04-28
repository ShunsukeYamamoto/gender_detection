import tensorflow as tf
import numpy as np
import cv2

filename = "/home/asilla/gender_detection/tfrecord/train.tfrecord"

def parse(tfrecord):
  features = tf.parse_single_example(
    tfrecord,
    features={
      'image/height': tf.FixedLenFeature([],dtype=tf.int64),
      'image/width': tf.FixedLenFeature([],dtype=tf.int64),
      'image/encoded': tf.FixedLenFeature([],dtype=tf.string),
      'image/format': tf.FixedLenFeature([],dtype=tf.string),
      'image/object/bbox/xmin': tf.FixedLenFeature([],dtype=tf.float32),
      'image/object/bbox/xmax': tf.FixedLenFeature([],dtype=tf.float32),
      'image/object/bbox/ymin': tf.FixedLenFeature([],dtype=tf.float32),
      'image/object/bbox/ymax': tf.FixedLenFeature([],dtype=tf.float32),
      'image/object/class/text': tf.FixedLenFeature([],dtype=tf.string),
      'image/object/class/label': tf.FixedLenFeature([],dtype=tf.int64)
    }
  )
  return features

dataset = tf.data.TFRecordDataset([filename]).map(parse)
iterator = dataset.make_one_shot_iterator()
next_element= iterator.get_next()
raw_img = next_element["image/encoded"]
xmin = next_element["image/object/bbox/xmin"]
img = tf.image.decode_jpeg(raw_img,channels=3)

tfrecord = next(tf.python_io.tf_record_iterator(filename))
example = tf.train.Example()
example.ParseFromString(tfrecord)

raw_image = example.features.feature["image/encoded"].bytes_list.value[0]
height = example.features.feature["image/height"].int64_list.value[0]
width = example.features.feature["image/width"].int64_list.value[0]
xmin = example.features.feature["image/object/bbox/xmin"].float_list.value[0]
ymin = example.features.feature["image/object/bbox/ymin"].float_list.value[0]
xmax = example.features.feature["image/object/bbox/xmax"].float_list.value[0]
ymax = example.features.feature["image/object/bbox/ymax"].float_list.value[0]

xmin = int(width * xmin)
xmax = int(width * xmax)
ymin = int(height * ymin)
ymax = int(height * ymax)

array = np.asarray(bytearray(raw_image), dtype=np.uint8)
img = cv2.imdecode(array, -1)
cv2.rectangle(img,(xmin,ymax), (xmax, ymin),(255,0,0,), thickness=2)
cv2.imshow("test",img)
cv2.waitKey(0)
cv2.destroyAllWindows()