# T2I
    # - prompt + lora
    # - adetailer
    #     - face & hands
    # - contorlnet
    #     - pose Img
    #     - setting 
    #         - balanced
    #         - crop and resize
    # - reactor
    #     - visual 0.7~0.8, 0.5 weight

# I2I
    # - prompt + lora + denoise = 0.5
    # - t2i output = Base
    # - adetailer 
    #     - face & hands = denoise 0.4


# Upscale (i2i-2)
    # - prompt + lora + denoise = 0.1
    # - i2i output = Base
    # - controlnet
    #     -tile img = i2i output
    #     - balanced
    #     - crop and resize
    # - script - upscale
    #     - 4x-ultrasharp
    #     - scale size 2
#######################################################################

import requests         
import io              
import base64           
import json
import os
import cv2
from PIL import Image

# environment setting
url = ""

os.chdir('/home/ds/api/outputs')
out_dir = 'api_out'
out_dir_i2i = os.path.join(out_dir, 'result')
os.makedirs(out_dir_i2i, exist_ok=True)
save_path = os.path.join(out_dir_i2i)   


# function

def encode_image_from_base64(path):
        input = f'./{path}.png'
        img = cv2.imread(input)

        retval, bytes = cv2.imencode('.png', img)
        iamge_code = base64.b64encode(bytes).decode('utf-8')
        return iamge_code

def request_save(api, payload, file_name):
        response = requests.post(url=f'{url}/sdapi/v1/{api}', json=payload)
        r = response.json()
        image = Image.open(io.BytesIO(base64.b64decode(r['images'][0])))
        image.save(f'{file_name}.png')
        return image



user_code = encode_image_from_base64("user")    #image name

pose_number = input()
pose_code = encode_image_from_base64(f"{pose_number}")

#######################################################################
## parameter - t2i
negative_prompt = ""
model = "majicmixRealistic_v7.safetensors"
vae = "vae-ft-mse-840000-ema-pruned.ckpt"
sampler_name = "DPM++ 2M SDE Karras"         #"Euler a"    #"Euler"    #"DPM++ 2M Karras"  #"DPM++ 2M SDE Karras"
steps = 40
cfg = 4

user_id = "" # choose train lora
prompt = ""
# cool tone
prompt_cool = ""
# warm tone
prompt_warm = ""

prompt_number = input()
if prompt_number == 0:
        pass
elif prompt_number == 1:
        prompt = prompt_cool
        sampler_name = "DPM++ 2M Karras"  # DPM++ 2M Karras # Euler a
else:
        prompt = prompt_warm
        sampler_name = "DPM++ 2M SDE Karras" # DPM++ SDE Karras #Euler



## Adetailer parameter
args_ad=[
    # True,
    # False,
    {
        "ad_model": "face_yolov8s.pt",
            "ad_prompt": f"<lora:{user_id}:1.1>", 
            "ad_negative_prompt": "",
            "ad_denoising_strength": 0.6,
            "ad_inpaint_only_masked": True,
            "ad_mask_blur": 4,
            "ad_inpaint_only_masked_padding": 32,    # 32? or 0?
            "ad_restore_face": True,
    },
    {
        "ad_model": "hand_yolov8n.pt",
            "ad_prompt": "", 
            "ad_negative_prompt": "",
            "ad_denoising_strength": 0.4,
            "ad_inpaint_only_masked": True,
            "ad_mask_blur": 4,
            "ad_inpaint_only_masked_padding": 32,    # 32? or 0?
    }
]

## ControlNet parameter
pose_ControlNet =[
    {
        "input_image" : pose_code, # pose img encode
        "module" : "dw_openpose_full", #"dw_openpose_full", "openpose_full"
        "model" : "control_v11p_sd15_openpose [cab727d4]", 
        "weight" : 1,
        "resize_mode" : 2,          # {0:just resize, 1: inner fit, 2: outer fit}
        "control_mode" : 1,         # {0:Balanced, 1: my prompt more, 2: controlnet more}  
        "pixel_perfect" : False
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


## parameter - upscale  # seams fix 제외해
args_upscale = [
        "",
        512,    # 512 , 768
        0,
        8, # 8~ 16, 20
        32, #32, 55
        64,
        0.2,   # Denoise
        32,
        3,  # upscaler_index 3,4 or 5
        False,   # upscale save image
        0,
        False,
        8,
        0,      # mode 0: none 1: Band pass
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
    "width": 512,
    "height": 768,
    "prompt" : prompt,
    "negative_prompt": negative_prompt,
    "steps": steps,
    "cfg_scale": cfg,
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
    "width": 512,
    "height": 768,
    "denoising_strength" : 0.45, #0.35
    "prompt" : "",
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



# upscale
base_upscale = encode_image_from_base64("base_upscale")
upscale_ControlNet =[
    {
        "input_image" : base_upscale, # pose img encode
        "module" : "tile_resample",
        "model" : "control_v11f1e_sd15_tile [a371b31b]", 
        "weight" : 1,
        "resize_mode" : 2,
        "control_mode" : 2,
        "pixel_perfect" : False
    }
]


upscale_payload = {          
    "init_images" : [
        base_upscale
    ],
    "denoising_strength" : 0.15, # 0.15
    "prompt" : "",
    "negative_prompt": negative_prompt,
    "steps": steps,
    "cfg_scale": cfg,
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
request_save("img2img", upscale_payload, "final")