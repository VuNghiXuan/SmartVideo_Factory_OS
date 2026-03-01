import streamlit as st
import asyncio
import os
import json
import traceback
from main_orchestrator import MainOrchestrator

class RenderUI:
    def __init__(self):
        self.orchestrator = MainOrchestrator()

    def display(self):
        st.header("🎬 Render Console")
        st.write("Cấu hình và theo dõi quá trình xuất video.")

        # 1. Lấy dữ liệu từ Session State
        raw_script = st.session_state.get('current_script', [])
        active_course_id = st.session_state.get('selected_course', "")
        
        # 2. XỬ LÝ ÉP KIỂU SCRIPT_DATA
        script_data = []
        if isinstance(raw_script, str) and raw_script.strip():
            try:
                script_data = json.loads(raw_script)
            except Exception as e:
                st.error(f"❌ Lỗi định dạng JSON kịch bản: {e}")
                st.info("Hãy quay lại tab Biên tập để đảm bảo kịch bản là một mảng [] đúng chuẩn.")
                return
        else:
            script_data = raw_script

        # Kiểm tra nếu kịch bản vẫn rỗng sau khi xử lý
        if not script_data or len(script_data) == 0:
            st.warning("⚠️ Chưa có nội dung kịch bản để Render. Hãy soạn bài trước!")
            return

        # 3. GIAO DIỆN CẤU HÌNH
        col1, col2 = st.columns(2)
        with col1:
            # Không dùng mặc định KHOA_01 nữa, lấy trực tiếp từ cái đang chọn
            course_id = st.text_input("Course ID (Thư mục gốc)", value=active_course_id)
            lesson_id = st.text_input("Lesson ID (Tên bài)", value="bai_moi_nhat")
            
            if not course_id:
                st.warning("❗ Vui lòng nhập hoặc chọn Course ID để định danh file.")
        
        with col2:
            st.info(f"📋 Tổng số phân cảnh phát hiện: {len(script_data)}")
            with st.expander("🔍 Xem trước cấu trúc kịch bản gửi đi"):
                st.json(script_data)

        # # 4. NÚT START PRODUCTION
        # 4. NÚT START PRODUCTION
        if st.button("🚀 START PRODUCTION", type="primary", disabled=not course_id):
            status_placeholder = st.empty()
            progress_bar = st.progress(0) # Khởi tạo thanh progress ban đầu

            # Hàm callback để cập nhật giao diện mỗi khi xong 1 phân cảnh
            def update_progress(percent, message):
                progress_bar.progress(percent)
                status_placeholder.info(f"⚙️ **Tiến độ:** {message}")

            async def run_render():
                try:
                    # Bước 1: Chuẩn bị dữ liệu
                    status_placeholder.info("⏳ 1/3: Đang khởi tạo tài nguyên và kiểm tra kịch bản...")
                    if isinstance(script_data, str):
                        final_script = json.loads(script_data)
                    else:
                        final_script = script_data
                    
                    progress_bar.progress(5) # Nhích nhẹ một tí cho người dùng biết máy đang chạy

                    # Bước 2: Chạy Production và truyền callback update_progress vào
                    # Lúc này thanh progress sẽ nhảy tự động theo từng Scene nhờ Orchestrator gọi update_progress
                    output_path = await self.orchestrator.run_production(
                        script_data=final_script,
                        course_id=course_id,
                        lesson_id=lesson_id,
                        progress_callback=update_progress  # <--- Quan trọng nhất là dòng này
                    )
                    
                    # Bước 3: Hoàn tất
                    if output_path:
                        progress_bar.progress(100)
                        status_placeholder.success("✅ 3/3: Đã gộp video hoàn tất!")
                    return output_path

                except Exception as e:
                    print(f"❌ RENDER CRITICAL ERROR:\n{traceback.format_exc()}")
                    st.error(f"🔥 Lỗi hệ thống Render: {str(e)}")
                    progress_bar.empty() 
                    return None

            # Thực thi luồng Render
            try:
                result_path = asyncio.run(run_render())
                
                if result_path:
                    st.balloons() # Hiệu ứng chúc mừng
                    st.success(f"🎉 Video đã sẵn sàng tại: {result_path}")
                    if os.path.exists(result_path):
                        st.video(result_path)
            except Exception as outer_e:
                st.error(f"Lỗi thực thi Async: {outer_e}")