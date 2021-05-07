## 顔検出・性別判定アルゴリズム  

【概要】  
Webカメラの入力から顔検出と性別判定を行う

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

## デモ動画(5/6現在)
https://user-images.githubusercontent.com/59650988/117405542-c4d81880-af46-11eb-9a94-fa898fbee4e9.mp4

※青BBOX=男性、赤BBOX=女性  

### 改善点
- 検知範囲が最大5m→顔が小さめな学習データを投入して改善を狙います  

### 今後やりたいこと（4/27現在）
- Jetson Nanoにデプロイ  
- 推論モデルをTensorRTに変換してCUDA上で実行  
