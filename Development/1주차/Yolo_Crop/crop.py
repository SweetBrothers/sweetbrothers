
# cv 에서는 x = height y = width 이다.

import cv2
# in colab
# from google.colab.patches import cv2_imshow
from ultralyticsplus import YOLO


class Croper:

    """
    이미지의 얼굴의 바운드 박스의 중심을 기준으로 정사각형으로이 이미지를 자른 후에
    crop_img_size * 2 값의 가로 세로 값을 가지는 이미지로 저장해 주는 클래스이다.

    img_path: 이미지가 저장되어 있는 경로
    model_path : model 이 저장되어 있는 경로
    crop_img_size : 최종 이미지의 한변 길이의 절반 값
    """
    def __init__(self ,img_path ,model_path = './model/yolov8n-face.pt'  ,crop_img_size = 256 ):
      self.img_path = img_path
      self.model = YOLO(model_path)
    # set model parameters
      self.model.overrides['conf'] = 0.25  # NMS confidence threshold
      self.model.overrides['iou'] = 0.45  # NMS IoU threshold
      self.model.overrides['agnostic_nms'] = False  # NMS class-agnostic
      self.model.overrides['max_det'] = 1000  # maximum number of detections per image
      self.crop_img_size = crop_img_size
      self.resize =False
      self.makeSavePath()

    def makeSavePath(self):
        """
        이미지가 저장되는 경로를 save_path에 저장한다.
        """
        temp = self.img_path.split('/')
        temp[-1] = "result/"+temp[-1]
        self.save_path = '/'.join(temp)

    def getCordinate(self):
        """
        이미지를 자를 때 필요한 바운드 박스의 중심값,
        이미지를 자르는 기준이 될 사각형의 속성값등을 저장하는 함수
        """
        self.img = cv2.imread(self.img_path)
        img_x ,img_y ,_= self.img.shape

        results = self.model.predict(self.img_path,verbose =False)

        # # observe results
        # print(results[0].boxes)
        # render = render_result(model=model, image=image, result=results[0])

        try:
          x,y,xx,yy = results[0].boxes[0].xyxy[0]
          x,y,xx,yy = int(x),int(y),int(xx),int(yy)
          m_x = x + int((xx-x)/2)
          m_y = y + int((yy-y)/2)
          self.suc = True
        except:
          print("fail!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
          print(results)
          self.suc = False
          return 0

        bbw = xx- x
        bbh = yy-y

        if img_x < (2 * self.crop_img_size):
            self.crop_img_size = int((img_x)/2) + 1
        if img_y <  (2 * self.crop_img_size):
            self.crop_img_size = int((img_y)/2) + 1
        # 얼굴의 크기가 512 *512 보다 크면 바운드 박스에 맞추어 자른 후 이미지 크기를 조절한다. 
        if bbh > self.crop_img_size :
            self.crop_img_size  = int(bbh/2)+90
            self.resize = True


        self.x_low = m_x - self.crop_img_size
        self.x_high = m_x + self.crop_img_size

        self.y_low = m_y -self.crop_img_size
        self.y_high = m_y+self.crop_img_size

        ## 이미지를 자르는 박스가 이미지 밖으러 나갔을 때는 나간 만큼 반대 쪽으로 늘린다.

        if self.x_low < 0:
            self.x_high -= self.x_low 
            self.x_low =0 

        if self.y_low < 0:
            self.y_high -= self.y_low
            self.y_low =0
    def cropImg(self,verbose = 1):
        """
        이미지를 자르는 함수 verbose값으로 1을 넣으면 최종 이미지를 출력해준다.
        Args:
            verbose (int, optional): _description_. Defaults to 1.
        """
        self.getCordinate()
        if self.suc:
            crop_img =  self.img[self.y_low:self.y_high,self.x_low:self.x_high]
            if self.resize :
                crop_img = cv2.resize(crop_img,dsize= (512,512))
            if verbose == 1:
                # in colab
                cv2_imshow(crop_img)
                print(self.save_path)
                # in local
                # cv2.imshow(self.img[self.y_low:self.y_high,self.x_low:self.x_high])
            cv2.imwrite(f'{self.save_path}',crop_img)



# 사용 예시
if __name__ == '__main__':
    path = "/content/drive/MyDrive/YearDream/img_Data/2.newjeans_data/danielle"
    names = os.listdir(path)
    for name in names :
        cr =  Croper("/".join((path,name)))
        print("/".join((path,name)) )
        print("="*100)
        cr.cropImg()


