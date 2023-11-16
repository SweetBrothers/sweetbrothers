# YOLO를 통한 이미지 전처리


```python

# 사용예시
import os

path = "/content/drive/MyDrive/YearDream/img_Data/2.newjeans_data/danielle"
names = os.listdir(path)
for name in names :
    cr =  Croper("/".join((path,name)))
    print("/".join((path,name)) )
    print("="*100)
    cr.cropImg()

```

Ultralytics YOLOv8.0.43 🚀 Python-3.10.12 torch-2.1.0+cu118 CPU
/content/drive/MyDrive/YearDream/img_Data/2. newjeans_data/danielle/danielle_(14).jpg
====================================================================================================
Model summary (fused): 168 layers, 3005843 parameters, 0 gradients, 8.1 GFLOPs

![result](image.png)

/content/drive/MyDrive/YearDream/img_Data/2. newjeans_data/danielle/result/danielle_(14).jpg