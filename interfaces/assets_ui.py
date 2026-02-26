import streamlit as st
from .base_ui import BaseInterface
import os
from config import config

class AssetsUI(BaseInterface):
    def __init__(self):
        super().__init__("Kho tài nguyên (Assets)")

    def display(self):
        self.render_header()
        
        tab1, tab2, tab3 = st.tabs(["🎵 Nhạc nền", "🎨 Branding", "✨ Lottie Animations"])
        
        with tab1:
            st.subheader("Quản lý âm nhạc")
            st.info("Thư mục: assets/music/")
            # Logic quét file trong folder assets/music sẽ nằm ở đây
            st.button("Tải nhạc mới lên")

        with tab2:
            st.subheader("Bộ nhận diện thương hiệu")
            st.color_picker("Màu chủ đạo khóa học", "#1E90FF")
            st.file_uploader("Upload Logo (.png)", type=['png'])

        with tab3:
            st.subheader("Icon động Lottie")
            st.write("Dùng để chèn vào các cảnh báo hoặc chú thích.")
            st.button("Quét lại kho Lottie")