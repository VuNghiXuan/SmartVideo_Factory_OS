import streamlit as st
import streamlit.components.v1 as components
import json
import os
import sys

# Fix path để nhận diện folder core/templates
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from templates.template_manager import TemplateManager 

st.set_page_config(layout="wide", page_title="Template Lab - Full Height Preview")

# CSS để tối ưu không gian hiển thị
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    /* Loại bỏ viền trắng mặc định của iframe và đổ bóng cho sang */
    iframe { 
        border: none !important; 
        border-radius: 12px; 
        box-shadow: 0 20px 50px rgba(0,0,0,0.7); 
        background-color: #1e1e1e;
    }
    .stMarkdown h3 { margin-bottom: -10px; padding-top: 20px; }
    </style>
""", unsafe_allow_html=True)

def main():
    st.title("🚀 Pro Visual Previewer")
    st.caption("Chế độ hiển thị Full-Scale: Xem trọn bộ giao diện 1080p không cần cuộn chuột")

    # 1. Khu vực nhập liệu
    with st.sidebar:
        st.header("⚙️ Cấu hình")
        filename = st.text_input("Tên file giả lập:", "Project_Thanh_Vu")
        scale_val = st.slider("Tỉ lệ Scale (0.1 - 1.0):", 0.1, 1.0, 0.46)
        st.info("Mẹo: Dùng scale 0.46 để hiển thị vừa khít trên màn hình Laptop.")

    test_content = st.text_area(
        "Nội dung kịch bản (Text/Code):",
        value="Hôm nay Vũ sẽ hướng dẫn Python ghi dữ liệu tự động vào Excel cực nhanh...",
        height=100
    )
    
    st.divider()

    # 2. Danh sách mẫu (Bao gồm cả Terminal và Folder mới tách)
    all_types = ["excel", "vsc", "terminal", "folder", "chrome"]
    
    # 3. Render Grid 2 cột
    cols = st.columns(2)
    
    # Tính toán chiều cao iframe dựa trên scale (Gốc là 950px chiều cao cửa sổ)
    iframe_height = int(1000 * scale_val) 

    for idx, t_type in enumerate(all_types):
        with cols[idx % 2]:
            st.markdown(f"### 🖼️ Preview: **{t_type.upper()}**")
            
            try:
                # Lấy mã HTML gốc từ Manager
                raw_html = TemplateManager.get_template(
                    template_type=t_type,
                    content=test_content,
                    filename=filename
                )
                
                # Bọc HTML vào một Div để Scale toàn bộ chiều cao
                # transform-origin: top left đảm bảo nó không bị lệch khung
                scaled_wrapper = f"""
                <div style="
                    width: 1710px; 
                    height: 960px; 
                    transform: scale({scale_val}); 
                    transform-origin: top left;
                    overflow: hidden;
                    border-radius: 10px;
                ">
                    {raw_html}
                </div>
                """
                
                # Hiển thị Iframe
                components.html(scaled_wrapper, height=iframe_height, scrolling=False)
                
            except Exception as e:
                st.error(f"Lỗi render {t_type}: {e}")
            
            st.divider()

if __name__ == "__main__":
    main()