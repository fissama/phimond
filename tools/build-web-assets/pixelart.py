"""Bộ vẽ pixel-art gốc (Phimond) cho vật trang trí cảnh HD-2D.
Mật độ texel chuẩn: 40 px = 1 đơn vị thế giới (khớp sprite APK). Mọi hình ở đây do Phimond tự vẽ bằng mã."""
import random, math
from PIL import Image, ImageDraw

OUT = (24, 20, 30, 255)  # viền tối chung

def C(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)

def shade(c, f):
    return (max(0, min(255, int(c[0] * f))), max(0, min(255, int(c[1] * f))), max(0, min(255, int(c[2] * f))), c[3])

def canvas(w, h):
    return Image.new('RGBA', (w, h), (0, 0, 0, 0))

def outline(im, col=OUT):
    """Viền 1px quanh phần không trong suốt (4 hướng)."""
    w, h = im.size; src = im.load(); out = im.copy(); o = out.load()
    for y in range(h):
        for x in range(w):
            if src[x, y][3] < 40:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and src[nx, ny][3] >= 200:
                        o[x, y] = col; break
    return out

def pad(im, n=1):
    r = canvas(im.width + 2 * n, im.height + 2 * n); r.alpha_composite(im, (n, n)); return r

def poly(d, pts, fill): d.polygon(pts, fill=fill)

def lit_rect(d, box, base, top=1.18, side=0.82):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=base)
    d.line([(x0, y0), (x1, y0)], fill=shade(base, top))
    d.line([(x0, y0), (x0, y1)], fill=shade(base, 1.08))
    d.line([(x1, y0 + 1), (x1, y1)], fill=shade(base, side))
    d.line([(x0 + 1, y1), (x1, y1)], fill=shade(base, 0.7))

def tuft(seed, w=22, h=18, greens=('#2f7a2a', '#4fa83a', '#8ad04a')):
    rnd = random.Random(seed); im = canvas(w, h); d = ImageDraw.Draw(im)
    n = rnd.randint(5, 8)
    for i in range(n):
        x = int(2 + (w - 4) * (i + rnd.random() * 0.6) / n); top = rnd.randint(2, h - 6); lean = rnd.randint(-3, 3)
        col = C(rnd.choice(greens))
        for yy in range(h - 1, top, -1):
            t = (h - 1 - yy) / max(1, h - 1 - top); xx = x + int(lean * t * t)
            d.point((xx, yy), fill=col)
            if yy > h - 4: d.point((xx + 1, yy), fill=shade(col, 0.7))
    return outline(pad(im), (22, 52, 26, 255))

def flower(seed, petal='#ffffff', centre='#ffd84a', h=22, w=14):
    rnd = random.Random(seed); im = canvas(w, h); d = ImageDraw.Draw(im); cx = w // 2
    for yy in range(h - 1, 8, -1): d.point((cx + (1 if yy < h - 8 and rnd.random() < .3 else 0), yy), fill=C('#3d8a30'))
    d.polygon([(cx, h - 7), (cx - 4, h - 10), (cx - 2, h - 5)], fill=C('#4fa83a')); d.polygon([(cx, h - 9), (cx + 4, h - 12), (cx + 2, h - 6)], fill=C('#2f7a2a'))
    p = C(petal)
    for dx, dy in ((-3, 5), (3, 5), (0, 2), (-2, 8), (2, 8)):
        d.rectangle((cx + dx - 1, dy - 1 + 3, cx + dx + 1, dy + 1 + 3), fill=p)
    d.rectangle((cx - 1, 7, cx + 1, 9), fill=C(centre))
    return outline(pad(im), (30, 56, 32, 255))

def pebbles(seed, w=26, h=14):
    rnd = random.Random(seed); im = canvas(w, h); d = ImageDraw.Draw(im)
    for i in range(rnd.randint(2, 4)):
        rw, rh = rnd.randint(5, 10), rnd.randint(3, 6); x = rnd.randint(1, w - rw - 1); y = rnd.randint(2, h - rh - 1); g = rnd.randint(110, 150)
        base = (g, g - 6, g - 14, 255)
        d.ellipse((x, y, x + rw, y + rh), fill=base); d.arc((x, y, x + rw, y + rh), 200, 340, fill=shade(base, 1.3)); d.arc((x, y, x + rw, y + rh), 20, 160, fill=shade(base, .65))
    return outline(pad(im))

