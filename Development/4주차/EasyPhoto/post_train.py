import base64
import json
import os
import sys
import time
from glob import glob
from io import BytesIO
import argparse
import requests


def post_train(encoded_images, url="http://0.0.0.0:7860",user_id="test"):
    datas = json.dumps(
        {
            "user_id": user_id,  # A custom ID that identifies the trained face model
            "sd_model_checkpoint": "Chilloutmix-Ni-pruned-fp16-fix.safetensors",
            "train_mode_choose": "Train Human Lora",
            "resolution": 512,
            "val_and_checkpointing_steps": 100,
            "max_train_steps": 800,  # Training steps
            "steps_per_photos": 200,
            "train_batch_size": 1,
            "gradient_accumulation_steps": 4,
            "dataloader_num_workers": 16,
            "learning_rate": 1e-4,
            "rank": 128,
            "network_alpha": 64,
            "instance_images": encoded_images,
            "skin_retouching_bool": False,
        }
    )
    r = requests.post(f"{url}/easyphoto/easyphoto_train_forward", data=datas, timeout=1500)
    data = r.content.decode("utf-8")
    return data


if __name__ == "__main__":
    """
    There are two ways to test:
        The first: make sure the directory is full of readable images
        The second: public link of readable picture
    """
    # initiate time
    time_start = time.time()

    # parser = argparse.ArgumentParser(description="Description of your script")

    # parser.add_argument("--input_dir", type=str, default="", help="Path to the template directory")
    # parser.add_argument("--user_ids", type=str, default="test", help="Test user ids, split with space")
    # parser.add_argument("--url_id", type=str, default="http://0.0.0.0:7860", help="URL_id, split with space")

    # args = parser.parse_args()

    # input_dir = args.input_dir
    # user_ids = args.user_ids.split(" ")
    # user_id = user_ids[0]
    # url_id = args.url_id
    
    user_id = sys.argv[2] 
    url_id = sys.argv[3]


    # -------------------training procedure------------------- #
    # When there is no parameter input.
    if len(sys.argv) == 1:
        img_list = [
            "http://pai-vision-data-inner.oss-cn-zhangjiakou.aliyuncs.com/data/easyphoto/train_data/test_face_1/t1.jpg",
            "http://pai-vision-data-inner.oss-cn-zhangjiakou.aliyuncs.com/data/easyphoto/train_data/test_face_1/t2.jpg",
            "http://pai-vision-data-inner.oss-cn-zhangjiakou.aliyuncs.com/data/easyphoto/train_data/test_face_1/t3.jpg",
            "http://pai-vision-data-inner.oss-cn-zhangjiakou.aliyuncs.com/data/easyphoto/train_data/test_face_1/t4.jpg",
        ]
        encoded_images = []
        for idx, img_path in enumerate(img_list):
            encoded_image = requests.get(img_path)
            encoded_image = base64.b64encode(BytesIO(encoded_image.content).read()).decode("utf-8")
            encoded_images.append(encoded_image)

        outputs = post_train(encoded_images)
        outputs = json.loads(outputs)
        print(outputs["message"])

    # When selecting a folder as a parameter input.
    elif len(sys.argv) == 4:
        img_list = glob(os.path.join(sys.argv[1], "*"))
    #elif len(sys.argv) == 4:
        #img_list = glob(input_dir)
        encoded_images = []
        for idx, img_path in enumerate(img_list):
            with open(img_path, "rb") as f:
                encoded_image = base64.b64encode(f.read()).decode("utf-8")
                encoded_images.append(encoded_image)
        outputs = post_train(encoded_images,url_id,user_id)
        outputs = json.loads(outputs)
        print(outputs["message"])

    else:
        print("other modes except url and local read are not supported")

    # End of record time
    # The calculated time difference is the execution time of the program, expressed in minute / m
    time_end = time.time()
    time_sum = (time_end - time_start) // 60

    print("# --------------------------------------------------------- #")
    print(f"#   Total expenditure：{time_sum} minutes ")
    print("# --------------------------------------------------------- #")
