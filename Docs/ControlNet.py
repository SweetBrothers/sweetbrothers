import requests         # reqeust
from PIL import Image, PngImagePlugin    # color
import io               # convert information server into a file
import base64           # convert information of image into a base64 code
import json
import os


url = "" ## always needs to check      # 고정 url.

os.chdir('/home/ds/api/outputs')
current_directory = os.getcwd()
print("ok")


# ## parameter
# args =[
#     {
#         "input_image" : image to use in this unit. Defaults to NULL,
#         "mask" : mask pixel_perfect to filter the image. defaults to null,
#         "module" : preprocessor to use on the image passed to this unit before using it for conditioning.
#           accepts values returned by the /controlnet/module_list route. defaults to "none" ,          # find and put a module 
#         "model" : name of the model to use for conditioning in this unit. accepts values returned by the /controlnet/model_list route. defaults to "None", # find and put model
#         "weight" : weight of this unit. defaults to 1,
#         "resize_mode" : how to resize the input image so as to fit the output resolution of the generation. 
#             defaults to "Scale to Fit (Inner Fit)".
#                 {Accepted values:
#                     0 or "Just Resize" : simply resize the image to the target width/height
#                     1 or "Scale to Fit (Inner Fit)" : scale and crop to fit smallest dimension. preserves proportions.
#                     2 or "Envelope (Outer Fit)" : scale to fit largest dimension. preserves proportions.},
#         "lowvram" : whether to compensate low GPU memory with processing time. defaults to false,
#         "processor_res" : resolution of the preprocessor. defaults to 64,
#         "threshold_a" : first parameter of the preprocessor. only takes effect when preprocessor accepts arguments. defaults to 64,
#         "threshold_b" : second parameter of the preprocessor, same as above for usage. defaults to 64,
#         "guidance_start" : ratio of generation where this unit starts to have an effect. defaults to 0.0,
#         "guidance_end" : ratio of generation where this unit stops to have an effect. defaults to 1.0,
#         "control_mode" : see the related issue for usage. defaults to 0. 
#                 {Accepted values:
#                     0 or "Balanced" : balanced, no preference between prompt and control model
#                     1 or "My prompt is more important" : the prompt has more impact than the model
#                     2 or "ControlNet is more important" : the controlnet model has more impact than the prompt}
#         "pixel_perfect" : enable pixel-perfect preprocessor. defaults to false
#     }
# ]


# important thing is script "alwayson_scripts"

#  one contorlnet use example
payload = {
  "init_images": ["base64..."],
  "sampler_name": "Euler",
  "alwayson_scripts": {
    "controlnet": {                                               
      "args": [
        {
          "module": "depth",                                        # dw pose  == preprocessor
          "model": "diff_control_sd15_depth_fp16 [978ef0a1]"        # model name
        }
      ]
    }
  }
}


#  Multi-controlnet use example
payload = {
    "prompt": 'your-promot',
    "sampler_index": "Euler a",
    "alwayson_scripts": {
        "controlnet": {
            "args": [
                {
                    "input_image": LR_encoded_image,
                    "model": "control_v11f1e_sd15_tile [a371b31b]",
                    "resize_mode":1,
                    "control_mode":0,
                    "weight":1,
                },
                {
                    "input_image": Depth_encoded_image,
                    "model": "control_v11f1p_sd15_depth [cfd03158]",
                    "resize_mode":1,
                    "control_mode":0,
                    "weight":1,
                }
            ]
        }
    }
}

