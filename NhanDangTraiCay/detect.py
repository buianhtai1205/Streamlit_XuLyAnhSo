import os
import torch
import numpy as np
from PIL import Image
from io import BytesIO
import streamlit as st


@st.cache_data(show_spinner=False)
def load_model():
    with st.spinner('Getting Neruons in Order ...'):
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='NhanDangTraiCay//weights//yolov5s.pt')
        return model


def run(model, file_path):
    # file_path = "refs/sat.png"
    results = model(file_path)
    return results


def show_detects(results):
    st.title("Results")
    st.image(results.render(), use_column_width=True)
    st.dataframe(results.pandas().xyxy[0])


def get_detect_path(results):
    img = Image.fromarray(np.squeeze(results.render()))
    buf = BytesIO()
    img.save(buf, format="JPEG")
    byte_im = buf.getvalue()
    return byte_im


def process(model, upload):
    # save upload to file
    filename = upload.name.split('.')[0]
    filetype = upload.name.split('.')[-1]
    name = len(os.listdir("NhanDangTraiCay//images")) + 1
    file_path = os.path.join('NhanDangTraiCay//images', f'{name}.{filetype}')
    with open(file_path, "wb") as f:
        f.write(upload.getbuffer())

    # predict detections and show results
    results = run(model, file_path)
    show_detects(results)

    # offer download
    detection_image = get_detect_path(results)
    st.download_button(label="Download Detections", data=detection_image,
                       file_name='{}.jpeg'.format(filename),
                       mime='image/jpeg')

    # clean up - if over 1000 images in folder, delete oldest 1
    if len(os.listdir("NhanDangTraiCay//images")) > 1000:
        oldest = min(os.listdir("NhanDangTraiCay//images"), key=os.path.getctime)
        os.remove(os.path.join("NhanDangTraiCay//images", oldest))


def main(model):

    # title
    st.title("Nhận diện trái cây với yolo5")

    # example
    if st.button("Example Image"):
        with st.spinner('Detecting and Counting Single Image...'):
            results = run(model, "NhanDangTraiCay//images//traicay.jpg")
            show_detects(results)
            if st.button("Clear Example"):
                st.markdown("")

    # upload
    upload = st.file_uploader('Upload Images/Video', type=['jpg', 'jpeg', 'png'])
    if upload is not None:
        filetype = upload.name.split('.')[-1]
        if filetype in ['jpg', 'jpeg', 'png']:
            with st.spinner('Detecting and Counting Single Image...'):
                process(model, upload)
        else:
            st.warning('Unsupported file type.')


if __name__ == '__main__':
    model = load_model()
    main(model)