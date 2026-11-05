#!/usr/bin/env python3
"""画布模板：生成空白故事板画布（白底、黑框、序号），用于检查布局。
用法：python make_canvas.py out.png [--panels G]
格数 G 是参数（G = N × 3，N = D ÷ 10；D=30 秒时 9 格，D=60 秒时 18 格），默认 9。
"""
import sys
from PIL import Image, ImageDraw, ImageFont

def main(out, panels=9):
    cols = 3
    rows = (panels + cols - 1) // cols
    W, H = 1920, 1280 * rows // 3
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 60, index=2)
    except Exception:
        font = ImageFont.load_default()
    pw, ph = W // 3, H // rows
    for i in range(panels):
        x, y = (i % 3) * pw, (i // 3) * ph
        d.rectangle([x + 10, y + 10, x + pw - 10, y + ph - 10], outline=(0, 0, 0), width=4)
        d.text((x + 30, y + 20), str(i + 1), font=font, fill=(0, 0, 0))
    im.save(out)
    print(out, im.size)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "storyboard_canvas.png"
    panels = 9
    if "--panels" in sys.argv:
        panels = int(sys.argv[sys.argv.index("--panels") + 1])
    main(out, panels)
