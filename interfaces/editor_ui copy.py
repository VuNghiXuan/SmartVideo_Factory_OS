import streamlit as st
import json
import os
import shutil
import asyncio
import re
import traceback
from .base_ui import BaseInterface
from core.course_manager import CourseManager
from core.llm_factory import LLMProvider
from core.memory import LongTermMemory
from core.classifier import SceneClassifier
from main_orchestrator import MainOrchestrator
from config import config

class EditorUI(BaseInterface):
    def __init__(self):
        super().__init__("Biên tập & Sản xuất thông minh")
        self.manager = CourseManager()
        self.orchestrator = MainOrchestrator()
        self.courses_dir = config.COURSES_DIR
        self.workspace_dir = config.WORKSPACE_DIR

    def extract_clean_json(self, text):
        """Hàm lọc sạch mọi rác rưởi quanh JSON để tránh lỗi 'str' object"""
        try:
            # Tìm cặp ngoặc nhọn bao quanh nội dung chính
            match = re.search(r'({.*})', text, re.DOTALL)
            if match:
                clean_content = match.group(1)
                return json.loads(clean_content)
            return json.loads(text)
        except Exception:
            return None

    def display(self):
        left_col, right_col = st.columns([1, 1.3], gap="large")

        with left_col:
            st.subheader("🛠️ Cấu hình & Soạn thảo")
            
            # 1. Lấy Catalog và tính toán Khóa học mặc định
            catalog = self.manager.get_catalog()
            course_names = [c['name'] for c in catalog['courses']]
            course_options = {c['name']: c['id'] for c in catalog['courses']}
            all_course_list = ["-- Chọn khóa học --"] + course_names
            
            # Tính Index khóa học (Tránh lỗi Unbound)
            default_course_idx = 0
            if len(all_course_list) > 1:
                if st.session_state.get('sb_course') is None:
                    default_course_idx = len(all_course_list) - 1
                elif st.session_state.get('sb_course') in all_course_list:
                    default_course_idx = all_course_list.index(st.session_state['sb_course'])

            selected_course_name = st.selectbox(
                "📂 1. Chọn Khóa học", 
                all_course_list,
                index=default_course_idx,
                key="sb_course"
            )
            
            selected_course_id = course_options.get(selected_course_name)
            st.session_state['active_course_id_internal'] = selected_course_id

            # 2. Xử lý bài học (Chapters)
            chapter_list = self.get_chapters_list(selected_course_id)
            target_chapter_idx = self.get_last_chapter_index(chapter_list)
            
            # --- ĐOẠN NÀY LÀ CHỖ GÂY LỖI TRƯỚC ĐÓ ---
            # Thay vì gán trực tiếp st.session_state['selectbox_chapter'] = ... (gây lỗi API)
            # Ta chỉ load nội dung kịch bản nếu index hợp lệ
            if target_chapter_idx > 0:
                current_chap = chapter_list[target_chapter_idx]
                # Chỉ load khi bài học thực sự thay đổi để tránh loop
                if st.session_state.get('last_loaded_chap') != current_chap:
                    self.load_script_content(selected_course_id, current_chap)
                    st.session_state['last_loaded_chap'] = current_chap

            st.selectbox(
                "📖 2. Mở bài học cũ", 
                chapter_list, 
                index=target_chapter_idx, 
                key="selectbox_chapter", 
                on_change=self.handle_chapter_change
            )

            st.divider()

           
            
            # Trợ lý AI
            st.subheader("🤖 Trợ lý AI")
            lesson_name = st.text_input("📍 Tên bài học mới:", placeholder="Ví dụ: 01_Excel_Python", key="new_lesson_input")
            topic = st.text_area("💡 Ý tưởng kịch bản:", placeholder="Dán nội dung thô vào đây...", height=100)
            
             # --- THÊM CHỌN GIỌNG ĐỌC Ở ĐÂY ---
            
            st.write("🎙️ Cấu hình giọng đọc")
            voice_map = {
                "Hoài Mỹ (Nữ - Miền Nam)": "vi-VN-HoaiMyNeural",
                "Nam Minh (Nam - Miền Bắc)": "vi-VN-NamMinhNeural"
            }
            selected_voice_label = st.selectbox(
                "Chọn giọng thuyết minh:", 
                list(voice_map.keys()),
                key="selected_voice_label"
            )
            # Lưu mã voice vào session_state để dùng khi Render
            st.session_state['selected_voice_id'] = voice_map[selected_voice_label]
            st.divider()
            # --------------------------------

            
            btn_c1, btn_c2, btn_c3 = st.columns([1, 1, 1])

            
            
            with btn_c1:
                if st.button("🪄 Soạn AI", use_container_width=True, type="primary"):
                    if not selected_course_id or not topic:
                        st.error("Thiếu khóa học hoặc ý tưởng!")
                    else:
                        with st.spinner("AI đang soạn JSON..."):
                            selected_brain = st.session_state.get('selected_brain', 'groq')
                            try:
                                llm = LLMProvider(selected_brain)
                                # prompt = f"Viết kịch bản video chuyên nghiệp dạng JSON cho chủ đề: {topic}. Yêu cầu: Trả về duy nhất đối tượng JSON, có key 'title', 'description', 'sections' (list các dict có 'title' và 'content'), và 'code' (list các dict 'language' và 'code')."
                                prompt = f"""
                                        Soạn kịch bản video JSON cho nội dung: {topic}. 
                                        YÊU CẦU CẤU TRÚC JSON CHÍNH XÁC NHƯ SAU:
                                        {{
                                        "title": "Tên bài học",
                                        "description": "Mô tả ngắn",
                                        "sections": [
                                            {{
                                            "title": "Tiêu đề cảnh 1",
                                            "text": "Nội dung thuyết minh cảnh 1",
                                            "content": "Nội dung hiển thị trên slide"
                                            }},
                                            {{
                                            "title": "Tiêu đề cảnh 2",
                                            "text": "Nội dung thuyết minh cảnh 2",
                                            "content": "Nội dung hiển thị trên slide"
                                            }}
                                        ]
                                        }}
                                        CHỈ TRẢ VỀ JSON, không giải thích gì thêm.
                                        """
                                raw_res = llm.ask(prompt)
                                json_data = self.extract_clean_json(raw_res)
                                
                                if json_data:
                                    st.session_state.current_script = json.dumps(json_data, indent=4, ensure_ascii=False)
                                    st.rerun()
                                else:
                                    st.error("AI không trả về JSON chuẩn. Thử lại lần nữa Vũ ơi!")
                            except Exception as e:
                                st.error(f"Lỗi AI: {str(e)}")

            with btn_c2:
                if st.button("🔍 Tìm bài cũ", use_container_width=True):
                    if selected_course_id and topic:
                        with st.spinner("Đang lục kho..."):
                            match = self.manager.find_lesson_by_prompt(topic, selected_course_id)
                            if match and match.get('title'):
                                lesson_folder = match['title']
                                script_path = os.path.join(self.courses_dir, selected_course_id, "chapters", lesson_folder, "script.json")
                                if os.path.exists(script_path):
                                    with open(script_path, 'r', encoding='utf-8') as f:
                                        st.session_state.current_script = f.read()
                                    st.toast(f"🎯 Đã tìm thấy: {lesson_folder}")
                                    st.rerun()
                    else: st.warning("Cần khóa học và ý tưởng!")

            with btn_c3:
                if st.button("🗑️ Xoá bài", use_container_width=True):
                    sel_chap = st.session_state.get('selectbox_chapter')
                    if sel_chap and sel_chap != "-- Chọn bài --":
                        # Đảm bảo có path tuyệt đối chuẩn
                        target_del_path = os.path.join(self.courses_dir, selected_course_id, "chapters", sel_chap)
                        if os.path.exists(target_del_path):
                            shutil.rmtree(target_del_path)
                            # RESET AN TOÀN: Dùng rerun để Streamlit tự dọn dẹp state
                            if 'last_loaded_chap' in st.session_state:
                                del st.session_state['last_loaded_chap']
                            st.rerun()

        # ================= LỀ PHẢI: BIÊN TẬP & RENDER =================
        with right_col:
            if "current_script" in st.session_state:
                st.subheader("📝 Biên tập kịch bản JSON")
                edited_script = st.text_area("Chỉnh sửa thủ công:", value=st.session_state.current_script, height=450)
                st.session_state.current_script = edited_script

                btn_save, btn_render = st.columns(2)
                
                with btn_save:
                    if st.button("💾 LƯU BÀI HỌC", use_container_width=True):
                        final_name = lesson_name.strip() if lesson_name else st.session_state.get('selectbox_chapter')
                        if final_name and final_name != "-- Chọn bài --":
                            path = os.path.join(self.courses_dir, selected_course_id, "chapters", final_name)
                            os.makedirs(path, exist_ok=True)
                            with open(os.path.join(path, "script.json"), "w", encoding="utf-8") as f:
                                f.write(edited_script)
                            st.success(f"✅ Đã lưu!")
                            st.rerun()
                        else: st.error("Thiếu tên bài!")

                with btn_render:
                    if st.button("🚀 RENDER VIDEO", use_container_width=True, type="primary"):
                        # 1. Lấy ID khóa học và bài học
                        sel_course_id = st.session_state.get('active_course_id_internal')
                        final_lesson_id = lesson_name.strip() if lesson_name else st.session_state.get('selectbox_chapter', 'temp_lesson')
                        
                        # --- FIX LỖI 1: LẤY GIỌNG ĐỌC TỪ SESSION STATE ---
                        selected_voice = st.session_state.get('selected_voice_id', config.DEFAULT_VOICE)

                        if not sel_course_id:
                            st.error("Chưa chọn khóa học!")
                        elif not edited_script.strip():
                            st.error("Kịch bản trống!")
                        else:
                            async def run_production_ui():
                                try:
                                    js_dict = json.loads(edited_script)
                                    
                                    # TRUYỀN THÊM THAM SỐ voice=selected_voice VÀO ĐÂY
                                    return await self.orchestrator.run_production(
                                        js_dict, 
                                        sel_course_id, 
                                        final_lesson_id,
                                        voice=selected_voice
                                    )
                                
                                except json.JSONDecodeError as e:
                                    st.error(f"Lỗi cú pháp JSON! ({e})")
                                    return None
                                except Exception as e:
                                    st.error(f"Lỗi Render: {str(e)}")
                                    st.expander("Chi tiết lỗi").code(traceback.format_exc())
                                    return None

                            with st.spinner("🎬 Đang sản xuất video..."):
                                video_result = asyncio.run(run_production_ui())
                                
                                # --- FIX LỖI 2: XỬ LÝ TUPLE TRẢ VỀ ---
                                if video_result:
                                    # Nếu video_result là tuple (path, metadata), lấy phần tử 0
                                    actual_video_path = video_result[0] if isinstance(video_result, tuple) else video_result
                                    
                                    if actual_video_path and os.path.exists(actual_video_path):
                                        st.success("Render xong rồi Vũ ơi!")
                                        st.video(actual_video_path)
                                    else:
                                        st.error("Không tìm thấy file video sau khi render!")
            else:
                st.info("👈 Hãy chọn hoặc soạn bài để bắt đầu.")