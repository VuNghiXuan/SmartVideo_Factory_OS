import streamlit as st
from .base_ui import BaseInterface
from core.course_manager import CourseManager
from core.llm_factory import LLMProvider
from core.memory import LongTermMemory
from core.classifier import SceneClassifier
import json

class EditorUI(BaseInterface):
    def __init__(self):
        super().__init__("Biên tập kịch bản thông minh")
        self.manager = CourseManager()

    def display(self):
        self.render_header()

        # 1. Chọn Khóa học & Chương (Quản lý đa tầng)
        with st.expander("📂 Chọn bài học cần biên tập", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                with open(self.manager.catalog_path, 'r', encoding='utf-8') as f:
                    catalog = json.load(f)
                course_options = {c['name']: c['id'] for c in catalog['courses']}
                selected_course_name = st.selectbox("Khóa học", ["-- Chọn khóa học --"] + list(course_options.keys()))
                selected_course_id = course_options.get(selected_course_name)

            with col2:
                st.selectbox("Chương (Chapter)", ["Chương 1: Mở đầu", "Chương 2: Cơ bản"])
            
            with col3:
                st.selectbox("Bài học (Lesson)", ["Bài 1.1", "Bài 1.2"])

        # 2. Khu vực điều khiển AI soạn kịch bản
        st.subheader("🤖 Trợ lý Biên kịch AI")
        topic = st.text_area("Chủ đề hoặc nội dung thô:", placeholder="Ví dụ: Cách dùng vòng lặp For trong Python...")
        
        col_btn1, col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("🪄 Soạn kịch bản", use_container_width=True):
                if not selected_course_id:
                    st.error("Vui lòng chọn khóa học trước!")
                elif not topic:
                    st.warning("Vui lòng nhập chủ đề!")
                else:
                    with st.spinner(f"Đang dùng {st.session_state.selected_brain} lục lại trí nhớ và soạn bài..."):
                        # --- BƯỚC 1: TRUY VẤN TRÍ NHỚ ---
                        memory = LongTermMemory(selected_course_id)
                        old_knowledge = memory.search_context(topic)
                        context_string = " | ".join(old_knowledge) if old_knowledge else "Chưa có kiến thức cũ."

                        # --- BƯỚC 2: GỌI LLM SOẠN BÀI ---
                        llm = LLMProvider(st.session_state.selected_brain)
                        prompt = f"""
                        Bối cảnh kiến thức đã dạy: {context_string}
                        Dựa trên kiến thức đó, hãy soạn kịch bản video cho bài mới: {topic}.
                        Yêu cầu: Nếu có kiến thức liên quan bài cũ, hãy nhắc lại nhẹ nhàng.
                        Định dạng trả về: Chia thành các Scene rõ ràng. Mỗi scene gồm 'Lời thoại' và 'Hành động'.
                        """
                        st.session_state.current_script = llm.ask(prompt)

        # 3. Hiển thị & Chỉnh sửa kịch bản
        st.divider()
        if "current_script" in st.session_state:
            st.subheader("📝 Nội dung kịch bản")
            edited_script = st.text_area("Biên tập nội dung:", 
                                       value=st.session_state.current_script, 
                                       height=350)
            
            if st.button("✅ Lưu & Phân loại Module"):
                with st.spinner("Hệ thống đang phân tích module cho từng cảnh..."):
                    # --- BƯỚC 3: PHÂN LOẠI MODULE ---
                    classifier = SceneClassifier(st.session_state.selected_brain)
                    # Giả sử chúng ta tách kịch bản theo các dòng hoặc Scene (đây là logic demo)
                    module_tag = classifier.classify_scene(edited_script[:200]) # Lấy 200 ký tự đầu để nhận diện
                    
                    st.success(f"Đã lưu! Module nhận diện chủ đạo: {module_tag}")
                    
                    # --- BƯỚC 4: LƯU VÀO BỘ NHỚ ---
                    memory = LongTermMemory(selected_course_id)
                    memory.save_lesson_context("current_lesson_id", edited_script[:500]) # Lưu tóm tắt
                    st.toast("Trí nhớ đã được cập nhật!")