from flask import Flask, jsonify, request
import requests
import json
import cv2
import base64
app = Flask(__name__)
url = "http://127.0.0.1:7869"


@app.route('/i2i', methods=['POST'])
"""
    image to image API
"""
def i2i():
    # 사용자에게 입력 받은 데이터
    params = json.loads(request.get_data(), encoding='utf-8')
    # 입력 받은 데이터가 없을 시 'No parameter' 반환
    if len(params) == 0:
        return 'No parameter'
    try:
        # 생성 이미지의 베이스 이미지
        base = './base.png'       # Second img = base img
        img2 = cv2.imread(base)


        # 이미지 데이터를 base64를 통해 encode
        retval, bytes = cv2.imencode('.png', img2)
        image_base = base64.b64encode(bytes).decode('utf-8')

        # 생성 이미지 모델의 파라미터를 사용자에게 받은 값에 따라 정의
        ## 여자일 경우
        if params["gender"] == "woman":
            gender1 = "1girl"
            gender2 = "female"
        ## 남자일 경우
        else:
            gender1 = "handsome male"
            gender2 = "1boy"
        # 생성 이미지 프롬 프트
        prompt = f"({gender1}:2), (professional photograph of a stunning korean), front shot,upper body, dramatic, film grain,  blurry foreground, bokeh, (depth of field, interaction, sharp focus, smiling, casual wear), (masterpiece:1.4), extremely intricate, ultra realistic, highly detailed, professional color graded, best quality,ultra highres,photorealistic,RAW photo,HDR,uhd,4k,8k,telephoto lens,<lora:add_detail:1>, (clear brown background:1.4), {gender2}, portrait, front"
        negative_prompt = "nsfw, paintings, sketches, (low quality:2),(normal quality:2),(worst quality:2),lowres,((monochrome)),((grayscale)),acnes,skin spots,age spot,skin blemishes,bad feet,((wrong feet)),(wrong shoes),bad hands,distorted,blurry,missing fingers,multiple feet,bad knees,extra fingers,, body hair, bad eye, bad focus, Accessories, bad-picture-chill-75v, easynegative, ng_deepnegative_v1_75t"
        ## 모델
        model = "majicmixRealistic_v7.safetensors"
        ## 체크 포인트 및 세부 설정
        vae = "vae-ft-mse-840000-ema-pruned.ckpt"
        sampler_name = "DPM++ 2M Karras"         #"Euler a"    #"Euler"    #"DPM++ 2M Karras"  #"DPM++ SDE Karras"
        steps = 35
        denoising_strength = 0.65


        ## Reactor
        args=[
            image_base, #0  ## Img
            True, #1 Enable ReActor
            '0', #2 Comma separated face number(s) from swap-source image
            '0', #3 Comma separated face number(s) for target image (result)
            'inswapper_128.onnx', #4 model path
            'CodeFormer', #4 Restore Face: None; CodeFormer; GFPGAN
            1, #5 Restore visibility value
            True, #7 Restore face -> Upscale
            '4x-UltraSharp', #8 Upscaler (type 'None' if doesn't need), see full list here: http://127.0.0.1:7860/sdapi/v1/script-info -> reactor -> sec.8
            2, #9 Upscaler scale value  # 2time or 4 times
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
            1, #22 Select Source, 0 - Image, 1 - Face Model
            "elena.safetensors", #23 Filename of the face model (from "models/reactor/faces"), e.g. elena.safetensors
        ]


        ## Adetailer parameter
        args_ad=[
            # True,
            # False,
            {
                "ad_model": "face_yolov8n.pt",
                    "ad_prompt": f"sharp focus, smile, {gender2}",
                    "ad_negative_prompt": "bad eyes",
                    "ad_confidence": 0.3,
                    "ad_mask_k_largest": 0,
                    "ad_mask_min_ratio": 0.0,
                    "ad_mask_max_ratio": 1.0,
                    "ad_dilate_erode": 32,
                    "ad_x_offset": 0,
                    "ad_y_offset": 0,
                    "ad_mask_merge_invert": "None",
                    "ad_mask_blur": 4,
                    "ad_denoising_strength": 0.4,
                    "ad_inpaint_only_masked": True,
                    "ad_inpaint_only_masked_padding": 0,
                    "ad_use_inpaint_width_height": False,
                    "ad_inpaint_width": 512,
                    "ad_inpaint_height": 512,
                    "ad_use_steps": False,
                    "ad_steps": steps + 5,
                    "ad_use_cfg_scale": False,
                    "ad_cfg_scale": 7.0,
                    "ad_use_sampler": False,
                    "ad_sampler": sampler_name,
                    "ad_use_noise_multiplier": False,
                    "ad_noise_multiplier": 1.0,
                    "ad_use_clip_skip": False,
                    "ad_clip_skip": 1,
                    "ad_restore_face": False,
                    "ad_controlnet_model": "None",
                    "ad_controlnet_module": "None",
                    "ad_controlnet_weight": 1.0,
                    "ad_controlnet_guidance_start": 0.0,
                    "ad_controlnet_guidance_end": 1.0
            }
        ]





        payload = {
            "init_images" : params["init_images"]
            ,
            "width": 768,
            "height": 960,
            "denoising_strength" : denoising_strength,
            "prompt" : prompt,
            "negative_prompt": negative_prompt,
            "steps": 35,
            "cfg_scale": 7,
            "sampler_name": sampler_name,
            "alwayson_scripts": {
                "ADetailer":{
                    "args": args_ad
                },
                "reactor":{
                    "args": args
                },
            }
        }

        override_settings = {}
        override_settings["CLIP_stop_at_last_layers"] = 2
        override_settings["sd_model_checkpoint"] = model
        override_settings["sd_vae"] = vae
        override_payload = {
                        "override_settings": override_settings
                    }
        payload.update(override_payload)


        # webapi에 이미지 생성 요청
        response = requests.post(url=f'{url}/sdapi/v1/img2img', json=payload)
        r = response.json()
        # 생성된 이미지 값을 사용자에게 전달
        return jsonify({"images": f"{r['images']}",})

    except Exception as e:
        return jsonify({"error": str(e)})






if __name__ == '__main__':
    #  프라이빗 아이피의 개방한 포트로 flask api 실행
    app.run(port=7860, host='192.168.0.7')