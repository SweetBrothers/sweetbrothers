import numpy as np
import gradio as gr

# 이미지 생성 하는 함수 아직 API가 구현이 되지 않았으므로 세피아 필터로 구현
def predict_image(img , select_model , gender):
    sepia_filter = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    sepia_img = img.dot(sepia_filter.T)
    sepia_img /= sepia_img.max()
    print(gender,select_model)
    print(img)
    return sepia_img

# gradio blocks layout사용
with gr.Blocks() as demo:
    gr.Markdown("Profile Image demo")

    # 이미지 탭 추후에 다른 탭을 추가 가능
    with gr.Tab("Image"):
        with gr.Row():
            image_input = gr.Image()
            image_output = gr.Image()
        image_button = gr.Button("Create")
    # 세부 옵션
    with gr.Accordion("Option" ,open = False):
        select_model = gr.Dropdown(["first", "second", "third"], type="value",value="second",label = "model",interactive =True)
        gender = gr.Radio(["man", "woman"], type="value" , value="woman",label="gender",interactive=True)


    image_button.click(predict_image, inputs=[image_input,select_model,gender], outputs=image_output)

# 로그인창을 거쳐가게 한다.
if __name__ == "__main__":
    demo.launch(auth=("admin","admin"))
