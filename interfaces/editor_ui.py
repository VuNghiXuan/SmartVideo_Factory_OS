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

    # ================= 1. CÁC HÀM LOGIC HỖ TRỢ (HELPER FUNCTIONS) =================
    
    def extract_clean_json(self, text):
        """Lọc sạch JSON từ phản hồi của AI"""
        try:
            match = re.search(r'({.*})', text, re.DOTALL)
            if match:
                return json.loads(match.group(1))
            return json.loads(text)
        except Exception:
            return None

    def get_chapters_list(self, course_id):
        """Lấy danh sách folder bài học"""
        if not course_id or course_id == "-- Chọn khóa học --": 
            return ["-- Chọn bài --"]
        path = os.path.join(self.courses_dir, course_id, "chapters")
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            return ["-- Chọn bài --"]
        chapters = sorted([d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))])
        return ["-- Chọn bài --"] + chapters

    def get_last_chapter_index(self, chapter_list):
        """Tìm vị trí bài học cuối cùng hoặc bài đang làm dở"""
        if len(chapter_list) <= 1: 
            return 0
        
        current_val = st.session_state.get('selectbox_chapter')
        
        # Nếu đã có bài trong bộ nhớ và bài đó vẫn tồn tại trong list mới -> Giữ nguyên vị trí đó
        if current_val in chapter_list and current_val != "-- Chọn bài --":
            return chapter_list.index(current_val)
        
        # Nếu chưa chọn hoặc vừa đổi khóa học -> Trỏ thẳng xuống bài cuối cùng (len - 1)
        return len(chapter_list) - 1

    def load_script_content(self, course_id, chapter_name):
        """Đọc file script.json và nạp vào session_state để Editor hiển thị"""
        if not course_id or not chapter_name or chapter_name == "-- Chọn bài --":
            st.session_state.current_script = "{}"
            return

        script_path = os.path.join(self.courses_dir, course_id, "chapters", chapter_name, "script.json")
        if os.path.exists(script_path):
            with open(script_path, 'r', encoding='utf-8') as f:
                st.session_state.current_script = f.read()
        else:
            st.session_state.current_script = "{}"

    def handle_chapter_change(self):
        """Callback chạy khi người dùng thay đổi bài học trên UI"""
        sel_chap = st.session_state.get('selectbox_chapter')
        sel_course_id = st.session_state.get('active_course_id_internal')
        self.load_script_content(sel_course_id, sel_chap)
        st.session_state.new_lesson_input = ""

    # ================= 2. GIAO DIỆN HIỂN THỊ CHÍNH =================

    def display(self):
        """Hàm chính điều phối UI"""
        # 1. Khởi tạo State ban đầu (Fix lỗi Widget)
        self._init_session_states()

        left_col, right_col = st.columns([1, 1.3], gap="large")

        with left_col:
            self._render_config_section()
            st.divider()
            self._render_ai_assistant_section()

        with right_col:
            self._render_editor_section()

    # =================================================================
    # CÁC HÀM CON TÁCH RA
    # =================================================================

    def _init_session_states(self):
        """Khởi tạo các giá trị session state cần thiết"""
        if 'sb_course' not in st.session_state:
            st.session_state['sb_course'] = "-- Chọn khóa học --"
        if 'selectbox_chapter' not in st.session_state:
            st.session_state['selectbox_chapter'] = "-- Chọn bài --"
        if 'selected_voice_id' not in st.session_state:
            st.session_state['selected_voice_id'] = "vi-VN-HoaiMyNeural"

    def _render_config_section(self):
        """Phần 1 & 2: Chọn khóa học và bài học"""
        st.subheader("🛠️ Cấu hình & Soạn thảo")
        
        # --- CHỌN KHÓA HỌC ---
        catalog = self.manager.get_catalog()
        course_names = [c['name'] for c in catalog['courses']]
        course_options = {c['name']: c['id'] for c in catalog['courses']}
        all_course_list = ["-- Chọn khóa học --"] + course_names

        # FIX LỖI: Không dùng 'index' khi đã có 'key' và gán state thủ công
        st.selectbox("📂 1. Chọn Khóa học", all_course_list, key="sb_course")
        
        selected_course_name = st.session_state.sb_course
        selected_course_id = course_options.get(selected_course_name)
        st.session_state['active_course_id_internal'] = selected_course_id

        # --- CHỌN BÀI HỌC ---
        chapter_list = self.get_chapters_list(selected_course_id)
        
        # Logic tự động load bài học cuối nếu state chưa có hoặc bị reset
        target_idx = self.get_last_chapter_index(chapter_list)
        if target_idx > 0 and st.session_state.selectbox_chapter == "-- Chọn bài --":
            st.session_state.selectbox_chapter = chapter_list[target_idx]
            self.load_script_content(selected_course_id, chapter_list[target_idx])

        st.selectbox(
            "📖 2. Mở bài học cũ", 
            chapter_list, 
            key="selectbox_chapter", 
            on_change=self.handle_chapter_change
        )

    def _render_ai_assistant_section(self):
        """Phần 3: Trợ lý AI và các nút chức năng"""
        st.subheader("🤖 Trợ lý AI")
        lesson_name = st.text_input("📍 Tên bài học mới:", key="new_lesson_input")
        topic = st.text_area("💡 Ý tưởng kịch bản:", height=100, key="topic_input")


        
        voice_map = {
            "Hoài Mỹ (Nữ - Miền Nam)": "vi-VN-HoaiMyNeural",
            "Nam Minh (Nam - Miền Bắc)": "vi-VN-NamMinhNeural"
        }
        selected_voice_label = st.selectbox("Chọn giọng thuyết minh:", list(voice_map.keys()))
        st.session_state.selected_voice_id = voice_map[selected_voice_label]

        st.divider()
        # Hàng nút chính
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🪄 Soạn AI", use_container_width=True, type="primary"):
                self._handle_ai_generate(st.session_state.active_course_id_internal, topic)
        with c2:
            if st.button("🔍 Tìm bài cũ", use_container_width=True):
                # ... (giữ nguyên logic tìm bài) ...
                pass
        with c3:
            # Nút xóa bài (có xác nhận bằng checkbox để an toàn)
            if st.checkbox("Xác nhận xóa"):
                if st.button("🗑️ Xoá bài", use_container_width=True, type="secondary"):
                    self._handle_delete_lesson(st.session_state.active_course_id_internal)

        st.divider()
        # Hàng nút hệ thống (Dọn dẹp)
        st.caption("⚙️ Quản trị hệ thống")
        s1, s2 = st.columns(2)
        with s1:
            if st.button("🧹 Dọn Cache (Workspace)", use_container_width=True):
                self._handle_clear_cache()
        with s2:
            if st.button("❌ Xóa Khóa học", use_container_width=True, help="Xóa sạch folder khóa học này"):
                self._handle_delete_course(st.session_state.active_course_id_internal)

    def _render_editor_section(self):
        """Lề phải: Editor và Nút Render"""
        if "current_script" in st.session_state:
            st.subheader("📝 Biên tập kịch bản JSON")
            edited_script = st.text_area("Chỉnh sửa:", value=st.session_state.current_script, height=450)
            st.session_state.current_script = edited_script

            b1, b2 = st.columns(2)
            with b1:
                if st.button("💾 LƯU BÀI HỌC", use_container_width=True):
                    self._handle_save_script(edited_script)
            
            with b2:
                if st.button("🚀 RENDER VIDEO", use_container_width=True, type="primary"):
                    self._handle_render_video(edited_script)
        else:
            st.info("👈 Chọn khóa học và bài học để bắt đầu soạn thảo.")

    # =================================================================
    # CÁC HÀM XỬ LÝ LOGIC (EVENT HANDLERS)
    # =================================================================

    def _handle_delete_lesson(self, course_id):
        """Xóa bài học đang chọn"""
        chapter = st.session_state.get('selectbox_chapter')
        if not course_id or not chapter or chapter == "-- Chọn bài --":
            st.error("Chưa chọn bài để xóa!")
            return

        path = os.path.join(self.courses_dir, course_id, "chapters", chapter)
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
                st.success(f"Đã xóa bài: {chapter}")
                # Reset state để UI load lại
                st.session_state.selectbox_chapter = "-- Chọn bài --"
                st.rerun()
        except Exception as e:
            st.error(f"Không thể xóa: {str(e)}")

    def _handle_delete_course(self, course_id):
        """Xóa toàn bộ folder khóa học"""
        if not course_id:
            st.error("Chưa chọn khóa học!")
            return
        
        # Hộp thoại xác nhận nhanh của Streamlit
        st.warning(f"Bạn có chắc muốn xóa TOÀN BỘ khóa học ID: {course_id}?")
        if st.button("TÔI CHẮC CHẮN, XÓA ĐI!"):
            path = os.path.join(self.courses_dir, course_id)
            try:
                shutil.rmtree(path)
                st.session_state.sb_course = "-- Chọn khóa học --"
                st.success("Đã xóa khóa học thành công!")
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi khi xóa folder: {str(e)}")

    def _handle_clear_cache(self):
        """Dọn dẹp Workspace và tất cả __pycache__ trong project"""
        try:
            # 1. Dọn Workspace (giữ nguyên logic của mày)
            if os.path.exists(self.workspace_dir):
                shutil.rmtree(self.workspace_dir)
                os.makedirs(self.workspace_dir)

            # 2. Truy quét và diệt __pycache__
            project_root = os.getcwd() # Lấy thư mục gốc của project
            deleted_count = 0
            for root, dirs, files in os.walk(project_root):
                if "__pycache__" in dirs:
                    shutil.rmtree(os.path.join(root, "__pycache__"))
                    deleted_count += 1
            
            st.success(f"🧹 Đã dọn sạch Workspace và {deleted_count} thư mục __pycache__!")
        except Exception as e:
            st.error(f"Lỗi dọn cache: {str(e)}")
            

    def _handle_ai_generate(self, course_id, topic):
        if not course_id or not topic:
            st.warning("Thiếu khóa học hoặc ý tưởng!")
            return

        with st.spinner("AI đang soạn..."):
            # 1. Khởi tạo LLM
            llm = LLMProvider(st.session_state.get('selected_brain', 'groq'))
            
            # 2. Tạo Prompt chuẩn (Viết trực tiếp ở đây cho đỡ lỗi Attribute)            
            # prompt = f"""
            #     Bạn là một Senior Solution Architect và Chuyên gia sư phạm công nghệ.
            #     Nhiệm vụ: Soạn kịch bản JSON chi tiết cho video bài giảng kỹ thuật về chủ đề: {topic}.

            #     --- YÊU CẦU CHIẾN LƯỢC UI (ÁNH XẠ TRỰC TIẾP VỚI ENGINE) ---
            #     Mỗi phần (section) PHẢI thuộc một trong các loại giao diện sau:
            #     - 'mindmap': Dùng cho MỞ ĐẦU. Hiển thị lộ trình học (Bước 1, Bước 2...). Content phải là danh sách các bước, xuống dòng bằng \\n.
            #     - 'terminal': Màn hình Console toàn phần. Dùng để cài đặt thư viện (pip install...). Content là lệnh thực tế.
            #     - 'vsc': Giao diện Editor. Dùng để viết code Python. Content là đoạn mã Python sạch.
            #     - 'cmd_overlay': Cửa sổ lệnh hiện đè lên VSC. Dùng để CHẠY code (python main.py) và xem log output.
            #     - 'excel': Giao diện bảng tính. Dùng để trình bày kết quả dữ liệu cuối cùng.
            #     - 'summary': Dùng cho KẾT THÚC. Tổng kết các điểm Watch out! (Lưu ý quan trọng).

            #     --- STORYLINE BẮT BUỘC ---
            #     1. MỞ ĐẦU (mindmap): Giới thiệu tổng quan và lộ trình thực hiện theo các bước rõ ràng.
            #     2. THỰC HIỆN (vsc/terminal/excel): Chia nhỏ thành nhiều bước thực hành. Mỗi bước 1 section. 
            #     - Nếu viết code xong rồi chạy: Dùng 1 section 'vsc' (viết), sau đó 1 section 'cmd_overlay' (chạy).
            #     3. TỔNG KẾT (summary): Nhấn mạnh sai lầm thường gặp và kiến thức cốt lõi.

            #     --- YÊU CẦU GIỌNG ĐỌC (TEXT-TO-SPEECH OPTIMIZATION) ---
            #     - Giọng đọc phải CHẬM, SƯ PHẠM. 
            #     - Sử dụng dấu phẩy (,) để nghỉ ngắn và dấu ba chấm (...) để nghỉ dài giữa các ý.
            #     - Ví dụ: "Sau khi cài đặt xong... chúng ta sẽ tiến hành... khai báo thư viện xlwings."

            #     --- CẤU TRÚC JSON MẪU ---
            #     {{
            #         "title": "Tên bài học",
            #         "sections": [
            #             {{
            #                 "title": "Lộ trình thực hiện",
            #                 "ui_type": "mindmap",
            #                 "content": "Bước 1: Cài đặt thư viện\\nBước 2: Viết hàm xử lý\\nBước 3: Xuất báo cáo Excel",
            #                 "text": "Chào các bạn... Hôm nay chúng ta sẽ cùng giải quyết bài toán... Lộ trình của chúng ta gồm 3 bước..."
            #             }},
            #             {{
            #                 "title": "Viết mã nguồn",
            #                 "ui_type": "vsc",
            #                 "content": "import xlwings as xw\\n# Viết code tại đây",
            #                 "text": "Tại trình soạn thảo VSC... bạn hãy nhập đoạn mã sau... Chú ý việc import đúng thư viện."
            #             }},
            #             {{
            #                 "title": "Kết quả cuối cùng",
            #                 "ui_type": "summary",
            #                 "content": "1. Luôn đóng file Excel trước khi chạy\\n2. Kiểm tra quyền ghi file",
            #                 "text": "Cuối cùng... các bạn cần đặc biệt lưu ý... Hãy luôn đảm bảo file Excel được đóng trước khi thực thi lệnh."
            #             }}
            #         ]
            #     }}

            #     YÊU CẦU NGHIÊM NGẶT: Chỉ trả về mã JSON nguyên khối, không giải thích gì thêm.
            #     """

            # prompt = f"""
            #     Bạn là một Senior Solution Architect và Chuyên gia sư phạm công nghệ.
            #     Nhiệm vụ: Soạn kịch bản JSON chi tiết cho video bài giảng kỹ thuật về chủ đề: {topic}.

            #     --- YÊU CẦU CHIẾN LƯỢC UI (ÁNH XẠ TRỰC TIẾP VỚI ENGINE) ---
            #     Mỗi phần (section) PHẢI thuộc một trong các loại giao diện sau:
            #     - 'mindmap': Hiển thị lộ trình. Content: Danh sách các bước (\n).
            #     - 'terminal': Cài đặt. Content: Lệnh thực tế (Ví dụ: pip install xlwings).
            #     - 'vsc': Viết code Python. Content: Mã nguồn sạch. Dùng '>>' để ngăn cách code và output giả lập.
            #     - 'cmd_overlay': Chạy code. Content: 'python main.py >> [Kết quả trả về]'.
            #     - 'excel': Hiển thị kết quả bảng tính. 
            #         * QUY ĐỊNH CONTENT: Dạng CSV dùng dấu gạch đứng '|' để phân cột.
            #         * ĐỘNG NHẤT DỮ LIỆU: Dữ liệu trong bảng Excel PHẢI khớp hoàn toàn với logic xử lý trong phần 'vsc' trước đó.
            #     - 'summary': Tổng kết và lưu ý (Watch out!).

            #     --- STORYLINE BẮT BUỘC (PHẢI TUÂN THỦ) ---
            #     1. MỞ ĐẦU (mindmap): Lộ trình bài học.
            #     2. THỰC THI (vsc -> cmd_overlay): 
            #         - Tại 'vsc': Code phải thể hiện rõ các giá trị/biến sẽ ghi vào Excel.
            #         - Tại 'cmd_overlay': Thông báo "Đang ghi dữ liệu ra Excel..." trong text.
            #     3. KẾT QUẢ (excel): Hiện bảng dữ liệu ngay sau khi chạy code để chứng minh code chạy đúng. 
            #     4. TỔNG KẾT (summary).

            #     --- YÊU CẦU GIỌNG ĐỌC (TTS) ---
            #     - Giọng đọc CHẬM, ngắt nghỉ tự nhiên bằng dấu (,) và (...).
            #     - Ví dụ: "Bây giờ... chúng ta sẽ thực thi lệnh chạy... Dữ liệu đang được tự động đổ vào file Excel."

            #     --- CẤU TRÚC JSON MẪU ---
            #     {{
            #         "title": "Tên bài học",
            #         "sections": [
            #             {{
            #                 "title": "Lộ trình thực hiện",
            #                 "ui_type": "mindmap",
            #                 "content": "Bước 1: Cài đặt\\nBước 2: Viết code\\nBước 3: Xem kết quả",
            #                 "text": "Chào các bạn... Hôm nay chúng ta sẽ tự động hóa Excel... Lộ trình gồm 3 bước..."
            #             }},
            #             {{
            #                 "title": "Viết mã nguồn",
            #                 "ui_type": "vsc",
            #                 "content": "data = [('A1', 'Apple'), ('B1', 100)]\\nfor pos, val in data: ws.range(pos).value = val",
            #                 "text": "Đầu tiên... chúng ta tạo danh sách dữ liệu... sau đó dùng vòng lặp để ghi vào Excel."
            #             }},
            #             {{
            #                 "title": "Kết quả Excel",
            #                 "ui_type": "excel",
            #                 "content": "Vị trí | Giá trị \\n A1 | Apple \\n B1 | 100",
            #                 "text": "Kết quả là... ô A1 đã hiện Apple và B1 đã hiện 100... cực kỳ chính xác."
            #             }}
            #         ]
            #     }}

            #     CHỈ TRẢ VỀ JSON NGUYÊN KHỐI. KHÔNG GIẢI THÍCH.
            #     """
            
            prompt = f"""
                Bạn là một Senior Solution Architect và Chuyên gia sư phạm công nghệ.
                Nhiệm vụ: Soạn kịch bản JSON cho video bài giảng về: {topic}.

                --- QUY TẮC UI & CHỐNG TRÀN CHỮ (BẮT BUỘC) ---
                1. 'mindmap': CHỈ ghi tiêu đề các bước ngắn gọn (tối đa 5 từ mỗi dòng). 
                - Ví dụ: "1. Cài đặt thư viện\\n2. Khởi tạo Workbook\\n3. Ghi dữ liệu".
                2. 'vsc': Code Python sạch, có comment ngắn gọn lý do dùng hàm.
                3. 'excel': Bảng kết quả. Phải khớp 100% với dữ liệu trong code VSC. Định dạng: Cột | Giá trị.

                --- LUỒNG BÀI GIẢNG SƯ PHẠM ---
                - Bước 1 (mindmap): Giới thiệu có bao nhiêu bước thực hiện và mục tiêu từng bước.
                - Bước 2 (vsc): Viết code chậm rãi. Text giải thích: "Tại sao dùng thư viện này?", "Hàm này giải quyết vấn đề gì?".
                - Bước 3 (cmd_overlay): Chạy code và mô phỏng suy nghĩ: "Đợi một chút để hệ thống thực thi...".
                - Bước 4 (excel): Giải thích: "Dữ liệu này xuất hiện ở đây là do dòng code số X chúng ta vừa viết".

                --- CẤU TRÚC JSON MẪU ---
                {{
                    "title": "Tên bài học",
                    "sections": [
                        {{
                            "title": "Lộ trình 3 bước",
                            "ui_type": "mindmap",
                            "content": "1. Cài đặt xlwings\\n2. Mở Excel bằng Python\\n3. Ghi dữ liệu tự động",
                            "text": "Chào các bạn... Hôm nay chúng ta có 3 bước chính... Đầu tiên là cài đặt, sau đó là điều khiển Excel và cuối cùng là đổ dữ liệu."
                        }},
                        {{
                            "title": "Giải thích mã nguồn",
                            "ui_type": "vsc",
                            "content": "import xlwings as xw # Dùng để kết nối Excel\\napp = xw.App() # Mở ứng dụng Excel",
                            "text": "Ở đây, mình dùng import xlwings vì nó hỗ trợ tốt nhất cho việc điều khiển trực tiếp... Tiếp theo, lệnh xw.App giúp ta gọi ứng dụng Excel chạy ngầm hoặc hiện hữu."
                        }},
                        {{
                            "title": "Kết quả thực tế",
                            "ui_type": "excel",
                            "content": "Lệnh Python | Kết quả ô A1 \\n ws.range('A1') | Hello World",
                            "text": "Các bạn nhìn xem... Do lúc nãy mình viết lệnh ghi vào ô A1, nên bây giờ trên bảng Excel, giá trị Hello World đã xuất hiện chính xác."
                        }}
                    ]
                }}

                YÊU CẦU: JSON nguyên khối, không giải thích thừa.
                """
                            
            # 3. Gọi LLM và xử lý kết quả
            try:
                raw_res = llm.ask(prompt) 
                json_data = self.extract_clean_json(raw_res)

                if json_data:
                    # Tự động đoán ui_type nếu AI quên hoặc để default
                    from core.nlp_processor import NLPProcessor
                    nlp = NLPProcessor()
                    for sec in json_data.get("sections", []):
                        if "ui_type" not in sec or sec["ui_type"] == "default":
                            sec["ui_type"] = nlp.predict_action(sec.get("content", ""))
                    
                    # Lưu vào session state và ép UI load lại
                    st.session_state.current_script = json.dumps(json_data, indent=4, ensure_ascii=False)
                    st.success("✅ Đã soạn xong kịch bản!")
                    st.rerun()
                else:
                    st.error("AI trả về định dạng không phải JSON sạch. Hãy thử lại!")
            except Exception as e:
                st.error(f"Lỗi khi gọi AI: {str(e)}")

            

    def _handle_render_video(self, edited_script):
        async def run_prod():
            return await self.orchestrator.run_production(
                json.loads(edited_script), 
                st.session_state.active_course_id_internal, 
                st.session_state.selectbox_chapter,
                voice=st.session_state.selected_voice_id
            )
        with st.spinner("🎬 Đang render..."):
            video_result = asyncio.run(run_prod())
            if video_result:
                st.video(video_result)

    def _handle_save_script(self, content):
        name = st.session_state.new_lesson_input.strip() or st.session_state.selectbox_chapter
        if name and name != "-- Chọn bài --":
            path = os.path.join(self.courses_dir, st.session_state.active_course_id_internal, "chapters", name)
            os.makedirs(path, exist_ok=True)
            with open(os.path.join(path, "script.json"), "w", encoding="utf-8") as f:
                f.write(content)
            st.success("Đã lưu!")