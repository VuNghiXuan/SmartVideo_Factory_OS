"""interfaces/base_ui.py (Class Cha - Bản thiết kế chuẩn)
File này định nghĩa những gì mà một "Tab giao diện" cần phải có."""

import streamlit as st
from abc import ABC, abstractmethod

class BaseInterface(ABC):
    def __init__(self, title):
        self.title = title

    @abstractmethod
    def display(self):
        """Mọi class con phải có hàm này để hiển thị nội dung"""
        pass

    def render_header(self):
        st.title(f"🚀 {self.title}")
        st.divider()