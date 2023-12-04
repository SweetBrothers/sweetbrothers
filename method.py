###
# Train :
# - EasyPhoto - Train - 'Upload Photos' : Button Click 후

# 1.한 명의 얼굴 이미지를 5~20장 입력 받는다.

# 2.
# 2-1(option):Clear Photos-> 입력받았던 이미지들을 지움
# 2-2::Start Training : Button Click 후
# ID(LoRA의 이름)을 명명함 (추후 Output으로 나올)
# 약10분~30분 정도의 시간이 필요함(이미지 수 및 세팅과 연관)
# 첫 실행시 오래 걸림 이유는 The base checkpoint you use에
# Chilloutmix-Ni-pruned-fp16-fix.safetensors가 없기 때문 (SD 1.5기반)
# 학습 과정에서 Tagging등은 자동으로 이루어짐

# 3.
# 3-1. STABLE-DIFFUSION_WEBUI/models/Lora폴더에 해당 2번시 명명했던 ID.safetensors의 형태로 LoRA가 생성되었다.
# 3-2. - EasyPhoto - Photo Inference에 Single Image Upload 또는 Batch Images Upload Click 후
# 3-3. Start Generation 후 1이미지당 약 1~2분의 시간이 소요.
# 3-4 Results에서 Donwload Image.
# 3-5 Donwload Image를 Output으로 보여줌