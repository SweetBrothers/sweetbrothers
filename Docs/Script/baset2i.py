import requests         
import io              
import base64           
import json
import os
import cv2
from PIL import Image, PngImagePlugin    
from datetime import datetime, date

url = "" 

os.chdir('/home/ds/api/outputs')
current_directory = os.getcwd()
out_dir = 'api_out'
out_dir_i2i = os.path.join(out_dir, 'txt2img')
os.makedirs(out_dir_i2i, exist_ok=True)
save_path = os.path.join(out_dir_i2i)       
output = "base"

## img processing
input = './user.png'     # First img = face img (user img)
img = cv2.imread(input)
pose = './pose.png'
img2 = cv2.imread(pose)

# Encode into PNG and send
retval, bytes = cv2.imencode('.png', img)
iamge_code = base64.b64encode(bytes).decode('utf-8')

retval, bytes = cv2.imencode('.png', img2)
image_pose = base64.b64encode(bytes).decode('utf-8')


############################################################################################
## parameter
gender1 = "1girl"   # 1girl  # handsome male
gender2 = "female"            # female # 1boy
prompt = f"({gender1}:1.6)"

negative_prompt = ""
model = "majicmixRealistic_v7.safetensors"
vae = "vae-ft-mse-840000-ema-pruned.ckpt"
sampler_name = "DPM++ 2M Karras"         #"Euler a"    #"Euler"    #"DPM++ 2M Karras"  #"DPM++ SDE Karras"
steps = 10
denoising_strength = 0.75


## Reactor
args=[
    iamge_code, #0  ## Img
    True, #1 Enable ReActor
    '0', #2 Comma separated face number(s) from swap-source image
    '0', #3 Comma separated face number(s) for target image (result)
    'inswapper_128.onnx', #4 model path
    'CodeFormer', #4 Restore Face: None; CodeFormer; GFPGAN
    1, #5 Restore visibility value
    True, #7 Restore face -> Upscale
    '4x-UltraSharp', #8 Upscaler (type 'None' if doesn't need), see full list here: http://127.0.0.1:7860/sdapi/v1/script-info -> reactor -> sec.8
    1, #9 Upscaler scale value  # 2time or 4 times
    1, #10 Upscaler visibility (if scale = 1)
    False, #11 Swap in source image
    True, #12 Swap in generated image
    1, #13 Console Log Level (0 - min, 1 - med or 2 - max)
    0, #14 Gender Detection (Source) (0 - No, 1 - Female Only, 2 - Male Only)
    0, #15 Gender Detection (Target) (0 - No, 1 - Female Only, 2 - Male Only)
    False, #16 Save the original image(s) made before swapping                              ## do we need to save?
    0.8, #17 CodeFormer Weight (0 = maximum effect, 1 = minimum effect), 0.5 - by default
    False, #18 Source Image Hash Check, True - by default
    False, #19 Target Image Hash Check, False - by default
    "CUDA", #20 CPU or CUDA (if you have it), CPU - by default
    True, #21 Face Mask Correction
    0, #22 Select Source, 0 - Image, 1 - Face Model
]

## Adetailer parameter
args_ad=[
    # True,
    # False,
    {
        "ad_model": "face_yolov8n.pt",
            "ad_prompt": f"{gender2}", 
            "ad_negative_prompt": "",
            "ad_steps": 28,
            "ad_sampler": sampler_name,
            "ad_restore_face": True,
    },
    {
        "ad_model": "hand_yolov8n.pt",
            "ad_prompt": "", 
            "ad_negative_prompt": "",
            "ad_steps": 28,
            "ad_sampler": sampler_name,
    }
]

## ControlNet parameter
args_ControlNet =[
    {
        "input_image" : image_pose, # pose img encode
        "module" : "dw_openpose_full",
        "model" : "control_v11p_sd15_openpose [cab727d4]", 
        "weight" : 1,
        "resize_mode" : 2,          # {0:just resize, 1: inner fit, 2: outer fit}
        "control_mode" : 2,         # {0:Balanced, 1: my prompt more, 2: controlnet more}
        "pixel_perfect" : True
    }
]
###########################################################################################


payload = {          
    "width": 768,
    "height": 960,
    "denoising_strength" : denoising_strength,
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
            "args": args_ControlNet
        },
        "reactor":{
            "args": args
        },
    }
}

override_settings = {}
override_settings["CLIP_stop_at_last_layers"] = 1
override_settings["sd_model_checkpoint"] = model
override_settings["sd_vae"] = vae
override_payload = {
                "override_settings": override_settings
            }
payload.update(override_payload)


response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
r = response.json()

image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
image.save('base.png')