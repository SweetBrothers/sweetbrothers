import requests
from PIL import Image, PngImagePlugin
import io
import base64
import json
import os

url = ""

os.chdir('/home/ds/api/outputs')
current_directory = os.getcwd()
print("ok")


        ### 파일 함수 모양.
#     def run(self, p, _, tile_width, tile_height, mask_blur, padding, seams_fix_width, seams_fix_denoise, seams_fix_padding,
#             upscaler_index, save_upscaled_image, redraw_mode, save_seams_fix_image, seams_fix_mask_blur,
#             seams_fix_type, target_size_type, custom_width, custom_height, custom_scale):

# parameter = {
#     _
#     tile_width 
#     tile_height
#     mask_blur
#     padding
#     seams_fix_width
#     seams_fix_denoise
#     seams_fix_padding
#     upscaler_index
#     save_upscaled_image
#     redraw_mode
#     save_seams_fix_image
#     seams_fix_mask_blur
#     seams_fix_type
#     target_size_type
#     custom_width
#     custom_height
#     custom_scale
# }


"script_args": ["",512,0,8,32,64,0.275,32,3,false,0,true,8,3,2,1080,1440,1.875],
"script_name": "Ultimate SD upscale"

## Provided args should start 3rd arg (ex. "" is for _, 512 is for tile_width,... )
## (except for p, that is automatically the image you specified in init_images)