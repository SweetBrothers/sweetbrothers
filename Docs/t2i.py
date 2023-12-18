import requests         # reqeust
import io               # convert information server into a file
import base64           # convert information of image into a base64 code
import json
import os
from PIL import Image, PngImagePlugin    # color

url = ""

os.chdir('/home/ds/api/outputs')
current_directory = os.getcwd()


##txt2img

# payload_sample = {
#   "enable_hr": False,
#   "denoising_strength": 0,
#   "firstphase_width": 0,
#   "firstphase_height": 0,
#   "prompt": "",
#   "styles": ["string"],
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
#   "restore_faces": False,
#   "tiling": False,
#   "negative_prompt": "string",
#   "eta": 0,
#   "s_churn": 0,
#   "s_tmax": 0,
#   "s_tmin": 0,
#   "s_noise": 1,
#   "override_settings": {},
#   "override_settings_restore_afterwards": True,
#   "sampler_index": "Euler"
# }

payload = {
    "prompt": "maltese puppy",
    "steps": 20
}

response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
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
