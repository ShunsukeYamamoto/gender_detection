from icrawler.builtin import BingImageCrawler
import os, sys
from variables import classes

class_name = "女性"

if not os.path.exists("./" + class_name):
  os.mkdir(class_name)

crawler = BingImageCrawler(
  downloader_threads=4,
  storage={"root_dir": class_name}
)

crawler.crawl(
  keyword=class_name,
  filters=None,
  max_num=300,
  min_size=(500,500)
)