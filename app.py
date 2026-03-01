import streamlit as st
import traceback # Thêm cái này để in chi tiết lỗi
from interfaces.dashboard_ui import DashboardUI
from interfaces.editor_ui import EditorUI
from interfaces.render_ui import RenderUI
from interfaces.assets_ui import AssetsUI

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="SmartVideo Factory OS", 
    page_icon="🎬", 
    layout="wide"
)

def main():
    # print("\n--- [DEBUG] Main Loop Running ---") # Log mỗi khi App load lại

    # Định nghĩa danh sách các trang
    menu_options = [
        "🏠 Dashboard", 
        "📝 Biên tập kịch bản", 
        "🎬 Render Console", 
        "📂 Kho tài nguyên"
    ]

    # Kiểm tra tín hiệu chuyển trang
    redirect_signal = st.session_state.get('redirect_to_editor')
    if redirect_signal:
        # print(f"DEBUG: Nhận được tín hiệu nhảy trang! Đang ép menu_index về 1.")
        st.session_state.menu_index = 1
        del st.session_state['redirect_to_editor']
    
    if 'menu_index' not in st.session_state:
        st.session_state.menu_index = 0

    # 2. Sidebar
    st.sidebar.title("🎮 Factory Control")
    st.sidebar.markdown("---")

    # 3. Khởi tạo các Class UI
    if 'ui_pages' not in st.session_state:
        # print("DEBUG: Khởi tạo danh sách các trang UI lần đầu.")
        st.session_state.ui_pages = {
            "🏠 Dashboard": DashboardUI(),
            "📝 Biên tập kịch bản": EditorUI(),
            "🎬 Render Console": RenderUI(),
            "📂 Kho tài nguyên": AssetsUI()
        }

    # 4. Điều hướng (Navigation) với Index linh hoạt
    # CHỖ NÀY QUAN TRỌNG: 
    # Ta thêm menu_index vào Key để khi index thay đổi, Streamlit sẽ coi đây là một Widget mới
    # và buộc phải render lại theo đúng Index ta mong muốn.
    
    selection = st.sidebar.radio(
        "Chuyển đến khu vực:", 
        menu_options,
        index=st.session_state.menu_index,
        key=f"main_nav_radio_{st.session_state.menu_index}" # Thay đổi key động ở đây
    )

    # Cập nhật menu_index
    st.session_state.menu_index = menu_options.index(selection)
    # print(f"DEBUG: User selected: {selection} (Index: {st.session_state.menu_index})")

    st.sidebar.markdown("---")
    
    # 5. Bộ não AI
    st.session_state.selected_brain = st.sidebar.selectbox(
        "LLM Provider", 
        ["Groq", "Gemini", "Ollama"],
        index=0
    )

    # 6. Hiển thị trang
    page = st.session_state.ui_pages[selection]
    
    try:
        # print(f"DEBUG: Calling display() for {selection}")
        page.display()
    except Exception as e:
        # In lỗi chi tiết ra Terminal để mày fix code cho dễ
        # print(f"❌ ERROR in {selection}:")
        traceback.print_exc() 
        # Hiện lỗi lên giao diện web
        st.error(f"❌ Lỗi khi hiển thị trang {selection}: {e}")
        st.info("Xem chi tiết lỗi trong Terminal (cửa sổ đen CMD).")

if __name__ == "__main__":
    main()