# Sunny, smiling landscape, drawn with the standard library only (zlib + struct PNG writer).
import math, os, random, struct, zlib
W = H = 1024
buf = bytearray(W * H * 3)

def put(x, y, c, a=1.0):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        if a >= 1.0:
            buf[i:i + 3] = bytes(c)
        else:
            for k in range(3):
                buf[i + k] = int(buf[i + k] * (1 - a) + c[k] * a)

def ell(cx, cy, rx, ry, c, a=1.0, inner=0.0):
    for y in range(max(0, int(cy - ry)), min(H, int(cy + ry) + 1)):
        for x in range(max(0, int(cx - rx)), min(W, int(cx + rx) + 1)):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if inner <= d <= 1.0:
                put(x, y, c, a)

def rect(x0, y0, x1, y1, c, rad=0):
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            put(x, y, c)

def dot_line(pts, r, c, a=1.0):
    for x0, y0 in pts:
        ell(x0, y0, r, r, c, a)

def png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += buf[y * W * 3:(y + 1) * W * 3]
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    data += chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)

random.seed(11)
for y in range(H):
    t = y / H
    c = (int(255 * (1 - t) + 120 * t), int(230 * (1 - t) + 190 * t), int(120 * (1 - t) + 255 * t))
    buf[y * W * 3:(y + 1) * W * 3] = bytes(c) * W
for i, col in enumerate([(255, 90, 90), (255, 170, 60), (255, 235, 90), (120, 220, 120), (90, 170, 255), (160, 110, 230)]):
    r = 520 - i * 22
    for y in range(0, 700):
        for x in range(max(0, 512 - r - 8), min(W, 512 + r + 9)):
            d = math.hypot(x - 512, y - 700)
            if r - 8 <= d <= r + 8:
                put(x, y, col)
sx, sy = 170, 170
for k in range(16):
    a = k / 16 * math.pi * 2
    dot_line([(sx + math.cos(a) * (95 + j * 6), sy + math.sin(a) * (95 + j * 6)) for j in range(10)], 6, (255, 200, 40))
ell(sx, sy, 95, 95, (255, 215, 60))
ell(sx - 35, sy - 20, 10, 10, (90, 50, 20))
ell(sx + 35, sy - 20, 10, 10, (90, 50, 20))
dot_line([(sx - 40 + 80 * t / 40, sy + 20 + 25 * math.sin(math.pi * t / 40)) for t in range(41)], 5, (90, 50, 20))
ell(430, 1000, 630, 360, (110, 200, 110))
ell(900, 1000, 400, 320, (80, 180, 95))
for _ in range(60):
    fx, fy = random.uniform(40, 980), random.uniform(760, 1000)
    s = random.uniform(10, 22)
    col = random.choice([(255, 110, 150), (255, 240, 90), (180, 120, 255), (255, 255, 255)])
    for k in range(5):
        a = k / 5 * math.pi * 2
        ell(fx + math.cos(a) * s, fy + math.sin(a) * s, s / 2, s / 2, col)
    ell(fx, fy, s / 3, s / 3, (255, 190, 40))
    dot_line([(fx, fy + s + j * 6) for j in range(8)], 2, (40, 130, 50))
for bx, by in [(640, 300), (780, 240), (880, 330)]:
    dot_line([(bx + 30 * math.cos(math.pi * (1 + t / 20)), by + 14 * math.sin(math.pi * (1 + t / 20))) for t in range(21)], 2, (40, 40, 60))
png("/output/entry.png")
