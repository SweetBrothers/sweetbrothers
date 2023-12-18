
import time
import os
import random
from flask import Flask, jsonify, request
import requests
import json 
import cv2
import base64
import io
from PIL import Image
import numpy as np


file = "post_train.py"
# input img 를 임시로 저장할 공간
user_img = "./asset/input_img"
# webui가 실행되고 있는 아이피와 포트
url = "http://127.0.0.1:7869"
app = Flask(__name__)

#실행될 dir 설정
os.chdir('/home/ds/final_flask')
out_dir = './outputs/api_out'
out_dir_i2i = os.path.join(out_dir, 'result')
os.makedirs(out_dir_i2i, exist_ok=True)
save_path = os.path.join(out_dir_i2i)   



# param에 저장되어 있는 이미지 호출시 사용
IMAGE_KEY = range(10)


# function

def encode_image_from_base64(path,dir = "asset"):
    """
    이미지 경로를 받아 해당 이미지를 base64 endocoding을 하여 반환하는 함수
    """  
    temp = f"./{dir}/{path}.png"
    print(temp)
    img = cv2.imread(temp)

    retval, bytes = cv2.imencode('.png', img)
    iamge_code = base64.b64encode(bytes).decode('utf-8')
    return iamge_code

def request_save(api, payload, file_name):
    """
    webui의 api를 사용하는 함수
    payload 를 webui의 원하는 api에 보내고 결과값을 저장 및 반환한다.  
    """
    response = requests.post(url=f'{url}/sdapi/v1/{api}', json=payload)
    r = response.json()
    image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
    image.save(f'./outputs/{file_name}.png')
    return image




