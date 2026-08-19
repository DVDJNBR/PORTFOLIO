import math
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

SCALE = 6
SS = 3  # supersample factor: draw at SCALE*SS then downsample for anti-aliased edges
DRAW = SCALE * SS

hourColors = [
  '#2c3758', '#2c3554', '#2c3450', '#2c324c', '#2c3048', '#464260',
  '#615578', '#877480', '#ab9482', '#a59485', '#9f948a', '#98948d',
  '#999591', '#9b9993', '#9d9b97', '#a49184', '#aa8970', '#b17f5e',
  '#ac7659', '#a56e55', '#855d68', '#6a4e7a', '#574271', '#433668',
]
def colorFor(h): return hourColors[h % 24]

buildings = [
 dict(h=0, L=38.15, tiers=[(0,38.15,9.52),(38.15,1.14,6.66)], peak=False),
 dict(h=1, L=29.25, tiers=[(0,18.13,9.42),(18.13,11.12,5.18)], peak=False),
 dict(h=2, L=23.45, tiers=[(0,11.73,9.55),(11.73,6.57,5.73),(18.3,5.15,2.87)], peak=False),
 dict(h=3, L=19.81, tiers=[(0,19.81,9.85),(19.81,0.59,6.89)], peak=False),
 dict(h=4, L=18.0, tiers=[(0,11.16,8.29),(11.16,6.84,4.56)], peak=False),
 dict(h=5, L=18.45, tiers=[(0,9.23,8.89),(9.23,5.17,5.33),(14.4,4.05,2.67)], peak=False),
 dict(h=6, L=25.02, tiers=[(0,25.02,9.96),(25.02,0.75,6.97)], peak=False),
 dict(h=7, L=36.13, tiers=[(0,22.4,9.37),(22.4,13.73,5.15)], peak=False),
 dict(h=8, L=44.95, tiers=[(0,22.48,10.61),(22.48,12.59,6.37),(35.07,9.88,3.18)], peak=False),
 dict(h=9, L=47.58, tiers=[(0,47.58,11.38),(47.58,1.43,7.97)], peak=False),
 dict(h=10, L=49.55, tiers=[(0,30.72,12.1),(30.72,18.83,6.66)], peak=False),
 dict(h=11, L=52.5, tiers=[(0,26.25,10.89),(26.25,14.7,6.53),(40.95,11.55,3.27)], peak=False),
 dict(h=12, L=56.28, tiers=[(0,56.28,11.75),(56.28,1.69,8.22)], peak=False),
 dict(h=13, L=58.25, tiers=[(0,36.12,12.47),(36.12,22.13,6.86)], peak=False),
 dict(h=14, L=61.6, tiers=[(0,30.8,11.29),(30.8,17.25,6.77),(48.05,13.55,3.39)], peak=False),
 dict(h=15, L=63.29, tiers=[(0,63.29,11.99),(63.29,1.9,8.39)], peak=False),
 dict(h=16, L=63.05, tiers=[(0,39.09,12.54),(39.09,23.96,6.9)], peak=False),
 dict(h=17, L=68.26, tiers=[(0,34.13,13.51),(34.13,19.11,8.11),(53.24,15.02,4.05)], peak=True),
 dict(h=18, L=71.0, tiers=[(0,71.0,12.29),(71.0,2.13,8.6)], peak=True),
 dict(h=19, L=64.62, tiers=[(0,40.06,12.38),(40.06,24.56,6.81)], peak=True),
 dict(h=20, L=61.63, tiers=[(0,30.81,12.72),(30.81,17.26,7.63),(48.07,13.56,3.82)], peak=False),
 dict(h=21, L=62.84, tiers=[(0,62.84,11.38),(62.84,1.89,7.97)], peak=False),
 dict(h=22, L=59.52, tiers=[(0,36.9,11.7),(36.9,22.62,6.44)], peak=False),
 dict(h=23, L=49.18, tiers=[(0,24.59,11.5),(24.59,13.77,6.9),(38.36,10.82,3.45)], peak=False),
]

