import numpy as np
import gradio as gr
import requests
import cv2
import base64
import io
import json 
from PIL import Image, PngImagePlugin

url = "http://192.168.0.7:7860"
IMAGE_KEY = range(10)
TONE = 10
POSE = 11
GENDER =12

def change_img(pose):
    return gr.Image(
        label = "pose",
        value = f"./asset/{pose}.png",
        height = 300,
        width = 200,
        show_download_button = False,
        sources = None,
        interactive = False)
def generate_image(*args):
    print(args[-3:])
    params = {
        "gender" : args[GENDER],
        "pose" : args[POSE],
        "tone" : args[TONE]
        }
    
    for key in IMAGE_KEY:
        _, bytes = cv2.imencode('.png', args[key])  
        image_code = base64.b64encode(bytes).decode('utf-8')
        params[f"image{key}"] = image_code
    res ={}
    try:
        res = requests.post(f"{url}/generate_image", data=json.dumps(params))
        response_data = res.json()['images']
        image = Image.open(io.BytesIO(base64.b64decode(response_data.split(",",1)[0])))
    except:
        print(res.json())
        return None
    return image
        
    

# gradio blocks layout사용
with gr.Blocks() as demo:
    gr.Markdown("Profile Image demo")

    # 이미지 탭 추후에 다른 탭을 추가 가능
    with gr.Tab("Image"):
        input_data= [0]*13
        with gr.Row():
            for i in range(5):
                input_data[i] = gr.Image()
        with gr.Row():
            for i in range(5,10):
                input_data[i] = gr.Image()
        image_button = gr.Button("Create")
    with gr.Tab("Result"):
        with gr.Row():
            image_output = gr.Image()   
        
    # 세부 옵션
    with gr.Accordion("Option" ,open = False):
        input_data[TONE]= gr.Radio({"warm":0, "cool":1}, type="value",value="warm",label = "Tone",interactive =True)
        input_data[GENDER] = gr.Radio(["man", "woman"], type="value" , value="woman",label="gender",interactive=False)
        input_data[POSE] = gr.Radio(["1", "2","3","4"], type="value" , value="1",label="pose",interactive=True)
        pose_image = gr.Image(
            label = "pose",
            value = "./asset/1.png",
            height = 300,
            width = 200,
            show_download_button = False,
            sources = None,
            interactive = False
        )
        input_data[POSE].change(fn=change_img, inputs=input_data[POSE], outputs=pose_image )
 
        


    image_button.click(generate_image, inputs=input_data, outputs=image_output)

# 로그인창을 거쳐가게 한다.
if __name__ == "__main__":
    demo.launch(auth=("admin","admin"))