import streamlit as st
import asyncio
import os
from main_orchestrator import MainOrchestrator

class RenderUI:
    def __init__(self):
        self.orchestrator = MainOrchestrator()

    def display(self):
        st.header("🎬 Render Console")
        st.write("Cấu hình và theo dõi quá trình xuất video.")

        # Lấy dữ liệu kịch bản từ Session State (giả sử đã soạn ở EditorUI)
        script_data = st.session_state.get('current_script', [])
        
        if not script_data:
            st.warning("⚠️ Chưa có kịch bản nào được soạn. Hãy qua tab '📝 Biên tập kịch bản' trước.")
            return

        col1, col2 = st.columns(2)
        with col1:
            course_id = st.text_input("Course ID", value="KHOA_01")
            lesson_id = st.text_input("Lesson ID", value="BAI_01")
        
        with col2:
            st.write("Thông tin kịch bản:")
            st.json(script_data)

        if st.button("🚀 START PRODUCTION", type="primary"):
            status_placeholder = st.empty()
            progress_bar = st.progress(0)
            
            async def run_render():
                status_placeholder.info("⏳ Đang chuẩn bị hệ thống...")
                try:
                    output_path = await self.orchestrator.run_production(
                        script_data=script_data,
                        course_id=course_id,
                        lesson_id=lesson_id
                    )
                    return output_path
                except Exception as e:
                    st.error(f"Lỗi Render: {e}")
                    return None

            # Chạy render
            result_path = asyncio.run(run_render())

            if result_path:
                st.success(f"✅ Video đã sẵn sàng: {result_path}")
                st.video(result_path)