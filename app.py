import streamlit as st
from interfaces.dashboard_ui import DashboardUI
from interfaces.editor_ui import EditorUI
from interfaces.render_ui import RenderUI
from interfaces.assets_ui import AssetsUI

# 1. Cấu hình trang Streamlit (Phải là lệnh đầu tiên)
st.set_page_config(
    page_title="SmartVideo Factory OS", 
    page_icon="🎬", 
    layout="wide"
)

def main():
    # 2. Sidebar - Tiêu đề hệ thống
    st.sidebar.title("🎮 Factory Control")
    st.sidebar.markdown("---")

    # 3. Khởi tạo các Class UI
    # Việc khởi tạo này giúp giữ trạng thái (State) của từng trang riêng biệt
    if 'ui_pages' not in st.session_state:
        st.session_state.ui_pages = {
            "🏠 Dashboard": DashboardUI(),
            "📝 Biên tập kịch bản": EditorUI(),
            "🎬 Render Console": RenderUI(),
            "📂 Kho tài nguyên": AssetsUI()
        }

    # 4. Sidebar - Điều hướng (Navigation)
    selection = st.sidebar.radio(
        "Chuyển đến khu vực:", 
        list(st.session_state.ui_pages.keys())
    )

    st.sidebar.markdown("---")
    
    # 5. Cấu hình Bộ não (LLM) dùng chung cho toàn hệ thống
    st.sidebar.subheader("🧠 System Brain")
    st.session_state.selected_brain = st.sidebar.selectbox(
        "LLM Provider", 
        ["Groq", "Gemini", "Ollama"],
        index=0,
        help="Chọn bộ não AI sẽ xử lý viết kịch bản và phân tích logic."
    )

    # 6. Hiển thị trang được chọn
    page = st.session_state.ui_pages[selection]
    
    try:
        page.display()
    except Exception as e:
        st.error(f"❌ Lỗi khi hiển thị trang {selection}: {e}")
        st.info("Có thể file Class này chưa được định nghĩa logic bên trong.")

if __name__ == "__main__":
    main()