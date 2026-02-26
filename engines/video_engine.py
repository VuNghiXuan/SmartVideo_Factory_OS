import os
from moviepy import AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips, ColorClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from config import config

class VideoEngine:
    def __init__(self):
        self.output_dir = config.OUTPUT_DIR
        self.temp_dir = config.WORKSPACE_DIR
        self.fps = 24
        # Định nghĩa file nền mặc định
        self.default_bg = "background.jpg"
        self.default_music = "music.mp3"

    def create_text_image(self, text, size=(1920, 1080), font_size=60):
        # Tạo ảnh trong suốt để vẽ chữ
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        try:
            # Máy Windows thường có font này, nếu không nó sẽ dùng font mặc định
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        # Tính toán để căn giữa chữ
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        
        # Vẽ bóng chữ (Drop Shadow) cho dễ đọc
        draw.text(((size[0]-w)/2 + 3, 850 + 3), text, font=font, fill="black")
        # Vẽ chữ chính màu trắng
        draw.text(((size[0]-w)/2, 850), text, font=font, fill="white")
        return np.array(img)

    def create_scene(self, text, audio_path):
        audio = AudioFileClip(audio_path)
        duration = audio.duration

        # 1. Tạo nền (Ưu tiên ảnh 'background.jpg')
        if os.path.exists(self.default_bg):
            bg_clip = ImageClip(self.default_bg).with_duration(duration)
            # Cắt/Phóng ảnh cho vừa khung hình 1920x1080
            bg_clip = bg_clip.resized(width=1920) if bg_clip.w < 1920 else bg_clip.resized(height=1080)
            bg_clip = bg_clip.with_position("center")
        else:
            # Nếu không có ảnh, dùng nền màu xanh dương
            bg_clip = ColorClip(size=(1920, 1080), color=(30, 144, 255), duration=duration)

        # 2. Tạo Subtitle bằng Pillow
        txt_img = self.create_text_image(text)
        txt_clip = ImageClip(txt_img).with_duration(duration).with_start(0)

        # 3. Lắp ráp
        final_scene = CompositeVideoClip([bg_clip, txt_clip]).with_audio(audio)
        return final_scene

    def assemble_video(self, scene_clips, output_filename="final_lesson.mp4"):
        # Nối các cảnh lại
        final_video = concatenate_videoclips(scene_clips, method="compose")
        
        # 4. Chèn nhạc nền (Nếu có file 'music.mp3')
        if os.path.exists(self.default_music):
            try:
                bg_music = AudioFileClip(self.default_music)
                # Lặp lại nhạc nếu video dài hơn nhạc
                bg_music = bg_music.loop(duration=final_video.duration)
                # Giảm âm lượng nhạc nền xuống còn 10% để không đè tiếng đọc
                bg_music = bg_music.with_volume_scaled(0.10)
                
                # Trộn nhạc nền vào video
                new_audio = CompositeVideoClip([final_video.audio, bg_music.with_audio_codec('aac')]).audio
                final_video = final_video.with_audio(new_audio)
            except Exception as e:
                print(f"⚠️ Không thể chèn nhạc nền: {e}")

        output_path = os.path.join(self.output_dir, output_filename)
        
        # Xuất file với cấu hình tối ưu
        final_video.write_videofile(
            output_path, 
            fps=self.fps, 
            codec="libx264", 
            audio_codec="aac",
            threads=4, # Dùng 4 luồng CPU để render nhanh hơn
            logger=None # Tắt log của MoviePy để web chạy mượt
        )
        return output_path