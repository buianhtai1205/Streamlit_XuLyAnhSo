from subprocess import call

def open_my_file(fileOpen):
    call(["python", fileOpen])


import streamlit as st
from streamlit_option_menu import option_menu

import NhanDangKhuonMat.Buoc1.get_face as get_face
import NhanDangKhuonMat.Buoc3.predict as predict

import XuLyAnhSo.XyLyAnh as xulyanh

import NhanDangTraiCay.detect as detectFruit

class Main():
    def __init__(self):
        self.initUI()

    def initUI(self):
        with st.sidebar:
            st.sidebar.header = "Menu"
            selected = option_menu("Main Menu", ["Nhận dạng khuôn mặt", "Xử lý hình ảnh", "Nhận dạng trái cây"],
                                   icons=['bookmark-star', 'apple', 'star'], menu_icon="grid-1x2-fill", default_index=0)

        if selected == "Nhận dạng khuôn mặt":
            st.title("Nhận dạng khuôn mặt")
            col1, col2 = st.columns([0.5, 0.5], gap="large")
            with col1:
                option = st.selectbox("Function", (
                    "None", "Phát hiện khuôn mặt", "Nhận dạng khuôn mặt"))

                if option == "None":
                    st.write("Vui lòng chọn option!")
                if option == "Phát hiện khuôn mặt":
                    st.write(
                        "Tiến hàng phát hiện khuôn mặt thông qua camera")
                if option == "Nhận dạng khuôn mặt":
                    st.write(
                        "Tiến hàng nhận dạng khuôn mặt thông qua model đã được training")

            with col2:
                if option == "Phát hiện khuôn mặt":
                    get_face.runGetFace()
                if option == "Nhận dạng khuôn mặt":
                    predict.runPredict()

        if selected == "Xử lý hình ảnh":
            # Chọn thông tin file image
            uploaded_files = st.sidebar.file_uploader("Chọn file image", type=['csv', 'png', 'tif', 'jpg'])
            # Gọi hàm thực thi xử lý tính năng
            xulyanh.XuLyUploadFile(uploaded_files)

        if selected == "Nhận dạng trái cây":
            model = detectFruit.load_model()
            detectFruit.main(model)

p = Main()