def rock(seed, w=44, h=32, base=(120, 118, 124, 255)):
    rnd = random.Random(seed); im = canvas(w, h); d = ImageDraw.Draw(im)
    pts = [(2, h - 3), (4, h * .45), (w * .3, 3), (w * .62, 5), (w - 3, h * .5), (w - 2, h - 3)]
    d.polygon(pts, fill=base)
    d.polygon([(4, h * .45), (w * .3, 3), (w * .5, 8), (w * .3, h * .55)], fill=shade(base, 1.25))
    d.polygon([(w * .62, 5), (w - 3, h * .5), (w - 2, h - 3), (w * .6, h - 3)], fill=shade(base, .72))
    for i in range(6): d.point((rnd.randint(4, w - 5), rnd.randint(8, h - 5)), fill=shade(base, 1.4 if i % 2 else .6))
    return outline(pad(im))

def barrel(w=28, h=34):
    im = canvas(w, h); d = ImageDraw.Draw(im); wood = C('#9a6a3a')
    d.ellipse((1, h - 9, w - 2, h - 1), fill=shade(wood, .75)); d.rectangle((1, 8, w - 2, h - 5), fill=wood); d.ellipse((1, 3, w - 2, 13), fill=shade(wood, 1.2)); d.ellipse((4, 5, w - 5, 11), fill=shade(wood, .9))
    for xx in range(4, w - 3, 5): d.line([(xx, 9), (xx, h - 5)], fill=shade(wood, .8))
    for yy in (13, h - 10): d.rectangle((1, yy, w - 2, yy + 2), fill=C('#5c5f68')); d.line([(1, yy), (w - 2, yy)], fill=C('#8b8f9a'))
    return outline(pad(im))

