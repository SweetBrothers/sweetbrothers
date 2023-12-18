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
out_dir = 'api_out'
out_dir_i2i = os.path.join(out_dir, 'img2img')
save_path = os.path.join(out_dir_i2i, 'upscale')               


input = f'./upscale.png'
img = cv2.imread(input)     # first img = output of i2i for upscale

retval, bytes = cv2.imencode('.png', img)
iamge_base = base64.b64encode(bytes).decode('utf-8')

## parameter

gender1 = "1girl"   #1girl
gender2 = "female"            #female
prompt = ""

negative_prompt = ""
model = "majicmixRealistic_v7.safetensors"
vae = "vae-ft-mse-840000-ema-pruned.ckpt"
sampler_name = "DPM++ 2M Karras"         #"Euler a"    #"Euler"    #"DPM++ 2M Karras"  #"DPM++ SDE Karras"
steps = 30
denoising_strength = 0.2    # 0.15~0.3

## ControlNet parameter #tile 
args_ControlNet =[
    {
        "input_image" : iamge_base, # pose img encode
        "module" : "tile_resample",
        "model" : "control_v11f1e_sd15_tile [a371b31b]", 
        "weight" : 1,
        "resize_mode" : 2,
        "control_mode" : 2,
        "pixel_perfect" : True
    }
]

args_upscale = [
        "",
        512,
        0,
        8,
        32,
        64,
        0.35,   # Denoise
        32,
        3,  # ES
        True,   # upscale save image
        0,
        False,
        8,
        0,
        2,      # custom size?
        1024,
        1024,
        2       # scale size
]


payload = {          
    "init_images" : [
        iamge_base
    ],
    "width": 768,
    "height": 960,
    "denoising_strength" : denoising_strength,
    "prompt" : prompt,
    "negative_prompt": negative_prompt,
    "steps": 35,
    "cfg_scale": 7,
    "sampler_name": sampler_name,
    "script_name": "Ultimate SD upscale",
    "script_args": args_upscale,
    "alwayson_scripts": {
        "controlnet":{
            "args": args_ControlNet
        }
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


response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
r = response.json()

image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
image.save('final.png')



# denoise 0.35
# contorlNet tile + contorlNet important
# ultimate upscale 