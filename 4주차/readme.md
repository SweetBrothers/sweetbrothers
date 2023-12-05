
post_train.py 사용법
python post_train.py input_image_path user_id url_id
ex) /home/cora3/anaconda3/envs/torch201c118/bin/python /home/cora3/vscode_project/s1bsd/post_train.py /home/cora3/vscode_project/SweetBrothers/kohya_ss/images/train/iom10 DanielleEasyP http://0.0.0.0:7860

post_infer 사용법
python post_infer.py --template_dir path --output_path path --user_ids user_id
ex) /home/cora3/anaconda3/envs/torch201c118/bin/python /home/cora3/vscode_project/s1bsd/post_infer.py --template_dir /home/cora3/vscode_project/SweetBrothers/kohya_ss/images/train/haerin_10 --output_path /home/cora3/vscode_project/SweetBrothers/kohya_ss/images/infer/haerin10 --user_ids test
