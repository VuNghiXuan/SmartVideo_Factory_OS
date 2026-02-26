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
            # Logic này sẽ đọc từ data/catalog.json mà CourseManager quản lý
            catalog = self.manager.get_catalog()
            if not catalog['courses']:
                st.info("Chưa có khóa học nào. Hãy tạo khóa học đầu tiên ở bên phải! ➡️")
            else:
                for course in catalog['courses']:
                    with st.expander(f"📘 {course['name']}"):
                        st.write(f"ID: {course['id']}")
                        if st.button(f"Vào biên tập {course['id']}"):
                            st.session_state.selected_course = course['id']
                            st.toast(f"Đã chọn {course['name']}")

        with col2:
            st.subheader("🆕 Tạo khóa học mới")
            new_name = st.text_input("Tên khóa học", placeholder="Ví dụ: Python Cơ Bản")
            if st.button("Khởi tạo ngay", type="primary"):
                if new_name:
                    new_id = new_name.lower().replace(" ", "_")
                    self.manager.add_course(new_id, new_name)
                    st.success("Đã tạo khóa học thành công!")
                    st.rerun()