def crate(w=34, h=32):
    im = canvas(w, h); d = ImageDraw.Draw(im); wood = C('#b3843f')
    lit_rect(d, (1, 5, w - 2, h - 2), wood)
    d.polygon([(1, 5), (6, 1), (w - 2, 1), (w - 2, 5)], fill=shade(wood, 1.25))
    for k in (4, h // 2 + 1): d.line([(2, k + 4), (w - 3, k + 4)], fill=shade(wood, .65))
    d.line([(2, 6), (w - 3, h - 3)], fill=shade(wood, .7)); d.line([(w - 3, 6), (2, h - 3)], fill=shade(wood, .7))
    return outline(pad(im))

def bench(w=64, h=34):
    im = canvas(w, h); d = ImageDraw.Draw(im); wood = C('#a8733c'); iron = C('#3b3f4a')
    for x in (6, w - 9): d.rectangle((x, 14, x + 3, h - 2), fill=iron)
    lit_rect(d, (2, 12, w - 3, 18), wood); lit_rect(d, (2, 4, w - 3, 9), shade(wood, .95)); d.rectangle((6, 4, 8, 14), fill=iron); d.rectangle((w - 9, 4, w - 7, 14), fill=iron)
    return outline(pad(im))

def lamp(h=104, w=26):
    im = canvas(w, h); d = ImageDraw.Draw(im); iron = C('#2e323d'); cx = w // 2
    d.rectangle((cx - 1, 24, cx + 1, h - 8), fill=iron); d.rectangle((cx - 6, h - 8, cx + 6, h - 1), fill=shade(iron, 1.3)); d.rectangle((cx - 4, h - 14, cx + 4, h - 8), fill=iron)
    d.polygon([(cx - 7, 8), (cx + 7, 8), (cx + 9, 22), (cx - 9, 22)], fill=C('#ffd980')); d.polygon([(cx - 9, 22), (cx + 9, 22), (cx + 7, 25), (cx - 7, 25)], fill=iron)
    d.polygon([(cx - 8, 8), (cx, 1), (cx + 8, 8)], fill=iron); d.rectangle((cx - 3, 12, cx + 3, 20), fill=C('#fff6c8'))
    d.line([(cx - 7, 9), (cx - 8, 21)], fill=iron); d.line([(cx + 7, 9), (cx + 8, 21)], fill=iron)
    return outline(pad(im))

def glow(size=96, col=(255, 200, 120)):
    im = canvas(size, size); px = im.load(); c = size / 2
    for y in range(size):
        for x in range(size):
            r = math.hypot(x - c + .5, y - c + .5) / c
            a = max(0.0, 1 - r) ** 2.2
            px[x, y] = (col[0], col[1], col[2], int(255 * a))
    return im

def torch_frames(n=4, w=20, h=48):
    sheet = canvas(w * n, h)
    for i in range(n):
        im = canvas(w, h); d = ImageDraw.Draw(im); cx = w // 2
        d.rectangle((cx - 2, 22, cx + 2, h - 4), fill=C('#7a5230')); d.rectangle((cx - 4, 18, cx + 4, 24), fill=C('#3b3f4a')); d.rectangle((cx - 5, h - 6, cx + 5, h - 2), fill=C('#3b3f4a'))
        sw = [0, 1, 0, -1][i]
        d.polygon([(cx - 5, 18), (cx - 3 + sw, 8), (cx + sw, 1 + (i % 2)), (cx + 3 + sw, 8), (cx + 5, 18)], fill=C('#ff7a1a'))
        d.polygon([(cx - 3, 18), (cx - 1 + sw, 10), (cx + sw, 5), (cx + 2 + sw, 10), (cx + 3, 18)], fill=C('#ffc040'))
        d.polygon([(cx - 1, 18), (cx + sw, 11), (cx + 1, 18)], fill=C('#fff2b0'))
        sheet.alpha_composite(outline(im), (i * w, 0))
    return sheet

def shell(seed, w=18, h=14):
    rnd = random.Random(seed); im = canvas(w, h); d = ImageDraw.Draw(im); base = C(rnd.choice(['#f5d6c6', '#f0e6c8', '#f2b8b0']))
    d.pieslice((1, 1, w - 2, h * 2 - 4), 180, 360, fill=base)
    for k in range(3, w - 2, 3): d.line([(w // 2, h - 3), (k, 3)], fill=shade(base, .75))
    d.rectangle((w // 2 - 2, h - 3, w // 2 + 2, h - 2), fill=shade(base, .8))
    return outline(pad(im))

def starfish(w=22, h=20):
    im = canvas(w, h); d = ImageDraw.Draw(im); cx, cy = w / 2, h / 2; col = C('#e8743a'); pts = []
    for i in range(10):
        r = 9 if i % 2 == 0 else 3.6; a = -math.pi / 2 + i * math.pi / 5; pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=col)
    for p in pts[::2]: d.point((int(p[0] * .6 + cx * .4), int(p[1] * .6 + cy * .4)), fill=C('#ffd0a0'))
    return outline(pad(im))

def driftwood(w=70, h=22):
    im = canvas(w, h); d = ImageDraw.Draw(im); wood = C('#a58862')
    d.polygon([(2, h - 6), (8, 6), (w - 12, 4), (w - 2, 10), (w - 8, h - 4), (10, h - 2)], fill=wood)
    d.line([(8, 9), (w - 12, 8)], fill=shade(wood, 1.3)); d.line([(10, h - 6), (w - 10, h - 7)], fill=shade(wood, .7))
    for x in (18, 34, 50): d.line([(x, 8), (x + 3, h - 5)], fill=shade(wood, .8))
    return outline(pad(im))

def hay(w=44, h=34):
    im = canvas(w, h); d = ImageDraw.Draw(im); hay_c = C('#e4bb4a')
    d.ellipse((1, 3, w - 2, h - 2), fill=hay_c); d.ellipse((1, 3, w - 2, h - 2), outline=shade(hay_c, .65))
    for i in range(1, 6): d.arc((4 + i * 2, 6 + i, w - 4 - i * 2, h - 5 - i), 20, 340, fill=shade(hay_c, .82 if i % 2 else 1.1))
    d.rectangle((w // 2 - 1, 5, w // 2 + 1, h - 4), fill=shade(hay_c, .6))
    return outline(pad(im))

def reed(seed, w=20, h=40):
    rnd = random.Random(seed); im = canvas(w, h); d = ImageDraw.Draw(im)
    for i in range(5):
        x = 3 + i * 3 + rnd.randint(-1, 1); top = rnd.randint(4, 16); lean = rnd.randint(-2, 2)
        for yy in range(h - 1, top, -1): d.point((x + int(lean * (h - yy) / h * 1.5), yy), fill=C(rnd.choice(['#5f9a3a', '#7db84a', '#8a7a3a'])))
        d.rectangle((x - 1 + lean, top - 3, x + 1 + lean, top + 2), fill=C('#7a4a28'))
    return outline(pad(im))

def banner(w=26, h=70, col='#9b2a3a'):
    im = canvas(w, h); d = ImageDraw.Draw(im); pole = C('#c9a25a')
    d.rectangle((w // 2 - 1, 0, w // 2 + 1, h - 1), fill=pole); d.rectangle((2, 3, w - 3, 5), fill=pole)
    d.polygon([(4, 6), (w - 4, 6), (w - 4, h * .62), (w // 2, h * .72), (4, h * .62)], fill=C(col)); d.polygon([(4, 6), (w - 4, 6), (w - 4, 12), (4, 12)], fill=shade(C(col), 1.25))
    d.ellipse((w // 2 - 4, 22, w // 2 + 4, 30), fill=pole)
    return outline(pad(im))

def sign(w=34, h=52, text_col='#3a2a18'):
    im = canvas(w, h); d = ImageDraw.Draw(im); wood = C('#a5753d')
    d.rectangle((w // 2 - 2, 16, w // 2 + 2, h - 1), fill=shade(wood, .8)); lit_rect(d, (2, 3, w - 3, 21), wood)
    for y in (8, 13): d.line([(6, y), (w - 7, y)], fill=C(text_col))
    return outline(pad(im))

def fence(w=56, h=30):
    im = canvas(w, h); d = ImageDraw.Draw(im); wood = C('#b68a4c')
    for x in (3, w // 2 - 2, w - 7): lit_rect(d, (x, 3, x + 4, h - 2), wood)
    for y in (9, 19): lit_rect(d, (0, y, w - 1, y + 4), shade(wood, 1.05))
    return outline(pad(im))

def lily(w=34, h=16):
    im = canvas(w, h); d = ImageDraw.Draw(im); g = C('#3f9a48')
    d.ellipse((1, 3, w - 2, h - 2), fill=g); d.polygon([(w // 2, h // 2), (w - 2, h // 2 - 2), (w - 2, h // 2 + 1)], fill=(0, 0, 0, 0))
    d.ellipse((w // 2 - 3, 4, w // 2 + 3, 8), fill=C('#ffb8d8'))
    return outline(pad(im))

def tent(w=96, h=88, col='#c14a3a'):
    im = canvas(w, h); d = ImageDraw.Draw(im); c = C(col); cream = C('#f0e2bc')
    d.rectangle((6, h * .45, 9, h - 2), fill=C('#7a5230')); d.rectangle((w - 10, h * .45, w - 7, h - 2), fill=C('#7a5230'))
    n = 8; sw = (w - 4) / n
    for i in range(n):
        x0 = 2 + i * sw
        d.polygon([(x0, h * .36), (x0 + sw, h * .36), (x0 + sw - 1, h * .5), (x0 + sw / 2, h * .56), (x0 + 1, h * .5)], fill=c if i % 2 == 0 else cream)
    for i in range(n):
        x0 = 2 + i * sw; d.polygon([(w / 2, 2), (x0, h * .36), (x0 + sw, h * .36)], fill=c if i % 2 == 0 else cream)
    lit_rect(d, (10, h * .72, w - 11, h * .8), C('#a5753d'))
    for k, col2 in enumerate(['#e9533c', '#f2c040', '#5fb050', '#a65fd0']): d.ellipse((14 + k * 17, h * .62, 22 + k * 17, h * .72), fill=C(col2))
    return outline(pad(im))


# ---------------------------------------------------------------- ô sàn lặp (tileable)
def _periodic_field(w, h, seed, terms=9, kmax=5):
    rnd = random.Random(seed); fs = []
    for _ in range(terms):
        fs.append((rnd.randint(-kmax, kmax), rnd.randint(-kmax, kmax), rnd.uniform(0, 6.283), rnd.uniform(0.4, 1.0)))
    fs = [f for f in fs if f[0] or f[1]]
    tot = sum(f[3] for f in fs)
    out = [[0.0] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            v = 0.0
            for k, l, ph, a in fs: v += a * math.sin(2 * math.pi * (k * x / w + l * y / h) + ph)
            out[y][x] = v / tot
    return out

_BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]

def ground_tile(seed, w, h, tones, blades=None, specks=None, blade_n=60, speck_n=40, litter=None, litter_n=0):
    """Ô sàn lặp pixel-art: trường nhiễu tuần hoàn -> 4 tông + dither Bayer, thêm lá/cỏ lẻ. tones: 4 màu từ tối đến sáng."""
    rnd = random.Random(seed); f1 = _periodic_field(w, h, seed * 3 + 1, 8, 4); f2 = _periodic_field(w, h, seed * 3 + 2, 10, 9)
    im = Image.new('RGBA', (w, h)); px = im.load()
    T = [C(t) for t in tones]
    for y in range(h):
        for x in range(w):
            v = f1[y][x] * 0.65 + f2[y][x] * 0.35
            v = (v + 1) / 2 + (_BAYER[y % 4][x % 4] / 16 - 0.5) * 0.16
            i = 0 if v < 0.28 else 1 if v < 0.5 else 2 if v < 0.74 else 3
            px[x, y] = T[i]
    def put(x, y, col): px[x % w, y % h] = col
    for _ in range(blade_n):
        x, y = rnd.randrange(w), rnd.randrange(h); ln = rnd.randint(2, 4); col = T[3 if rnd.random() < .6 else 0]
        lean = rnd.choice([-1, 0, 1])
        for k in range(ln): put(x + (lean if k > ln // 2 else 0), y - k, shade(col, 1.0 - 0.08 * k) if col == T[0] else shade(col, 1.0 + 0.06 * k))
    for _ in range(speck_n):
        x, y = rnd.randrange(w), rnd.randrange(h); put(x, y, T[3]); put(x + 1, y, T[2])
    if litter:
        for _ in range(litter_n):
            x, y = rnd.randrange(w), rnd.randrange(h); c = C(rnd.choice(litter)); put(x, y, c); put(x + 1, y, c); put(x, y + 1, shade(c, .8))
    return im

def sand_tile(seed, w, h):
    rnd = random.Random(seed); tones = ['#c9b98a', '#d8c99a', '#e6d9ab', '#f2e8c4']
    im = ground_tile(seed, w, h, tones, blade_n=0, speck_n=26)
    px = im.load(); T = [C(t) for t in tones]
    f = _periodic_field(w, h, seed + 9, 5, 3)
    for y in range(h):
        for x in range(w):
            wave = math.sin(2 * math.pi * (y / h * 3 + 0.18 * f[y][x]))
            if wave > 0.94: px[x, y] = shade(T[3], 1.04)
            elif wave < -0.95: px[x, y] = shade(T[0], .94)
    return im

def haystack(w=52, h=50):
    im = canvas(w, h); d = ImageDraw.Draw(im); hay = C('#e2b845')
    d.polygon([(2, h - 3), (6, h * .5), (w * .35, 5), (w * .5, 2), (w * .65, 5), (w - 6, h * .5), (w - 2, h - 3)], fill=hay)
    d.polygon([(w * .5, 2), (w * .65, 5), (w - 6, h * .5), (w - 2, h - 3), (w * .62, h - 3)], fill=shade(hay, .82))
    d.polygon([(2, h - 3), (6, h * .5), (w * .35, 5), (w * .38, h * .55), (w * .22, h - 3)], fill=shade(hay, 1.12))
    rnd = random.Random(5)
    for _ in range(46):
        x = rnd.randint(5, w - 6); y = rnd.randint(8, h - 5); d.line([(x, y), (x + rnd.randint(-3, 3), y + rnd.randint(-5, -2))], fill=shade(hay, rnd.choice([.7, .85, 1.2, 1.3])))
    d.rectangle((4, h * .62, w - 5, h * .62 + 2), fill=C('#8a5a2a'))
    return outline(pad(im))


def carpet(w, h):
    """Thảm đỏ viền vàng, hoa văn dệt nhẹ (pixel art, nguyên bản)."""
    from PIL import Image, ImageDraw
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    red = [(150, 22, 22), (168, 28, 26), (132, 18, 20)]; gold = (226, 176, 70); gold2 = (170, 120, 40)
    for y in range(h):
        for x in range(w):
            base = red[((x // 2) + (y // 2)) % 2 if (x + y) % 5 else 2]
            im.putpixel((x, y), base + (255,))
    d.rectangle([0, 0, w - 1, h - 1], outline=gold2 + (255,)); d.rectangle([1, 1, w - 2, h - 2], outline=gold + (255,))
    d.rectangle([4, 4, w - 5, h - 5], outline=gold2 + (255,))
    for x in range(8, w - 8, 6):
        d.polygon([(x, h // 2), (x + 3, h // 2 - 3), (x + 6, h // 2), (x + 3, h // 2 + 3)], outline=gold + (255,))
    return im
