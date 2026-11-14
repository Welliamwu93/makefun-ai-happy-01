# Draws a sunny, smiling landscape to /output/entry.png (deterministic)
import math, os, random
from PIL import Image, ImageDraw, ImageFilter

W = H = 1024
random.seed(11)
img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)
# sky gradient from warm yellow to sky blue
for y in range(H):
    t = y / H
    c = (int(255 * (1 - t) + 120 * t), int(230 * (1 - t) + 190 * t), int(120 * (1 - t) + 255 * t))
    d.line([(0, y), (W, y)], fill=c)

# rainbow arcs
for i, col in enumerate([(255, 90, 90), (255, 170, 60), (255, 235, 90), (120, 220, 120), (90, 170, 255), (160, 110, 230)]):
    r = 520 - i * 22
    d.arc((512 - r, 700 - r, 512 + r, 700 + r), 180, 360, fill=col, width=16)

# smiling sun with rays
sx, sy = 170, 170
for k in range(16):
    a = k / 16 * math.pi * 2
    d.line([(sx + math.cos(a) * 95, sy + math.sin(a) * 95), (sx + math.cos(a) * 150, sy + math.sin(a) * 150)], fill=(255, 200, 40), width=12)
d.ellipse((sx - 95, sy - 95, sx + 95, sy + 95), fill=(255, 215, 60))
d.ellipse((sx - 45, sy - 30, sx - 25, sy - 10), fill=(90, 50, 20))
d.ellipse((sx + 25, sy - 30, sx + 45, sy - 10), fill=(90, 50, 20))
d.arc((sx - 55, sy - 10, sx + 55, sy + 50), 20, 160, fill=(90, 50, 20), width=9)

# hills
d.ellipse((-200, 640, 700, 1300), fill=(110, 200, 110))
d.ellipse((400, 680, 1300, 1300), fill=(80, 180, 95))

# bouncy flowers
for _ in range(60):
    fx, fy = random.uniform(40, 980), random.uniform(760, 1000)
    s = random.uniform(10, 22)
    col = random.choice([(255, 110, 150), (255, 240, 90), (180, 120, 255), (255, 255, 255)])
    for k in range(5):
        a = k / 5 * math.pi * 2
        d.ellipse((fx + math.cos(a) * s - s / 2, fy + math.sin(a) * s - s / 2, fx + math.cos(a) * s + s / 2, fy + math.sin(a) * s + s / 2), fill=col)
    d.ellipse((fx - s / 3, fy - s / 3, fx + s / 3, fy + s / 3), fill=(255, 190, 40))
    d.line([(fx, fy + s), (fx, fy + s * 3)], fill=(40, 130, 50), width=4)

# happy birds
for bx, by in [(640, 300), (780, 240), (880, 330)]:
    d.arc((bx - 30, by - 14, bx, by + 14), 200, 340, fill=(40, 40, 60), width=5)
    d.arc((bx, by - 14, bx + 30, by + 14), 200, 340, fill=(40, 40, 60), width=5)

img = img.filter(ImageFilter.SMOOTH)
os.makedirs("/output", exist_ok=True)
img.save("/output/entry.png", "PNG", optimize=True)
