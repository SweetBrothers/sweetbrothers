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

payload = {
    "prompt": "cirno",
    "steps": 20
}

override_settings = {}
override_settings["filter_nsfw"] = True
override_settings["CLIP_stop_at_last_layers"] = 2

override_payload = {
    "override_settings": override_settings
}

payload.update(override_payload)

# Define the normal payload.
# Define a dictionary containing your settings.
# Add it to the original payload.



### Example
prompt = "white background, sugimori ken \\(style\\), pokemon \\(creature\\), full body, tornado creature with smoke tentacles and a menacing face solo, grin, happy, highres, no humans, other focus, pokemon, smile, solo, teeth, uneven eyes, ((masterpiece)) <lora:pokemon_v3_offset:1>",
negative_prompt = "(painting by bad-artist-anime:0.9), (painting by bad-artist:0.9), watermark, text, error, blurry, jpeg artifacts, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, artist name, (worst quality, low quality:1.4), bad anatomy",
overlap:int=64 
upscaler:str="R-ESRGAN 4x+ Anime6B"
denoise_str=0.75 
prompt:str='test' 
negative_prompt:str=' ' 
width:int=512 
height:int=512 
cfg_scale:float=7.5 
model:str='PastelMix.safetensors' 
sampler:str='Euler' 
steps:int=25 
n_iter:int=1 
vae:str="vae-ft-ema-560000-ema-pruned.safetensors"
#SCRIPT CONFIG
scale:int=2 
overlap:int=64 
upscaler:str="R-ESRGAN 4x+ Anime6B"



json_settings = {
    "prompt": prompt,
    'sd_model_checkpoint': model,
    "sd_vae": vae,
}



json_payload={
  "init_images": [image],
  "denoising_strength": denoise_str,
  "prompt": prompt,
  "n_iter": n_iter,
  "steps": steps,
  "cfg_scale": cfg_scale,
  "width": width,
  "height": height,
  "negative_prompt": negative_prompt,
  'override_settings': json_settings, # looks like 
  "sampler_index": sampler,
  "script_name": "sd upscale",
  "script_args": [overl ap,scale, upscaler]
}

