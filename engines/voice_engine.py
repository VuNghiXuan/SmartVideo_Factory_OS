import os
import edge_tts
import asyncio
import re
from pydub import AudioSegment
from config import config

class VoiceEngine:
    def __init__(self):
        self.default_output = config.WORKSPACE_DIR 

    async def generate_voice(self, text, output_path, voice=None):
        # 1. Xác định giọng đọc
        target_voice = voice if (voice and str(voice).strip()) else getattr(config, 'DEFAULT_VOICE', "vi-VN-HoaiMyNeural")
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 2. Dọn dẹp file cũ
        if os.path.exists(output_path):
            try: os.remove(output_path)
            except: pass 

        if not text or len(text.strip()) == 0:
            text = "Nội dung bài giảng đang được cập nhật."

        # 3. Xử lý ngắt nghỉ: Thêm dấu phẩy để AI tự nghỉ nhịp tự nhiên
        processed_text = text.replace("Terminal", "Terminal, ").replace("Window", "Window, ")
        
        # 4. Vòng lặp thử lại nếu lỗi API
        for attempt in range(3):
            try:
                print(f"🎙️ Đang gọi Edge-TTS: {target_voice} (Lần {attempt + 1}, Tốc độ: -15%)")
                
                # KHÔNG khởi tạo rỗng. Truyền thẳng tham số vào đây:
                communicate = edge_tts.Communicate(
                    text=processed_text, 
                    voice=target_voice, 
                    rate="-15%"  # Đọc chậm lại để khớp với thao tác màn hình
                )
                
                await communicate.save(output_path)
                
                # Kiểm tra file có thực sự tồn tại và có dung lượng không
                if os.path.exists(output_path) and os.path.getsize(output_path) > 100:
                    print(f"✅ Audio thành công: {output_path}")
                    return output_path
                    
            except Exception as e:
                print(f"🔄 Lỗi lần {attempt + 1}: {e}")
                if attempt < 2: await asyncio.sleep(1.5)

        # 5. Tầng cứu sinh cuối cùng
        try:
            print("⚠️ Đang dùng giọng cứu sinh dự phòng...")
            backup_comm = edge_tts.Communicate(processed_text, "vi-VN-HoaiMyNeural", rate="-10%")
            await backup_comm.save(output_path)
            return output_path
        except Exception as e:
            print(f"❌ Thất bại hoàn toàn: {e}")
            return None

    def mix_bg_music_advanced(self, voice_path, final_path, bg_type=None):
        if not bg_type: return voice_path

        music_map = {
            "tutorial": "assets/soft_piano.mp3",
            "promo": "assets/upbeat_corporate.mp3"
        }
        
        music_path = music_map.get(bg_type)
        if not music_path or not os.path.exists(music_path): return voice_path

        voice = AudioSegment.from_file(voice_path)
        bg_music = AudioSegment.from_file(music_path)

        vol_reduction = -30 if bg_type == "tutorial" else -20
        if len(bg_music) < len(voice):
            bg_music = bg_music * (len(voice) // len(bg_music) + 1)
            
        combined = voice.overlay(bg_music[:len(voice)] + vol_reduction)
        combined.export(final_path, format="mp3")
        return final_path