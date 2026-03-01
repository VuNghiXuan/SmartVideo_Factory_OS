import math
import numpy as np
from PIL import ImageDraw, ImageFont

class BaseDrawer:
    @staticmethod
    def get_fonts(base_size=32):
        try:
            return {
                'code': ImageFont.truetype("consola.ttf", base_size),
                'term': ImageFont.truetype("consola.ttf", base_size - 6),
                'ui': ImageFont.truetype("arial.ttf", base_size - 12),
                'bold': ImageFont.truetype("arialbd.ttf", base_size + 10)
            }
        except:
            return {k: ImageFont.load_default() for k in ['code', 'term', 'ui', 'bold']}

    @staticmethod
    def draw_win11_controls(draw, width, is_dark=True):
        color = (200, 200, 200) if is_dark else (60, 60, 60)
        draw.text((width - 45, 12), "✕", fill=color, font=ImageFont.truetype("arial.ttf", 20))
        draw.rectangle([(width - 85, 18), (width - 70, 33)], outline=color, width=1)
        draw.line([(width - 125, 33), (width - 110, 33)], fill=color, width=2)

    @staticmethod
    def draw_smooth_cursor(img, t, duration):
        draw = ImageDraw.Draw(img)
        start_pos, end_pos = (1850, 1000), (960, 540)
        prog = min(t / (duration * 0.5), 1.0)
        curve = (1 - math.cos(prog * math.pi)) / 2
        cur_x = start_pos[0] + (end_pos[0] - start_pos[0]) * curve
        cur_y = start_pos[1] + (end_pos[1] - start_pos[1]) * curve
        draw.polygon([(cur_x, cur_y), (cur_x, cur_y + 25), (cur_x + 18, cur_y + 18)], fill="white", outline="black")