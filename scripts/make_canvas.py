#!/usr/bin/env python3
"""画布模板：生成空白 9 格故事板画布（白底、黑框、序号），用于检查布局。
用法：python make_canvas.py out.png
"""
import sys
from PIL import Image, ImageDraw, ImageFont

def main(out):
    W, H = 1920, 1280
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 60, index=2)
    except Exception:
        font = ImageFont.load_default()
    pw, ph = W // 3, H // 3
    for i in range(9):
        x, y = (i % 3) * pw, (i // 3) * ph
        d.rectangle([x + 10, y + 10, x + pw - 10, y + ph - 10], outline=(0, 0, 0), width=4)
        d.text((x + 30, y + 20), str(i + 1), font=font, fill=(0, 0, 0))
    im.save(out)
    print(out, im.size)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "storyboard_canvas.png")