slotWidth = 15
heightScale = 1.8
stripWidth = slotWidth * 24
groundY = 108
buildingBaseY = groundY

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

nightProb = [0.75,0.8,0.85,0.85,0.75,0.55,0.35,0.15, 0,0,0,0,0,0,0,0,0,0,0,0, 0.15,0.35,0.55,0.7]
def isLit(i, hour, x, y):
    prob = nightProb[hour % 24]
    return hashUnit(i*12.9898 + x*3.71 + y*7.13) < prob

sortedL = sorted(buildings, key=lambda b: -b['L'])
rankByHour = {b['h']: idx+1 for idx, b in enumerate(sortedL)}

# canvas bounds (unit space)
y_min, y_max = -50, 126
W = int(stripWidth * DRAW)
H = int((y_max - y_min) * DRAW)

def px(x, y):
    return (x*DRAW, (y - y_min)*DRAW)

im = Image.new('RGBA', (W, H), (0,0,0,0))
draw = ImageDraw.Draw(im)

WINDOW_OFF = '#2a4258'
WINDOW_LIT = '#f4c542'
STROKE = '#55555a'
SPIRE = '#6b6b70'

taxi_sprite = Image.open('/Users/davidjbreau/dev/PORTFOLIO/public/img/taxi-pixel.png').convert('RGBA')

# Meme courbe brightness que taxi-daynight / bgTaxiFilter dans TaxiHourlyClock.astro (24 paliers,
# 1 par heure), pour que les taxis de la voie du haut (cuits ici) suivent le meme cycle jour/nuit
# que le taxi heros et les taxis de la voie du bas.
taxiHourBrightness = [
    0.78, 0.76, 0.74, 0.74, 0.78, 0.84, 0.9, 0.94, 0.968, 0.984, 1.0, 1.0,
    1.0, 1.0, 1.0, 1.0, 1.0, 0.984, 0.968, 0.94, 0.912, 0.88, 0.84, 0.8,
]

try:
    font = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', int(3.9*DRAW))
    font_bold = ImageFont.truetype('/System/Library/Fonts/Menlo.ttc', int(3.9*DRAW), index=1)
except Exception:
    font = ImageFont.load_default()
    font_bold = font

topLaneY = groundY
laneHeight = 3.5

# Les nuages sont maintenant des éléments SVG vivants (TaxiHourlyClock.astro), pas cuits ici,
# pour pouvoir les teinter en direct selon l'heure (blancs le jour, plus foncés la nuit).

# Soleil, centre sur l'immeuble de 12h
sun_x = 12*slotWidth + slotWidth/2
sun_y = -28
sun_r = 6
glow0 = px(sun_x-sun_r*1.8, sun_y-sun_r*1.8); glow1 = px(sun_x+sun_r*1.8, sun_y+sun_r*1.8)
draw.ellipse([glow0[0],glow0[1],glow1[0],glow1[1]], fill=(244,197,66,60))
s0 = px(sun_x-sun_r, sun_y-sun_r); s1 = px(sun_x+sun_r, sun_y+sun_r)
draw.ellipse([s0[0],s0[1],s1[0],s1[1]], fill=(244,197,66,255))

