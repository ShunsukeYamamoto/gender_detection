from glob import glob
from typing import Text
from PIL import Image

import tensorflow as tf
import xml.etree.ElementTree as ET
import cv2,io

files = glob("/home/asilla/gender_detection/annotation2/*")


def create_tf_example(img_width,img_height,filename,encode_img,xmins,xmaxs,ymins,ymaxs,genders,labels):
  example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': tf.train.Feature(int64_list=tf.train.Int64List(value=[img_height])),
      'image/width': tf.train.Feature(int64_list=tf.train.Int64List(value=[img_width])),
      'image/encoded': tf.train.Feature(bytes_list=tf.train.BytesList(value=[encode_img])),
      'image/format': tf.train.Feature(bytes_list=tf.train.BytesList(value=[b'jpg'])),
      'image/object/bbox/xmin': tf.train.Feature(float_list=tf.train.FloatList(value=xmins)),
      'image/object/bbox/xmax': tf.train.Feature(float_list=tf.train.FloatList(value=xmaxs)),
      'image/object/bbox/ymin': tf.train.Feature(float_list=tf.train.FloatList(value=ymins)),
      'image/object/bbox/ymax': tf.train.Feature(float_list=tf.train.FloatList(value=ymaxs)),
      'image/object/class/text': tf.train.Feature(bytes_list=tf.train.BytesList(value=genders)),
      'image/object/class/label': tf.train.Feature(int64_list=tf.train.Int64List(value=labels))
  }))
  return example


writer_train = tf.python_io.TFRecordWriter("/home/asilla/gender_detection/tfrecord/train.tfrecord")
writer_test = tf.python_io.TFRecordWriter("/home/asilla/gender_detection/tfrecord/test.tfrecord")
for i,file in enumerate(files):
  xml = ET.parse(file)
  img_path = xml.find("path").text
  img_width = int(xml.find("size").find("width").text)
  img_height = int(xml.find("size").find("height").text)

  datas = xml.findall("object")
  with tf.gfile.GFile(img_path,"rb") as f:
    encode_img = f.read()

  xmins = []
  ymins = []
  xmaxs = []
  ymaxs = []
  genders = []
  labels = []

  for data in datas:
    gender = data.find("name").text.encode()
    label = 1 if gender == "male" else 2
    coordinates = data.find("bndbox")
    xmin = float(coordinates.find("xmin").text) / img_width
    ymin = float(coordinates.find("ymin").text) / img_height
    xmax = float(coordinates.find("xmax").text) / img_width
    ymax = float(coordinates.find("ymax").text) / img_height

    genders.append(gender)
    labels.append(label)
    xmins.append(xmin)
    ymins.append(ymin)
    xmaxs.append(xmax)
    ymaxs.append(ymax)

  examples = create_tf_example(
    img_width=img_width,
    img_height=img_height,
    filename=img_path,
    encode_img=encode_img,
    xmins=xmins,
    xmaxs=xmaxs,
    ymins=ymins,
    ymaxs=ymaxs,
    genders=genders,
    labels=labels
  )
  if i < 700:
    writer_train.write(examples.SerializeToString())
  else:
    writer_test.write(examples.SerializeToString())

writer_train.close()
writer_test.close()