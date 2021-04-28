## 顔検出・性別判定アルゴリズム

【概要】
Webカメラの入力から顔検出・性別判定を行う

【学習環境】
- ハードウェア
CPU：intel core i7
GPU：Geforce GTX 1650

- ミドルウェア
CUDA：v10.1

- フレームワーク
Tensorflow-gpu 1.14.0

【使用ライブラリ】
Flask
OpenCV
numpy
icrawler

【アノテーションツール】
labelImg

【採用アルゴリズム】
backbone：MovileNetv3
head：SSD

【作業内容】  
① icrawlerを用いて「male」「female」の画像データをスクレイピング（計730枚ほど）  
② labelImgを用いてPaccal Voc形式でアノテーション  
③ アノテーションデータをtfrecord形式に学習  
④ OpenCVでWebカメラから映像を入力しGPUを使用して推論


