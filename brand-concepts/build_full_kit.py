import os
import math
import shutil
import cairosvg

def build_glyphs():
    H = 100
    SW = 16
    glyphs = {}

    glyphs['T'] = {
        'w': 66,
        'd': f"M 0 0 H 66 V {SW} H {33 + SW//2} V {H} H {33 - SW//2} V {SW} H 0 Z"
    }
    glyphs['I'] = {
        'w': SW,
        'd': f"M 0 0 H {SW} V {H} H 0 Z"
    }
    glyphs['E'] = {
        'w': 60,
        'd': f"M 0 0 H 60 V {SW} H {SW} V 42 H 54 V 58 H {SW} V {H-SW} H 60 V {H} H 0 Z"
    }
    glyphs['P'] = {
        'w': 68,
        'd': (
            f"M 0 0 H 40 C 55.5 0 68 12.5 68 28 C 68 43.5 55.5 56 40 56 H {SW} V {H} H 0 Z "
            f"M {SW} {SW} H 40 C 46.6 {SW} 52 21.4 52 28 C 52 34.6 46.6 40 40 40 H {SW} Z"
        ),
        'rule': 'evenodd'
    }
    glyphs['R'] = {
        'w': 70,
        'd': (
            f"M 0 0 H 42 C 57.5 0 70 12.5 70 28 C 70 41.5 60.5 52.5 48 55.2 L 70 {H} H 50 L 30 56 H {SW} V {H} H 0 Z "
            f"M {SW} {SW} H 42 C 48.6 {SW} 54 21.4 54 28 C 54 34.6 48.6 40 42 40 H {SW} Z"
        ),
        'rule': 'evenodd'
    }
    glyphs['O'] = {
        'w': 76,
        'd': (
            f"M 38 0 C 59 0 76 17 76 50 C 76 83 59 100 38 100 C 17 100 0 83 0 50 C 0 17 17 0 38 0 Z "
            f"M 38 {SW} C 26 {SW} {SW} 29 {SW} 50 C {SW} 71 26 84 38 84 C 50 84 {76-SW} 71 {76-SW} 50 C {76-SW} 29 50 {SW} 38 {SW} Z"
        ),
        'rule': 'evenodd'
    }
    glyphs['Ó'] = {
        'w': 76,
        'd': glyphs['O']['d'] + f" M 40 -8 L 56 -24 L 66 -16 L 50 0 Z",
        'rule': 'evenodd'
    }
    glyphs['K'] = {
        'w': 68,
        'd': (
            f"M 0 0 H {SW} V 45 L 48 0 H 68 L 30 52 L 68 {H} H 46 L {SW} 60 V {H} H 0 Z"
        )
    }
    glyphs['S'] = {
        'w': 66,
        'd': (
            "M 58 24 L 46 29 C 43 20 37 16 33 16 C 25 16 20 21 20 27 C 20 34 26 37 38 42 "
            "C 54 48 64 54 64 68 C 64 86 49 100 33 100 C 15 100 4 87 2 72 L 17 68 "
            "C 19 79 26 84 33 84 C 42 84 48 78 48 70 C 48 61 41 58 29 52 "
            "C 16 46 4 40 4 27 C 4 12 17 0 33 0 C 48 0 56 10 58 24 Z"
        )
    }
    glyphs['A'] = {
        'w': 74,
        'd': (
            f"M 37 0 L 74 {H} H 55 L 47 76 H 27 L 19 {H} H 0 Z "
            f"M 37 26 L 43 62 H 31 Z"
        ),
        'rule': 'evenodd'
    }
    # Seamless Q:
    glyphs['Q'] = {
        'w': 76,
        'd': (
            "M 38 0 C 59 0 76 17 76 50 C 76 66 69 80 58 89 "
            "L 72 104 H 54 L 46 95 "
            "C 43 97 41 98 38 98 C 17 98 0 81 0 50 C 0 17 17 0 38 0 Z "
            "M 38 16 C 26 16 16 29 16 50 C 16 71 26 82 38 82 C 50 82 60 71 60 50 C 60 29 50 16 38 16 Z"
        ),
        'rule': 'evenodd'
    }
    glyphs['U'] = {
        'w': 72,
        'd': (
            f"M 0 0 H {SW} V 62 C {SW} 76 25 84 36 84 C 47 84 56 76 56 62 V 0 H 72 V 62 "
            f"C 72 86 56 100 36 100 C 16 100 0 86 0 62 Z"
        )
    }
    return glyphs

glyphs = build_glyphs()

