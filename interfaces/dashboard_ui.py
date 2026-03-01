import streamlit as st
from core.course_manager import CourseManager

class DashboardUI:
    def __init__(self):
        self.manager = CourseManager()

    def display(self):
        st.title("🚀 Quản lý Khóa học")
        st.markdown("---")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📚 Danh sách khóa học hiện có")
            # Đọc catalog chuẩn từ CourseManager
            catalog = self.manager.get_catalog()
            
            if not catalog['courses']:
                st.info("Chưa có khóa học nào. Hãy tạo khóa học đầu tiên ở bên phải! ➡️")
            else:
                for course in catalog['courses']:
                    with st.expander(f"📘 {course['name']}"):
                        st.write(f"ID: {course['id']}")
                        
                        # Nút bấm để chuyển sang trình biên tập
                        if st.button(f"Vào biên tập {course['id']}", key=f"btn_{course['id']}"):
                            # 1. Lưu ID khóa học vào bộ nhớ để EditorUI biết đường load file
                            st.session_state.selected_course = course['id'] 
                            
                            # 2. Phát tín hiệu cho main.py biết là cần nhảy sang trang Editor
                            # (Tên biến phải khớp với logic kiểm tra ở main.py)
                            st.session_state.redirect_to_editor = True   
                            
                            # 3. Toast thông báo cho xịn xò
                            st.toast(f"Đang mở: {course['name']}...")
                            
                            # 4. Ép Streamlit chạy lại để main.py bắt được tín hiệu và chuyển trang
                            st.rerun() 

        with col2:
            st.subheader("🆕 Tạo khóa học mới")
            new_name = st.text_input("Tên khóa học", placeholder="Ví dụ: Python Cơ Bản")
            if st.button("Khởi tạo ngay", type="primary", use_container_width=True):
                if new_name:
                    # Tạo ID sạch sẽ (không dấu, không khoảng trắng)
                    new_id = new_name.lower().replace(" ", "_")
                    self.manager.add_course(new_name) # Hàm add_course của mày tự lo phần ID rồi
                    st.success(f"Đã tạo khóa học '{new_name}' thành công!")
                    st.rerun()
                else:
                    st.warning("Vui lòng nhập tên khóa học!")