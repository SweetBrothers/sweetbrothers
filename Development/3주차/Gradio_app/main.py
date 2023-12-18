import numpy as np
import gradio as gr
import requests
import cv2
import base64
import io
import json
from PIL import Image, PngImagePlugin

# flask api가 실행되는 서버의 ip:port
url = "http://192.168.0.7:7860"

# 이미지와 성별 값을 받아 이미지 생성을 요청하는 함수
def i2i(img , select_model , gender):
    _, bytes = cv2.imencode('.png', img)
    image_code = base64.b64encode(bytes).decode('utf-8')
    params = {
        "init_images" : [image_code],
        "gender" : gender
    }
    res = requests.post(f"{url}/i2i", data=json.dumps(params))
    response_data = res.json()['images']
    image = Image.open(io.BytesIO(base64.b64decode(response_data.split(",",1)[0])))
    return image



# gradio blocks layout사용
with gr.Blocks() as demo:
    gr.Markdown("Profile Image demo")

    # 이미지 탭 추후에 다른 탭을 추가 가능
    with gr.Tab("Image"):
        with gr.Row():
            image_input = gr.Image()
            image_output = gr.Image()
        image_button = gr.Button("Create")
    # 세부 옵션
    with gr.Accordion("Option" ,open = False):
        select_model = gr.Dropdown(["first", "second", "third"], type="value",value="second",label = "model",interactive =True)
        gender = gr.Radio(["man", "woman"], type="value" , value="woman",label="gender",interactive=True)


    image_button.click(i2i, inputs=[image_input,select_model,gender], outputs=image_output)

# 로그인창을 거쳐가게 한다.
if __name__ == "__main__":
    demo.launch(auth=("admin","admin"))