def typeset_paths(text, scale, tracking, fill="currentColor"):
    x = 0
    paths = []
    kerning = {
        ('T', 'R'): -4,
        ('R', 'Ó'): -2,
        ('P', 'I'): 2,
        ('K', 'O'): -2,
        ('A', 'R'): -2,
        ('R', 'Q'): -2,
        ('Q', 'U'): -2,
    }
    for i, ch in enumerate(text):
        if ch not in glyphs:
            x += 20 * scale
            continue
        g = glyphs[ch]
        if i > 0:
            pair = (text[i-1], ch)
            if pair in kerning:
                x += kerning[pair] * scale
        rule_attr = ' fill-rule="evenodd"' if g.get('rule') == 'evenodd' else ''
        paths.append(f'<path d="{g["d"]}" transform="translate({round(x, 2)}, 0) scale({scale})"{rule_attr} fill="{fill}"/>')
        x += (g['w'] + tracking) * scale
    return x - (tracking * scale), paths

# Palette
COLOR_INK = "#191919"      # Onyx / Ink (matches site tokens)
COLOR_PALM = "#3D6E60"     # Architectural Palm / Sage Green
COLOR_TERRA = "#BA5424"    # Warm Terracotta
COLOR_WHITE = "#FFFFFF"

# -----------------------------------------------------------------------------
# 1. MASTER SYMBOL (3x3 Grid, 256x256)
# -----------------------------------------------------------------------------
def make_symbol(color_mode="color"):
    # color_mode: "color", "black", "white", "palm"
    if color_mode == "color":
        c_text = COLOR_INK
        c_garden = COLOR_PALM
    elif color_mode == "black":
        c_text = "#000000"
        c_garden = "#000000"
    elif color_mode == "white":
        c_text = COLOR_WHITE
        c_garden = COLOR_WHITE
    elif color_mode == "palm":
        c_text = COLOR_PALM
        c_garden = COLOR_PALM
        
    # Letters in 3x3 grid
    s = 0.46
    gap = 15
    c_w = 46
    c_h = 46
    x0 = 44
    y0 = 47
    
    paths = []
    grid = {
        (0, 0): 'T',
        (1, 0): 'R',
        (2, 0): 'Ó',
        (1, 1): 'P',
        (2, 1): 'I',
        (0, 2): 'K',
        (1, 2): 'O',
        (2, 2): 'S',
    }
    for (col, row), ch in grid.items():
        cx = x0 + col * (c_w + gap)
        cy = y0 + row * (c_h + gap)
        g = glyphs[ch]
        lx = cx + (c_w - g['w'] * s) / 2
        ly = cy + (c_h - 100 * s) / 2
        rule_attr = ' fill-rule="evenodd"' if g.get('rule') == 'evenodd' else ''
        paths.append(f'<path d="{g["d"]}" transform="translate({round(lx, 2)}, {round(ly, 2)}) scale({s})"{rule_attr} fill="{c_text}"/>')
        
    gx = x0
    gy = y0 + 1 * (c_h + gap)
    contours = [
        f"M {gx+3} {gy+38} C {gx+15} {gy+30} {gx+25} {gy+42} {gx+43} {gy+36}",
        f"M {gx+3} {gy+27} C {gx+15} {gy+19} {gx+26} {gy+31} {gx+43} {gy+25}",
        f"M {gx+3} {gy+16} C {gx+16} {gy+8} {gx+28} {gy+20} {gx+43} {gy+14}",
        f"M {gx+7} {gy+6} C {gx+18} {gy+1} {gx+30} {gy+9} {gx+43} {gy+3}",
    ]
    contour_paths = "".join([f'<path d="{c}" fill="none" stroke="{c_garden}" stroke-width="3.8" stroke-linecap="round"/>' for c in contours])
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-sym">
  <title id="title-sym">Trópikos Arquitetos — Símbolo</title>
  <g id="symbol">
    {contour_paths}
    {''.join(paths)}
  </g>