# Lune (croissant), centre sur l'immeuble de 0h
moon_x = 0*slotWidth + slotWidth/2
moon_y = -28
moon_r = 5.2
mglow0 = px(moon_x-moon_r*1.35, moon_y-moon_r*1.35); mglow1 = px(moon_x+moon_r*1.35, moon_y+moon_r*1.35)
draw.ellipse([mglow0[0],mglow0[1],mglow1[0],mglow1[1]], fill=(223,228,235,45))
moon_layer = Image.new('L', (W, H), 0)
mdraw = ImageDraw.Draw(moon_layer)
m0 = px(moon_x-moon_r, moon_y-moon_r); m1 = px(moon_x+moon_r, moon_y+moon_r)
mdraw.ellipse([m0[0],m0[1],m1[0],m1[1]], fill=255)
bite_r = moon_r*0.92
bx, by = moon_x+2.4, moon_y-1.0
b0 = px(bx-bite_r, by-bite_r); b1 = px(bx+bite_r, by+bite_r)
mdraw.ellipse([b0[0],b0[1],b1[0],b1[1]], fill=0)
moon_color = Image.new('RGBA', (W, H), (223, 228, 235, 255))
im.paste(moon_color, (0,0), moon_layer)

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
        p0 = px(x0,y0); p1 = px(x1,y1)
        draw.rectangle([p0[0],p0[1],p1[0],p1[1]], fill=bodyColor, outline=STROKE, width=max(1,int(0.5*DRAW)))
        for (wx, wy) in windowsFor(s,l,width):
            if hashUnit(i*33.71 + wx*5.19 + wy*9.02) < 0.12:
                continue
            lit = isLit(i, b['h'], wx, wy)
            realX = xCenter + wy
            realY = buildingBaseY - wx
            wp0 = px(realX-0.7, realY-0.7)
            wp1 = px(realX+0.7, realY+0.7)
            draw.rectangle([wp0[0],wp0[1],wp1[0],wp1[1]], fill=(WINDOW_LIT if lit else WINDOW_OFF))
    if b['peak']:
        sx = xCenter
        sy1 = buildingBaseY - b['L']*heightScale
        sy2 = sy1 - 9
        sp1 = px(sx, sy1); sp2 = px(sx, sy2)
        draw.line([sp1, sp2], fill=SPIRE, width=max(1,int(1.2*DRAW)))
    if b['h'] % 2 == 0:
        lx, ly = px(xCenter, groundY+13)
        txt = f"{b['h']}h"
        emphasize = b['h'] in (0, 12)
        useFont = font_bold if emphasize else font
        bbox = draw.textbbox((0,0), txt, font=useFont)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        fillA = 220 if emphasize else 166
        draw.text((lx - tw/2, ly - th/2 - bbox[1]), txt, font=useFont, fill=(139,149,165,fillA))

    # lampadaire au bord gauche du slot de cet immeuble
    lampX = i*slotWidth
    lampLit = hashUnit(b['h']*4.71 + 1.3) < nightProb[b['h'] % 24]
    lp0 = px(lampX, groundY); lp1 = px(lampX, groundY-5.5)
    draw.line([lp0, lp1], fill=(120,122,130,255), width=max(1,int(0.45*DRAW)))
    headColor = (255,224,140,255) if lampLit else (120,122,130,255)
    hr = 0.75
    h0 = px(lampX-hr, groundY-5.5-hr); h1 = px(lampX+hr, groundY-5.5+hr)
    draw.ellipse([h0[0],h0[1],h1[0],h1[1]], fill=headColor, outline=(60,60,64,255), width=max(1,int(0.15*DRAW)))

    rank = rankByHour.get(b['h'], 24)
    alternateTop = (i % 2 == 0)
    place_top = False
    if rank <= 3:
        place_top = True
    elif rank <= 11:
        place_top = alternateTop
    elif rank <= 21:
        place_top = alternateTop and hashUnit(b['h'] + 0.41) < 0.5
    else:
        place_top = alternateTop and hashUnit(b['h']) < 0.22
    if place_top:
        tx = xCenter - 6
        ty = topLaneY - 3.75
        tp0 = px(tx, ty)
        sprite_w = int(12*DRAW)
        sprite_h = int(7*DRAW)
        resized = taxi_sprite.resize((sprite_w, sprite_h), Image.NEAREST)
        tinted = ImageEnhance.Brightness(resized).enhance(taxiHourBrightness[b['h'] % 24])
        resized_a = tinted.copy()
        resized_a.putalpha(resized.split()[3])
        # apply 0.7 opacity like .bg-taxi
        alpha = resized_a.split()[3].point(lambda p: int(p*0.7))
        resized_a.putalpha(alpha)
        im.alpha_composite(resized_a, (int(tp0[0]), int(tp0[1])))

final = im.resize((int(stripWidth * SCALE), int((y_max - y_min) * SCALE)), Image.LANCZOS)
final.save('/Users/davidjbreau/dev/PORTFOLIO/public/img/skyline-strip.png')
print('saved', final.size)