@app.route('/generate_image', methods=['POST'])
def generate_image():
    """
    사용자에게 10자의 이미지와 여러 파라미터 정보를 받은 후에
    이미지를 생성하는 함수 
    """
    # gradio로 부터 받는 값
    params = json.loads(request.get_data(), encoding='utf-8')
    if len(params) == 0:
        return 'No parameter'
    try:
        # 임시 유저아이디 해당 아이디로 lora가 생성된다.
        user_id = "user"+str(random.randint(1, 7000))
        # 이미지 임시 저장
        for key in IMAGE_KEY:
            image = Image.open(io.BytesIO(base64.b64decode(params[f"image{key}"])))
            Image.fromarray(cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)).save(user_img+f"/{key+1}.png") 
        # post_train을 통한 lora훈련
        terminnal_command = f"python {file} {user_img} {user_id} {url}" 
        os.system(terminnal_command)
        
        #input받은 이미지중 첫번째로 받은 이미지를 통하여 생성 모델 실행 
        user_code = encode_image_from_base64("input_img/1")
        pose_number = params["pose"]
        pose_code = encode_image_from_base64(f"pose/{pose_number}")
        negative_prompt = ""
        model = "majicmixRealistic_v7.safetensors"
        vae = "vae-ft-mse-840000-ema-pruned.ckpt"
        sampler_name = "Euler a"         #"Euler a"    #"Euler"    #"DPM++ 2M Karras"  #"DPM++ SDE Karras"
        steps = 40
        cfg = 5
        prompt = f""
        # cool tone
        prompt_cool = f""
        # warm tone
        prompt_warm = f""

        if params["tone"] == "cool":
                prompt = prompt_cool
                sampler_name = 'Euler a'  # DPM++ 2M Karras
        elif params["tone"] == "warm":
                prompt = prompt_warm
                sampler_name = "Euler" # DPM++ SDE Karras
        # argument
        args_ad=[
            # True,
            # False,
            {
                "ad_model": "face_yolov8n.pt",
                    "ad_prompt": f"<lora:{user_id}:1>", 
                    "ad_negative_prompt": "",
                    "ad_denoising_strength": 0.5,
                    "ad_restore_face": True,
            },
            {
                "ad_model": "hand_yolov8n.pt",
                    "ad_prompt": "", 
                    "ad_negative_prompt": "",
            }
        ]
        # pose setting
        pose_ControlNet =[
            {
                "input_image" : pose_code, # pose img encode
                "module" : "dw_openpose_full",
                "model" : "control_v11p_sd15_openpose [cab727d4]", 
                "weight" : 1,
                "resize_mode" : 1,          # {0:just resize, 1: inner fit, 2: outer fit}
                "control_mode" : 2,         # {0:Balanced, 1: my prompt more, 2: controlnet more}
                "pixel_perfect" : True
            }
        ]
        ## parameter -i2i
        ## Reactor
        args=[
            user_code, #0  ## Img
            True, #1 Enable ReActor
            '0', #2 Comma separated face number(s) from swap-source image
            '0', #3 Comma separated face number(s) for target image (result)
            'inswapper_128.onnx', #4 model path
            'CodeFormer', #4 Restore Face: None; CodeFormer; GFPGAN
            1, #5 Restore visibility value
            False, #7 Restore face -> Upscale
            '4x-UltraSharp', #8 Upscaler (type 'None' if doesn't need), see full list here: http://127.0.0.1:7860/sdapi/v1/script-info -> reactor -> sec.8
            1, #9 Upscaler scale value  # 2time or 4 times
            1, #10 Upscaler visibility (if scale = 1)
            False, #11 Swap in source image
            True, #12 Swap in generated image
            1, #13 Console Log Level (0 - min, 1 - med or 2 - max)
            0, #14 Gender Detection (Source) (0 - No, 1 - Female Only, 2 - Male Only)
            0, #15 Gender Detection (Target) (0 - No, 1 - Female Only, 2 - Male Only)
            False, #16 Save the original image(s) made before swapping                              ## do we need to save?
            0.5, #17 CodeFormer Weight (0 = maximum effect, 1 = minimum effect), 0.5 - by default
            False, #18 Source Image Hash Check, True - by default
            False, #19 Target Image Hash Check, False - by default
            "CUDA", #20 CPU or CUDA (if you have it), CPU - by default
            True, #21 Face Mask Correction
            0, #22 Select Source, 0 - Image, 1 - Face Model
        ]


        ## parameter - upscale 
        args_upscale = [
                "",
                512,    # 512 , 768
                0,
                16, # 8~ 16, 20
                32, #32, 55
                64,
                0.2,   # Denoise
                32,
                5,  # upscaler_index 4 or 5
                False,   # upscale save image
                0,
                False,
                8,
                2,      # mode
                2,      # custom size?
                2048,
                2048,
                2       # scale size
        ]
        #########################################################################

        override_settings = {}
        override_settings["CLIP_stop_at_last_layers"] = 2
        override_settings["sd_model_checkpoint"] = model
        override_settings["sd_vae"] = vae
        override_payload = {
                        "override_settings": override_settings
                    }

        # t2i
        t2i_payload = {          
            "width": 768,
            "height": 960,
            "denoising_strength" : 0.75,
            "prompt" : prompt,
            "negative_prompt": negative_prompt,
            "steps": steps,
            "cfg_scale": 7,
            "sampler_name": sampler_name,
            "alwayson_scripts": {
                "ADetailer":{
                    "args": args_ad
                },
                "controlnet":{
                    "args": pose_ControlNet
                },
                # "reactor":{
                #     "args": args
                # }
            }
        }
        t2i_payload.update(override_payload)
        request_save("txt2img", t2i_payload, "base")      


        # i2i
        base_code = encode_image_from_base64("base")
        i2i_payload = {          
            "init_images" : [
                base_code
            ],
            "width": 768,
            "height": 960,
            "denoising_strength" : 0.45,
            "prompt" : prompt,
            "negative_prompt": negative_prompt,
            "steps": steps,
            "cfg_scale": cfg,
            "sampler_name": sampler_name,
            "alwayson_scripts": {
                "ADetailer":{
                    "args": args_ad
                }
            }
        }
        i2i_payload.update(override_payload)
        request_save("img2img", i2i_payload, "base_upscale")
        
        base_upscale = encode_image_from_base64("base_upscale","outputs")
        upscale_ControlNet =[
            {
                "input_image" : base_upscale, # pose img encode
                "module" : "tile_resample",
                "model" : "control_v11f1e_sd15_tile [a371b31b]", 
                "weight" : 1,
                "resize_mode" : 1,
                "control_mode" : 0,
                "pixel_perfect" : True
            }
        ]


        upscale_payload = {          
            "init_images" : [
                base_upscale
            ],
            "denoising_strength" : 0.2, # 0.15
            "prompt" : prompt,
            "negative_prompt": negative_prompt,
            "steps": steps,
            "cfg_scale": 7,
            "sampler_name": sampler_name,
            "script_name": "Ultimate SD upscale",
            "script_args": args_upscale,
            "alwayson_scripts": {
                "controlnet":{
                    "args": upscale_ControlNet
                }
            }
        }
        upscale_payload.update(override_payload)

        response = requests.post(url=f'{url}/sdapi/v1/img2img', json=upscale_payload)
        r = response.json()
        
        return jsonify({"images": f"{r['images']}",})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(port=7860, host='192.168.0.7')