</svg>'''
    return svg

# -----------------------------------------------------------------------------
# 2. MASTER STACKED LOGO (Symbol + 'ARQUITETOS', 256x256)
# -----------------------------------------------------------------------------
def make_stacked(color_mode="color"):
    if color_mode == "color":
        c_text = COLOR_INK
        c_garden = COLOR_PALM
        c_desc = COLOR_TERRA
    elif color_mode == "black":
        c_text = "#000000"
        c_garden = "#000000"
        c_desc = "#000000"
    elif color_mode == "white":
        c_text = COLOR_WHITE
        c_garden = COLOR_WHITE
        c_desc = COLOR_WHITE
    elif color_mode == "palm":
        c_text = COLOR_PALM
        c_garden = COLOR_PALM
        c_desc = COLOR_PALM

    s = 0.44
    gap = 14
    c_w = 46
    c_h = 46
    x0 = 45
    y0 = 32
    
    paths = []
    grid = {
        (0, 0): 'T',
        (1, 0): 'R',
        (2, 0): 'Ó',
        (1, 1): 'P',
        (2, 1): 'I',
        (0, 2): 'K',
        (1, 2): 'O',
        (2, 2): 'S',
    }
    for (col, row), ch in grid.items():
        cx = x0 + col * (c_w + gap)
        cy = y0 + row * (c_h + gap)
        g = glyphs[ch]
        lx = cx + (c_w - g['w'] * s) / 2
        ly = cy + (c_h - 100 * s) / 2
        rule_attr = ' fill-rule="evenodd"' if g.get('rule') == 'evenodd' else ''
        paths.append(f'<path d="{g["d"]}" transform="translate({round(lx, 2)}, {round(ly, 2)}) scale({s})"{rule_attr} fill="{c_text}"/>')
        
    gx = x0
    gy = y0 + 1 * (c_h + gap)
    contours = [
        f"M {gx+3} {gy+38} C {gx+15} {gy+30} {gx+25} {gy+42} {gx+43} {gy+36}",
        f"M {gx+3} {gy+27} C {gx+15} {gy+19} {gx+26} {gy+31} {gx+43} {gy+25}",
        f"M {gx+3} {gy+16} C {gx+16} {gy+8} {gx+28} {gy+20} {gx+43} {gy+14}",
        f"M {gx+7} {gy+6} C {gx+18} {gy+1} {gx+30} {gy+9} {gx+43} {gy+3}",
    ]
    contour_paths = "".join([f'<path d="{c}" fill="none" stroke="{c_garden}" stroke-width="3.8" stroke-linecap="round"/>' for c in contours])
    
    w_d, p_d = typeset_paths("ARQUITETOS", scale=0.18, tracking=15, fill=c_desc)
    dx = x0 + (166 - w_d)/2
    dy = y0 + 3 * (c_h + gap) + 12
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-stacked">
  <title id="title-stacked">Trópikos Arquitetos — Logo Completo</title>
  <g id="symbol">
    {contour_paths}
    {''.join(paths)}
  </g>
  <g id="descriptor" transform="translate({round(dx, 2)}, {dy})">
    {''.join(p_d)}
  </g>
</svg>'''
    return svg

# -----------------------------------------------------------------------------
# 3. MASTER HORIZONTAL LOCKUP (Header / Navbar, 720x256)
# -----------------------------------------------------------------------------
def make_horizontal(color_mode="color"):
    if color_mode == "color":
        c_sym_text = COLOR_INK
        c_garden = COLOR_PALM
        c_wm = COLOR_INK
        c_desc = COLOR_TERRA
        c_rule = COLOR_INK
    elif color_mode == "black":
        c_sym_text = "#000000"
        c_garden = "#000000"
        c_wm = "#000000"
        c_desc = "#000000"
        c_rule = "#000000"
    elif color_mode == "white":
        c_sym_text = COLOR_WHITE
        c_garden = COLOR_WHITE
        c_wm = COLOR_WHITE
        c_desc = COLOR_WHITE
        c_rule = COLOR_WHITE
    elif color_mode == "palm":
        c_sym_text = COLOR_PALM
        c_garden = COLOR_PALM
        c_wm = COLOR_PALM
        c_desc = COLOR_PALM
        c_rule = COLOR_PALM

    w_t, p_t = typeset_paths("TRÓPIKOS", scale=0.64, tracking=9, fill=c_wm)
    w_a, p_a = typeset_paths("ARQUITETOS", scale=0.25, tracking=24, fill=c_desc)
    
    ox_sym = 92
    oy_sym = 59
    x_rule = ox_sym + 150
    x_text = x_rule + 36
    
    # 3x3 symbol inside lockup
    s = 0.46
    gap = 15
    c_w = 46
    c_h = 46
    x0 = 44
    y0 = 47
    
    paths = []
    grid = {
        (0, 0): 'T', (1, 0): 'R', (2, 0): 'Ó',
        (1, 1): 'P', (2, 1): 'I',
        (0, 2): 'K', (1, 2): 'O', (2, 2): 'S',
    }
    for (col, row), ch in grid.items():
        cx = x0 + col * (c_w + gap)
        cy = y0 + row * (c_h + gap)
        g = glyphs[ch]
        lx = cx + (c_w - g['w'] * s) / 2
        ly = cy + (c_h - 100 * s) / 2
        rule_attr = ' fill-rule="evenodd"' if g.get('rule') == 'evenodd' else ''
        paths.append(f'<path d="{g["d"]}" transform="translate({round(lx, 2)}, {round(ly, 2)}) scale({s})"{rule_attr} fill="{c_sym_text}"/>')
        
    gx = x0
    gy = y0 + 1 * (c_h + gap)
    contours = [
        f"M {gx+3} {gy+38} C {gx+15} {gy+30} {gx+25} {gy+42} {gx+43} {gy+36}",
        f"M {gx+3} {gy+27} C {gx+15} {gy+19} {gx+26} {gy+31} {gx+43} {gy+25}",
        f"M {gx+3} {gy+16} C {gx+16} {gy+8} {gx+28} {gy+20} {gx+43} {gy+14}",
        f"M {gx+7} {gy+6} C {gx+18} {gy+1} {gx+30} {gy+9} {gx+43} {gy+3}",
    ]
    contour_paths = "".join([f'<path d="{c}" fill="none" stroke="{c_garden}" stroke-width="3.8" stroke-linecap="round"/>' for c in contours])
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 256" width="720" height="256" role="img" aria-labelledby="title-h">
  <title id="title-h">Trópikos Arquitetos — Lockup Horizontal</title>
  <g id="symbol" transform="translate({ox_sym}, {oy_sym}) scale(0.54)">
    {contour_paths}
    {''.join(paths)}
  </g>
  <line x1="{x_rule}" y1="62" x2="{x_rule}" y2="194" stroke="{c_rule}" stroke-width="1.2"/>
  <g id="wordmark" transform="translate({x_text}, 86)">
    {''.join(p_t)}
  </g>
  <g id="descriptor" transform="translate({x_text+2}, 162)">
    {''.join(p_a)}
  </g>
