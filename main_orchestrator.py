# Dispatcher: Nhan kich ban -> Goi Engine -> Noi Video

import os
import asyncio
import json
from config import config
from engines.voice_engine import VoiceEngine
from engines.video_engine import VideoEngine

class MainOrchestrator:
    def __init__(self):
        self.voice_eng = VoiceEngine()
        self.video_eng = VideoEngine()

    async def run_production(self, script_data, course_id, lesson_id):
        # 0. Thiết lập đường dẫn output chuẩn theo cấu trúc của mày
        output_dir = os.path.join(config.COURSES_DIR, course_id, "outputs")
        os.makedirs(output_dir, exist_ok=True)
        
        # Folder tạm để chứa audio/ảnh của bài học này
        workspace = os.path.join(config.WORKSPACE_DIR, f"{course_id}_{lesson_id}")
        os.makedirs(workspace, exist_ok=True)

        scene_clips = []
        
        for i, scene in enumerate(script_data):
            text = scene['text']
            # Lấy giọng đọc từ kịch bản, nếu không có dùng mặc định
            voice = scene.get('voice', config.DEFAULT_VOICE)
            
            audio_path = os.path.join(workspace, f"audio_{i}.mp3")
            
            # Bước 1: Thu âm (Mày nên truyền audio_path vào để VoiceEngine biết chỗ lưu)
            print(f"   [+] Recording Scene {i}...")
            await self.voice_eng.generate_voice(text, audio_path, voice=voice)
            
            # Bước 2: Dựng hình
            print(f"   [+] Rendering Scene {i}...")
            clip = self.video_eng.create_scene(text, audio_path)
            scene_clips.append(clip)

        # Bước 3: Xuất video vào đúng thư mục bài học
        final_filename = f"{lesson_id}.mp4"
        output_path = self.video_eng.assemble_video(scene_clips, final_filename, output_dir)
        
        return output_path

# Để test nhanh:
# orchestrator = MainOrchestrator()
# test_script = [{"text": "Chào mừng bạn đến với khóa học Python", "action": "intro"}]
# asyncio.run(orchestrator.run_production(test_script, "python_101", "bai_1"))