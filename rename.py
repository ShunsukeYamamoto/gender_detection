from glob import glob
import os
import time

name = "img2"
num = 0

files = glob("./" + name + "/*")

for i, file in enumerate(files):
  os.rename(file,"./" + name + "/" + name + "-" + str(i + num) + ".jpg")