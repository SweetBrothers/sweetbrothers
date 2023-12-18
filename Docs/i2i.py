import requests         # reqeust
import io               # convert information server into a file
import base64           # convert information of image into a base64 code
import json
import os
import cv2
from PIL import Image, PngImagePlugin    # color


url = "" ## always needs to check      # 고정 url.
os.chdir('/home/ds/api/outputs')
current_directory = os.getcwd()

## img2img

# {
#   "prompt": "",
#   "negative_prompt": "",
#   "styles": [
#     "string"
#   ],
#   "seed": -1,
#   "subseed": -1,
#   "subseed_strength": 0,
#   "seed_resize_from_h": -1,
#   "seed_resize_from_w": -1,
#   "sampler_name": "string",
#   "batch_size": 1,
#   "n_iter": 1,
#   "steps": 50,
#   "cfg_scale": 7,
#   "width": 512,
#   "height": 512,
#   "restore_faces": true,
#   "tiling": true,
#   "do_not_save_samples": false,
#   "do_not_save_grid": false,
#   "eta": 0,
#   "denoising_strength": 0.75,
#   "s_min_uncond": 0,
#   "s_churn": 0,
#   "s_tmax": 0,
#   "s_tmin": 0,
#   "s_noise": 0,
#   "override_settings": {},
#   "override_settings_restore_afterwards": true,
#   "refiner_checkpoint": "string",
#   "refiner_switch_at": 0,
#   "disable_extra_networks": false,
#   "comments": {},
#   "init_images": [
#     "string"
#   ],
#   "resize_mode": 0,
#   "image_cfg_scale": 0,
#   "mask": "string",
#   "mask_blur_x": 4,
#   "mask_blur_y": 4,
#   "mask_blur": 0,
#   "inpainting_fill": 0,
#   "inpaint_full_res": true,
#   "inpaint_full_res_padding": 0,
#   "inpainting_mask_invert": 0,
#   "initial_noise_multiplier": 0,
#   "latent_mask": "string",
#   "sampler_index": "Euler",
#   "include_init_images": false,
#   "script_name": "string",
#   "script_args": [],
#   "send_images": true,
#   "save_images": false,
#   "alwayson_scripts": {}
# }


# 필요한 item = prompt, sampler_name, alwayson_scripts

path = './output.png'

# img = Image.open(path)
# with io.BytesIO() as output:
#     img.save(output, format='PNG')
#     img_bytes = output.getvalue()
# iamge_code = base64.b64encode(img_bytes).decode('utf-8')

# Read Image in RGB order
img = cv2.imread(path)

# Encode into PNG and send to ControlNet
retval, bytes = cv2.imencode('.png', img)
iamge_code = base64.b64encode(bytes).decode('utf-8')

payload = {
    "init_images" : [
        iamge_code
    ],
    "denoising_strength" : 0.75,
    "prompt" : "cute cat",
    "steps": 20
}

response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
r = response.json()

for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

    png_payload = {
        "image": "data:image/png;base64," + i
    }
    response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    image.save('output.png', pnginfo=pnginfo)

# output1 = reference image.
# output2 = final output