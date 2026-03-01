import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    VideoClip, ImageClip, AudioFileClip, 
    CompositeVideoClip, CompositeAudioClip, 
    concatenate_videoclips
)
from .drawers import InterfaceDrawers
from config import config
# from .drawers import draw_vsc, draw_cmd, draw_excel, draw_mindmap, draw_document

class VideoEngine:
    def __init__(self):
        self.fps = 24
        self.default_bg = "background.jpg"
        self.default_music = "music.mp3"

    def wrap_text(self, text, font, max_width):
        """Tự động ngắt dòng cho Subtitle"""
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            width = font.getlength(test_line)
            if width <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        lines.append(' '.join(current_line))
        return "\n".join(lines)

    def create_text_image(self, text, size=(1920, 1080), font_size=38):
        """Vẽ Subtitle có nền mờ"""
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        try:
            font_path = "C:/Windows/Fonts/Arial.ttf" if os.name == 'nt' else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()

        wrapped_text = self.wrap_text(text, font, size[0] - 300)
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, align="center")
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pos_x, pos_y = (size[0] - text_w) / 2, size[1] - text_h - 100 # Đẩy cao hơn tí tránh taskbar

        padding = 30
        draw.rectangle([(pos_x - padding, pos_y - padding), (pos_x + text_w + padding, pos_y + text_h + padding)], fill=(0, 0, 0, 160))
        draw.multiline_text((pos_x, pos_y), wrapped_text, font=font, fill="white", align="center")
        return np.array(img)

    def create_scene(self, text, audio_path, scene_type="vsc", index=0, workspace="", **kwargs):
        """Hàm điều phối: Render từng cảnh đơn lẻ để đảm bảo Audio Reader không bị None"""
        duration = 5.0
        audio = None
        
        # 1. Khởi tạo Audio gốc (Giọng đọc)
        if audio_path and os.path.exists(audio_path):
            try:
                # Thêm fps=44100 để đồng bộ chuẩn âm thanh
                audio = AudioFileClip(audio_path, fps=44100)
                duration = max(audio.duration, 1.0)
            except Exception as e:
                print(f"⚠️ Lỗi load audio cảnh {index}: {e}")

        content = kwargs.get('content', '')
        title = kwargs.get('title', 'HƯỚNG DẪN HỌC TẬP')

        # 2. Hàm vẽ frame
        # Tìm đến hàm make_frame bên trong create_scene và sửa như sau:
        def make_frame(t):
            # Đảm bảo scene_type không bị dính khoảng trắng hay chữ hoa chữ thường
            s_type = str(scene_type).lower().strip()
            
            params = {
                't': t, 
                'duration': duration,
                'content': content, 
                'title': title,
                **kwargs 
            }

            try:
                # 1. Kiểm tra các loại giao diện
                if s_type in ["cmd", "terminal", "cmd_overlay"]:
                    frame = InterfaceDrawers.draw_cmd(**params)
                
                elif s_type == "doc":
                    frame = InterfaceDrawers.draw_document(**params)
                    
                elif s_type == "excel":
                    frame = InterfaceDrawers.draw_excel(**params)
                    
                else:
                    # Mặc định luôn là VSC để tránh trả về None
                    frame = InterfaceDrawers.draw_vsc(**params)

                # 2. KIỂM TRA CUỐI CÙNG: Nếu hàm vẽ lỡ tay trả về None
                if frame is None:
                    print(f"⚠️ Cảnh báo: Hàm vẽ {s_type} trả về None tại t={t}. Dùng frame đen dự phòng.")
                    import numpy as np
                    return np.zeros((1080, 1920, 3), dtype=np.uint8)
                    
                return frame

            except Exception as e:
                print(f"❌ Lỗi nghiêm trọng tại make_frame cảnh {index} (t={t}): {e}")
                import numpy as np
                return np.zeros((1080, 1920, 3), dtype=np.uint8)

        # 3. Tạo Main Video Clip
        main_clip = VideoClip(make_frame, duration=duration).set_fps(self.fps)

        # 4. Chèn Subtitle
        try:
            sub_img = self.create_text_image(text)
            sub_clip = ImageClip(sub_img).set_duration(duration).set_position(("center", "bottom"))
            final_clip = CompositeVideoClip([main_clip, sub_clip], size=(1920, 1080))
        except:
            final_clip = main_clip

        # 5. MIX AUDIO - ĐÂY LÀ CHỖ DỄ LỖI NHẤT
        audio_list = []
        if audio:
            audio_list.append(audio)
            
            # Tiếng gõ phím
            kb_path = "assets/keyboard.mp3"
            if scene_type == "vsc" and os.path.exists(kb_path):
                try:
                    # Ép chuẩn fps cho âm thanh gõ phím
                    kb_audio = AudioFileClip(kb_path, fps=44100).subclip(0, min(duration, 5.0)).volumex(0.1)
                    audio_list.append(kb_audio)
                except: pass
        
        if audio_list:
            final_clip.audio = CompositeAudioClip(audio_list)
        
        final_clip.duration = duration

        # 6. KẾT XUẤT CẢNH TẠM (Dùng đường dẫn tuyệt đối, không dấu nếu có thể)
        temp_filename = os.path.join(workspace, f"temp_scene_{index}.mp4")
        print(f"🎥 Đang kết xuất cảnh đơn lẻ {index}...")
        
        try:
            final_clip.write_videofile(
                temp_filename, 
                fps=self.fps, 
                codec="libx264", 
                audio_codec="aac", 
                logger=None,
                threads=1 # Để threads=1 khi render cảnh đơn lẻ giúp tránh lỗi tranh chấp reader
            )
        except Exception as e:
            print(f"❌ Render cảnh {index} thất bại: {e}")
            return None

        # GIẢI PHÓNG BỘ NHỚ
        if final_clip.audio: final_clip.audio.close()
        final_clip.close()
        if audio: audio.close()

        return temp_filename

    def _apply_fade_transitions(self, scene_clips, padding=0.5):
        if len(scene_clips) <= 1: return concatenate_videoclips(scene_clips, method="chain")
        faded_clips = [scene_clips[0]]
        for clip in scene_clips[1:]:
            faded_clips.append(clip.crossfadein(padding))
        return concatenate_videoclips(faded_clips, method="compose", padding=-padding)

    def assemble_video(self, scene_paths, output_filename, target_dir):
        """Gộp các file MP4 tạm thành video cuối cùng - Bản sửa lỗi triệt để"""
        clips = []
        try:
            from moviepy.editor import VideoFileClip, concatenate_videoclips
            
            # 1. Load clips cẩn thận
            for path in scene_paths:
                if path and os.path.exists(path):
                    try:
                        # Ép moviepy không dùng cache audio nếu không cần
                        c = VideoFileClip(path)
                        if c.duration > 0:
                            clips.append(c)
                    except Exception as e:
                        print(f"⚠️ Bỏ qua clip lỗi {path}: {e}")

            if not clips:
                print("❌ Không có clip hợp lệ để gộp!")
                return None

            print(f"📦 Đang gộp {len(clips)} cảnh...")
            
            # 2. Dùng method="compose" nhưng tối giản hóa
            final_video = concatenate_videoclips(clips, method="compose")
            
            output_path = os.path.join(target_dir, output_filename)

            # 3. Ghi file với các tham số an toàn nhất
            final_video.write_videofile(
                output_path,
                fps=24,
                codec="libx264",
                audio_codec="aac",
                temp_audiofile=os.path.join(target_dir, "last_resort_audio.m4a"),
                remove_temp=True,
                logger=None
            )

            # 4. Đóng sạch sẽ
            final_video.close()
            for c in clips:
                c.close()
            
            return output_path

        except Exception as e:
            print(f"❌ Lỗi gộp video cực nghiêm trọng: {e}")
            import traceback
            traceback.print_exc()
            return None