</svg>'''
    return svg

# -----------------------------------------------------------------------------
# 4. SMALL-SIZE / FAVICON CUT (Optimized for 16px/32px)
# -----------------------------------------------------------------------------
def make_small_symbol():
    # Thickened strokes, bolder contour lines for tiny screens / tabs
    s = 0.50
    gap = 14
    c_w = 48
    c_h = 48
    x0 = 42
    y0 = 42
    paths = []
    grid = {
        (0, 0): 'T', (1, 0): 'R', (2, 0): 'Ó',
        (1, 1): 'P', (2, 1): 'I',
        (0, 2): 'K', (1, 2): 'O', (2, 2): 'S',
    }
    for (col, row), ch in grid.items():
        cx = x0 + col * (c_w + gap)
        cy = y0 + row * (c_h + gap)
        g = glyphs[ch]
        lx = cx + (c_w - g['w'] * s) / 2
        ly = cy + (c_h - 100 * s) / 2
        rule_attr = ' fill-rule="evenodd"' if g.get('rule') == 'evenodd' else ''
        paths.append(f'<path d="{g["d"]}" transform="translate({round(lx, 2)}, {round(ly, 2)}) scale({s})"{rule_attr} fill="{COLOR_INK}"/>')
        
    gx = x0
    gy = y0 + 1 * (c_h + gap)
    # 3 bold contour curves for 16px clarity:
    contours = [
        f"M {gx+2} {gy+38} C {gx+14} {gy+30} {gx+24} {gy+44} {gx+46} {gy+36}",
        f"M {gx+2} {gy+24} C {gx+15} {gy+16} {gx+26} {gy+30} {gx+46} {gy+22}",
        f"M {gx+4} {gy+10} C {gx+16} {gy+4} {gx+28} {gy+16} {gx+46} {gy+8}",
    ]
    contour_paths = "".join([f'<path d="{c}" fill="none" stroke="{COLOR_PALM}" stroke-width="5.5" stroke-linecap="round"/>' for c in contours])
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-small">
  <title id="title-small">Trópikos Arquitetos — Favicon &amp; Small Size</title>
  <g id="symbol">
    {contour_paths}
    {''.join(paths)}
  </g>
</svg>'''
    return svg

# Write all masters
out_dir = "/home/civo/tropikos/brand-kit"
svg_dir = os.path.join(out_dir, "svg")
os.makedirs(svg_dir, exist_ok=True)

masters = {
    # Símbolo
    "tropikos-symbol-color.svg": make_symbol("color"),
    "tropikos-symbol-black.svg": make_symbol("black"),
    "tropikos-symbol-white.svg": make_symbol("white"),
    "tropikos-symbol-palm.svg": make_symbol("palm"),
    "tropikos-symbol-small.svg": make_small_symbol(),
    # Stacked
    "tropikos-stacked-color.svg": make_stacked("color"),
    "tropikos-stacked-black.svg": make_stacked("black"),
    "tropikos-stacked-white.svg": make_stacked("white"),
    "tropikos-stacked-palm.svg": make_stacked("palm"),
    # Horizontal
    "tropikos-horizontal-color.svg": make_horizontal("color"),
    "tropikos-horizontal-black.svg": make_horizontal("black"),
    "tropikos-horizontal-white.svg": make_horizontal("white"),
    "tropikos-horizontal-palm.svg": make_horizontal("palm"),
}

for fname, content in masters.items():
    with open(os.path.join(svg_dir, fname), "w") as f:
        f.write(content)
    print(f"Generated {fname}")

print("All vector masters generated in brand-kit/svg/")
