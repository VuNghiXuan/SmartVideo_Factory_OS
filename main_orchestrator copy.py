import os
import asyncio
import re
import json
import shutil
import traceback
from config import config
from engines.voice_engine import VoiceEngine
from engines.video_engine import VideoEngine
from engines.scene_generator import SceneGenerator
from moviepy.editor import AudioFileClip
from core.nlp_processor import NLPProcessor 

class MainOrchestrator:
    def __init__(self):
        self.voice_eng = VoiceEngine()
        self.video_eng = VideoEngine()
        self.scene_gen = SceneGenerator()
        self.nlp = NLPProcessor() 

    # =================================================================
    # 1. HÀM CHÍNH (ENTRY POINT)
    # =================================================================
    async def run_production(self, script_data, course_id, lesson_id, progress_callback=None, voice=None):
        try:
            # Bước 1: Chuẩn bị môi trường
            clean_lesson_id, workspace, output_dir = self._setup_environment(course_id, lesson_id)
            voice = voice or config.DEFAULT_VOICE

            # Bước 2: Phân tích kịch bản thành danh sách cảnh
            scenes = self._parse_script_data(script_data)
            if not scenes: return None
            
            print(f"📊 Bắt đầu sản xuất: {len(scenes)} cảnh.")

            # Bước 3: Vòng lặp sản xuất từng cảnh
            scene_clips = []
            for i, scene_data in enumerate(scenes):
                clip = await self._produce_single_scene(i, scene_data, workspace, clean_lesson_id, voice)
                if clip:
                    scene_clips.append(clip)
                
                if progress_callback:
                    progress_val = int(((i + 1) / len(scenes)) * 80)
                    progress_callback(progress_val, f"Hoàn thành cảnh {i+1}/{len(scenes)}")

            # Bước 4: Gộp video cuối cùng
            return self._assemble_final_video(scene_clips, clean_lesson_id, output_dir, progress_callback)

        except Exception as e:
            print(f"❌ LỖI HỆ THỐNG: {str(e)}")
            traceback.print_exc()
            return None

    # =================================================================
    # 2. CÁC HÀM HỖ TRỢ (PRIVATE METHODS)
    # =================================================================

    def _setup_environment(self, course_id, lesson_id):
        """Dọn dẹp workspace và tạo thư mục output"""
        clean_id = re.sub(r'[^\w\s-]', '', lesson_id).strip().replace(' ', '_')
        if not clean_id or "Chọn_bài" in clean_id:
            clean_id = f"lesson_{int(asyncio.get_event_loop().time())}"

        course_path = os.path.join(config.COURSES_DIR, course_id)
        output_dir = os.path.join(course_path, config.OUTPUT_FOLDER_NAME)
        workspace = os.path.join(config.WORKSPACE_DIR, f"{course_id}_{clean_id}")

        os.makedirs(output_dir, exist_ok=True)
        if os.path.exists(workspace):
            shutil.rmtree(workspace, ignore_errors=True) 
        os.makedirs(workspace, exist_ok=True)
        
        return clean_id, workspace, output_dir

    def _parse_script_data(self, script_data):
        """Chuyển đổi mọi định dạng đầu vào thành list scenes chuẩn"""
        if isinstance(script_data, str):
            try: script_data = json.loads(script_data)
            except: return [{"text": script_data, "content": script_data}]

        if isinstance(script_data, dict):
            # Tìm danh sách cảnh trong các key phổ biến
            scenes = script_data.get('sections') or script_data.get('scenes') or script_data.get('lessons')
            if not scenes:
                for v in script_data.values():
                    if isinstance(v, list) and len(v) > 0: return v
            return scenes if scenes else [script_data]
            
        return script_data if isinstance(script_data, list) else []

    async def _produce_single_scene(self, index, scene, workspace, lesson_id, voice):
        """Quy trình sản xuất 1 cảnh: Voice -> Dựng Clip trực tiếp bằng VideoEngine"""
        try:
            # 1. Trích xuất dữ liệu từ kịch bản
            if isinstance(scene, dict):
                text = scene.get('text', '')
                raw_content = scene.get('content', text)
                ui_type = scene.get('ui_type')
            else:
                text = raw_content = str(scene)
                ui_type = None

            if not text.strip(): return None

            # 2. Tạo Voice (Audio)
            audio_path = os.path.join(workspace, f"audio_{index}.mp3")
            await self.voice_eng.generate_voice(text, audio_path, voice=voice)

            # 3. Dự đoán loại giao diện (VSC, CMD, Excel, Doc) nếu chưa có
            if not ui_type or ui_type == "default":
                ui_type = self.nlp.predict_action(f"{raw_content} {text}")

            # 4. Tiền xử lý nội dung cho VSC (nếu cần tách Editor và Terminal)
            final_content = raw_content
            if ui_type == "vsc" and hasattr(self.nlp, 'split_editor_terminal'):
                final_content = self.nlp.split_editor_terminal(raw_content)

            # 5. DỰNG CLIP (Bỏ qua SceneGenerator, gọi thẳng VideoEngine)
            # VideoEngine giờ đã tích hợp InterfaceDrawers để tự vẽ mọi thứ
            return self.video_eng.create_scene(
                text=text,           # Phụ đề
                audio_path=audio_path, 
                scene_type=ui_type,  # "vsc", "cmd", "excel", hoặc "doc"
                content=final_content,
                title=lesson_id      # Dùng làm tiêu đề nếu là cảnh Document
            )

        except Exception as e:
            print(f"⚠️ Lỗi sản xuất cảnh {index+1}: {e}")
            traceback.print_exc()
            return None

    def _assemble_final_video(self, scene_clips, lesson_id, output_dir, progress_callback):
        """Gộp các cảnh và đóng gói video"""
        if not scene_clips:
            print("❌ Không có cảnh nào để gộp!")
            return None

        print(f"\n📦 Đang gộp {len(scene_clips)} cảnh...")
        output_filename = f"{lesson_id}.mp4"
        
        final_path = self.video_eng.assemble_video(
            scene_clips=scene_clips, 
            output_filename=output_filename, 
            target_dir=output_dir
        )
        
        if progress_callback:
            progress_callback(100, "Sản xuất video thành công!")
        
        return final_path