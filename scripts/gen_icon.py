import math
from PIL import Image, ImageDraw, ImageEnhance

# Miniature du roster (icon-selection.png) : rendue nativement en haute resolution avec la meme
# grille/logique que gen_skyline.py (immeubles, fenetres, taxis), au lieu de screenshotter puis
# agrandir une capture basse-resolution du navigateur. Deux immeubles de jour, coupes avant leur
# sommet (on ne veut pas la tour entiere), + route avec 2 taxis.

SCALE = 24
SS = 3
DRAW = SCALE * SS

hourColors = [
  '#2c3758', '#2c3554', '#2c3450', '#2c324c', '#2c3048', '#464260',
  '#615578', '#877480', '#ab9482', '#a59485', '#9f948a', '#98948d',
  '#999591', '#9b9993', '#9d9b97', '#a49184', '#aa8970', '#b17f5e',
  '#ac7659', '#a56e55', '#855d68', '#6a4e7a', '#574271', '#433668',
]
def colorFor(h): return hourColors[h % 24]

buildings = [
    dict(h=12, tiers=[(0, 56.28, 11.75), (56.28, 1.69, 8.22)]),
    dict(h=13, tiers=[(0, 36.12, 12.47), (36.12, 22.13, 6.86)]),
]

slotWidth = 15
heightScale = 1.8
groundY = 108
buildingBaseY = groundY
laneHeight = 3.5
roadHeight = laneHeight * 3

STROKE = '#55555a'
WINDOW_OFF = '#2a4258'
WINDOW_LIT = '#f4c542'

def windowsFor(start, length, width):
    if length < 5 or width < 3.5: return []
    margin = 2.2
    rowGap = 4.2
    usable = length - margin*2
    rows = max(1, int(usable // rowGap) + 1)
    halfW = width/2 - 1
    colGap = 3.2
    cols = []
    if halfW > 3:
        c = -halfW + 1
        while c <= halfW - 1:
            cols.append(c); c += colGap
    elif halfW > 1:
        cols = [-halfW*0.55, halfW*0.55]
    else:
        cols = [0]
    pts = []
    for r in range(rows):
        d = usable/2 if rows == 1 else (usable*r)/(rows-1)
        for c in cols:
            pts.append((start+margin+d, c))
    return pts

def hashUnit(seed):
    x = math.sin(seed) * 43758.5453
    return x - math.floor(x)

# Cadrage : 2 slots de large, immeubles coupes avant leur sommet, route tout en bas (pas de marge
# morte). Fond rempli avec la couleur du ciel de la scene (pas transparent) pour que l'espace entre
# les deux tours reste coherent avec le reste du site, pas un vide.
viewW = slotWidth * 2
viewYBottom = groundY + roadHeight
viewYTop = viewYBottom - viewW / (36/68)
y_min, y_max = viewYTop, viewYBottom

W = int(viewW * DRAW)
H = int((y_max - y_min) * DRAW)

def px(x, y):
    return (x*DRAW, (y - y_min)*DRAW)

im = Image.new('RGBA', (W, H), (10, 22, 40, 255))
draw = ImageDraw.Draw(im)

taxi_sprite = Image.open('/Users/davidjbreau/dev/PORTFOLIO/public/img/taxi-pixel.png').convert('RGBA')

# route
r0 = px(0, groundY); r1 = px(viewW, groundY + roadHeight)
draw.rectangle([r0[0], r0[1], r1[0], r1[1]], fill='#646770')
for laneY in (groundY + laneHeight, groundY + laneHeight * 2):
    l0 = px(0, laneY); l1 = px(viewW, laneY)
    draw.line([l0, l1], fill='#e8dfae', width=max(1, int(0.35*DRAW)))

for i, b in enumerate(buildings):
    xCenter = i*slotWidth + slotWidth/2
    bodyColor = colorFor(b['h'])
    for (start, length, width) in b['tiers']:
        s = start*heightScale
        l = length*heightScale
        x0 = xCenter - width/2
        y0 = buildingBaseY - s - l
        x1 = x0 + width
        y1 = y0 + l
        p0 = px(x0, y0); p1 = px(x1, y1)
        draw.rectangle([p0[0], p0[1], p1[0], p1[1]], fill=bodyColor, outline=STROKE, width=max(1, int(0.5*DRAW)))
        for (wx, wy) in windowsFor(s, l, width):
            if hashUnit(i*33.71 + wx*5.19 + wy*9.02) < 0.12:
                continue
            realX = xCenter + wy
            realY = buildingBaseY - wx
            wp0 = px(realX-0.7, realY-0.7)
            wp1 = px(realX+0.7, realY+0.7)
            draw.rectangle([wp0[0], wp0[1], wp1[0], wp1[1]], fill=WINDOW_OFF)

# 2 taxis fixes sur la route
for tx in (slotWidth*0.55, slotWidth*1.55):
    ty = groundY + laneHeight*1.5 - 3.75
    tp0 = px(tx - 6, ty)
    sprite_w = int(12*DRAW)
    sprite_h = int(7*DRAW)
    resized = taxi_sprite.resize((sprite_w, sprite_h), Image.NEAREST)
    im.alpha_composite(resized, (int(tp0[0]), int(tp0[1])))

final = im.resize((int(viewW * SCALE), int((y_max - y_min) * SCALE)), Image.LANCZOS)
final.save('/Users/davidjbreau/dev/PORTFOLIO/src/content/projects/nyc-taxi/assets/icon-selection.png')
print('saved', final.size)
