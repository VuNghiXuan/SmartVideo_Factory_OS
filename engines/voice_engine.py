import os
import edge_tts
import asyncio
from pydub import AudioSegment
from config import config

class VoiceEngine:
    def __init__(self):
        # Mặc định lấy từ config, nhưng có thể thay đổi linh hoạt
        self.default_output = config.WORKSPACE_DIR 

    async def generate_voice(self, text, output_path, voice="vi-VN-HoaiNhanNeural"):
        """
        output_path: Bây giờ sẽ nhận đường dẫn đầy đủ từ Orchestrator
        """
        # Đảm bảo thư mục chứa file đó tồn tại
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if not text or len(text.strip()) == 0:
            text = "Đoạn văn bản trống."

        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)
            
            if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                raise Exception("Server Edge-TTS không trả về dữ liệu.")
                
            return output_path
        except Exception as e:
            print(f"⚠️ Lỗi Edge-TTS: {e}. Đang dùng giọng Nữ HoaiMy...")
            try:
                communicate = edge_tts.Communicate(text, "vi-VN-HoaiMyNeural")
                await communicate.save(output_path)
                return output_path
            except:
                return None # Trả về None để Orchestrator biết mà bỏ qua Scene này

    def mix_bg_music(self, voice_path, music_path, final_path):
        """
        Gia cố thêm: Kiểm tra xem file nhạc nền có tồn tại không
        """
        if not os.path.exists(music_path):
            print(f"⚠️ Không tìm thấy nhạc nền tại: {music_path}, bỏ qua mix nhạc.")
            return voice_path

        voice = AudioSegment.from_file(voice_path)
        bg_music = AudioSegment.from_file(music_path)

        # Loop nhạc nền nếu nó ngắn hơn giọng đọc
        if len(bg_music) < len(voice):
            bg_music = bg_music * (len(voice) // len(bg_music) + 1)

        bg_music = bg_music - 25 # Giảm sâu hơn chút cho chuyên nghiệp
        combined = voice.overlay(bg_music)
        
        combined.export(final_path, format="mp3")
        return final_path