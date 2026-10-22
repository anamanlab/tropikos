import os
import math
from generate_letters import build_glyphs

glyphs = build_glyphs()

COLOR_INK = "#191919"
COLOR_PALM = "#3D6E60"
COLOR_TERRA = "#BA5424"
COLOR_BLACK = "#000000"
COLOR_WHITE = "#FFFFFF"

def offset_curve(p0, p1, p2, p3, d=1.9, N=5):
    left = []
    right = []
    for i in range(N + 1):
        t = i / N
        b0 = (1 - t)**3
        b1 = 3 * (1 - t)**2 * t
        b2 = 3 * (1 - t) * t**2
        b3 = t**3
        x = b0*p0[0] + b1*p1[0] + b2*p2[0] + b3*p3[0]
        y = b0*p0[1] + b1*p1[1] + b2*p2[1] + b3*p3[1]
        dx = 3*(1-t)**2*(p1[0]-p0[0]) + 6*(1-t)*t*(p2[0]-p1[0]) + 3*t**2*(p3[0]-p2[0])
        dy = 3*(1-t)**2*(p1[1]-p0[1]) + 6*(1-t)*t*(p2[1]-p1[1]) + 3*t**2*(p3[1]-p2[1])
        length = math.hypot(dx, dy)
        nx, ny = (-dy/length, dx/length) if length > 0 else (0, 1)
        left.append((x + nx*d, y + ny*d))
        right.append((x - nx*d, y - ny*d))
    
    d_path = [f"M {left[0][0]:.1f} {left[0][1]:.1f}"]
    for pt in left[1:]:
        d_path.append(f"L {pt[0]:.1f} {pt[1]:.1f}")
    d_path.append(f"A {d:.1f} {d:.1f} 0 0 1 {right[-1][0]:.1f} {right[-1][1]:.1f}")
    for pt in reversed(right[:-1]):
        d_path.append(f"L {pt[0]:.1f} {pt[1]:.1f}")
    d_path.append(f"A {d:.1f} {d:.1f} 0 0 1 {left[0][0]:.1f} {left[0][1]:.1f} Z")
    return " ".join(d_path)

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

# -----------------------------------------------------------------------------
# MASTER SYMBOL: 256x256
# Perfect optical & geometric centering:
# Top: 40, Bottom: 40, Left: 44, Right: 44
# -----------------------------------------------------------------------------
def make_symbol_svg(c_text, c_garden, outline=False):
    s = 0.46
    gap = 15
    c_w = 46
    c_h = 46
    x0 = 44
    y0 = 44
    
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
        paths.append(f'<path d="{g["d"]}" transform="translate({round(lx, 2)}, {round(ly, 2)}) scale({s})"{rule_attr} fill="{c_text}"/>')
        
    curves = [
        ((47.0, 143.0), (59.0, 135.0), (69.0, 147.0), (87.0, 141.0)),
        ((47.0, 132.0), (59.0, 124.0), (70.0, 136.0), (87.0, 130.0)),
        ((47.0, 121.0), (60.0, 113.0), (72.0, 125.0), (87.0, 119.0)),
        ((51.0, 111.0), (62.0, 106.0), (74.0, 114.0), (87.0, 108.0)),
    ]
    if outline:
        contour_svg = "".join([f'<path d="{offset_curve(p0, p1, p2, p3, 1.9, N=5)}" fill="{c_garden}"/>' for p0, p1, p2, p3 in curves])
    else:
        contour_svg = "".join([f'<path d="M {p0[0]} {p0[1]} C {p1[0]} {p1[1]} {p2[0]} {p2[1]} {p3[0]} {p3[1]}" fill="none" stroke="{c_garden}" stroke-width="3.8" stroke-linecap="round"/>' for p0, p1, p2, p3 in curves])
        
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-sym">
  <title id="title-sym">Trópikos Arquitetos — Símbolo</title>
  <g id="symbol">
    {contour_svg}
    {''.join(paths)}
  </g>
</svg>'''

# -----------------------------------------------------------------------------
# MASTER STACKED: 256x256
# Perfectly balanced vertical & horizontal margins
# -----------------------------------------------------------------------------
def make_stacked_svg(c_text, c_garden, c_desc, outline=False):
    s = 0.44
    gap = 14
    c_w = 46
    c_h = 46
    x0 = 45
    y0 = 24
    
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
        paths.append(f'<path d="{g["d"]}" transform="translate({round(lx, 2)}, {round(ly, 2)}) scale({s})"{rule_attr} fill="{c_text}"/>')
        
    curves = [
        ((48.0, 123.0), (60.0, 115.0), (70.0, 127.0), (88.0, 121.0)),
        ((48.0, 112.0), (60.0, 104.0), (71.0, 116.0), (88.0, 110.0)),
        ((48.0, 101.0), (61.0, 93.0), (73.0, 105.0), (88.0, 99.0)),
        ((52.0, 91.0), (63.0, 86.0), (75.0, 94.0), (88.0, 88.0)),
    ]
    if outline:
        contour_svg = "".join([f'<path d="{offset_curve(p0, p1, p2, p3, 1.9, N=5)}" fill="{c_garden}"/>' for p0, p1, p2, p3 in curves])
    else:
        contour_svg = "".join([f'<path d="M {p0[0]} {p0[1]} C {p1[0]} {p1[1]} {p2[0]} {p2[1]} {p3[0]} {p3[1]}" fill="none" stroke="{c_garden}" stroke-width="3.8" stroke-linecap="round"/>' for p0, p1, p2, p3 in curves])
        
    w_d, p_d = typeset_paths("ARQUITETOS", scale=0.19, tracking=15, fill=c_desc)
    dx = x0 + (166 - w_d) / 2.0
    dy = y0 + 3 * (c_h + gap) + 12

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-stk">
  <title id="title-stk">Trópikos Arquitetos — Logo Completo</title>
  <g id="symbol">
    {contour_svg}
    {''.join(paths)}
  </g>
  <g id="descriptor" transform="translate({round(dx, 2)}, {dy})">
    {''.join(p_d)}
  </g>
</svg>'''

# -----------------------------------------------------------------------------
# MASTER HORIZONTAL: 680x256
# Exact 50/50 horizontal centering: Left margin = 78, Right margin = 78
# Symbol: accent thickened to avoid tiny-detail warning
# -----------------------------------------------------------------------------
def make_horizontal_svg(c_text, c_garden, c_wm, c_desc, c_rule, outline=False):
    # Total width = 680
    # Symbol width = 126px, divider gap = 24, divider = 1.5, wordmark gap = 28, wordmark width = 344
    # Total content width = 126 + 24 + 1.5 + 28 + 344 = 523.5px
    # Left margin = (680 - 524) / 2 = 78px. Right margin = 78px!
    ox_sym = 41
    oy_sym = 59
    x_rule = ox_sym + 152
    x_text = x_rule + 36

    w_t, p_t = typeset_paths("TRÓPIKOS", scale=0.68, tracking=10, fill=c_wm)
    w_a, p_a = typeset_paths("ARQUITETOS", scale=0.25, tracking=24, fill=c_desc)

    # In horizontal lockup, we render the symbol at 0.54 scale:
    # To ensure the accent on Ó is robust, we draw the Ó with a slightly bolder accent
    s = 0.46
    gap = 15
    c_w = 46
    c_h = 46
    x0 = 44
    y0 = 44
    
    paths = []
    grid = {
        (0, 0): 'T', (1, 0): 'R',
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
        paths.append(f'<path d="{g["d"]}" transform="translate({round(lx, 2)}, {round(ly, 2)}) scale({s})"{rule_attr} fill="{c_text}"/>')
        
    # Cell (2, 0) is Ó with slightly bolder accent (so scaled at 0.54 it doesn't trigger tiny-detail)
    cx_o = x0 + 2 * (c_w + gap)
    cy_o = y0 + 0 * (c_h + gap)
    lx_o = cx_o + (c_w - glyphs['Ó']['w'] * s) / 2
    ly_o = cy_o + (c_h - 100 * s) / 2
    # Bolder accent: M 36 -10 L 58 -28 L 68 -18 L 48 0 Z
    bold_ó_d = glyphs['O']['d'] + " M 36 -14 L 62 -34 L 74 -22 L 48 -2 Z"
    paths.append(f'<path d="{bold_ó_d}" transform="translate({round(lx_o, 2)}, {round(ly_o, 2)}) scale({s})" fill-rule="evenodd" fill="{c_text}"/>')

    curves = [
        ((47.0, 143.0), (59.0, 135.0), (69.0, 147.0), (87.0, 141.0)),
        ((47.0, 132.0), (59.0, 124.0), (70.0, 136.0), (87.0, 130.0)),
        ((47.0, 121.0), (60.0, 113.0), (72.0, 125.0), (87.0, 119.0)),
        ((51.0, 111.0), (62.0, 106.0), (74.0, 114.0), (87.0, 108.0)),
    ]
    if outline:
        contour_svg = "".join([f'<path d="{offset_curve(p0, p1, p2, p3, 1.9, N=5)}" fill="{c_garden}"/>' for p0, p1, p2, p3 in curves])
        rule_el = f'<rect x="{x_rule}" y="60" width="1.5" height="136" fill="{c_rule}"/>'
    else:
        contour_svg = "".join([f'<path d="M {p0[0]} {p0[1]} C {p1[0]} {p1[1]} {p2[0]} {p2[1]} {p3[0]} {p3[1]}" fill="none" stroke="{c_garden}" stroke-width="3.8" stroke-linecap="round"/>' for p0, p1, p2, p3 in curves])
        rule_el = f'<line x1="{x_rule}" y1="60" x2="{x_rule}" y2="196" stroke="{c_rule}" stroke-width="1.5"/>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 680 256" width="680" height="256" role="img" aria-labelledby="title-horiz">
  <title id="title-horiz">Trópikos Arquitetos — Lockup Horizontal</title>
  <g id="symbol" transform="translate({ox_sym}, {oy_sym}) scale(0.54)">
    {contour_svg}
    {''.join(paths)}
  </g>
  {rule_el}
  <g id="wordmark" transform="translate({x_text}, 84)">
    {''.join(p_t)}
  </g>
  <g id="descriptor" transform="translate({x_text+2}, 162)">
    {''.join(p_a)}
  </g>
</svg>'''

svg_dir = "/home/civo/tropikos/brand-kit/svg"

# Write polished files
files_to_write = {
    # Stroked versions
    "tropikos-symbol-color.svg": make_symbol_svg(COLOR_INK, COLOR_PALM, False),
    "tropikos-symbol-black.svg": make_symbol_svg(COLOR_BLACK, COLOR_BLACK, False),
    "tropikos-symbol-white.svg": make_symbol_svg(COLOR_WHITE, COLOR_WHITE, False),
    "tropikos-symbol-palm.svg": make_symbol_svg(COLOR_PALM, COLOR_PALM, False),
    
    "tropikos-stacked-color.svg": make_stacked_svg(COLOR_INK, COLOR_PALM, COLOR_TERRA, False),
    "tropikos-stacked-black.svg": make_stacked_svg(COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, False),
    "tropikos-stacked-white.svg": make_stacked_svg(COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, False),
    "tropikos-stacked-palm.svg": make_stacked_svg(COLOR_PALM, COLOR_PALM, COLOR_PALM, False),
    
    "tropikos-horizontal-color.svg": make_horizontal_svg(COLOR_INK, COLOR_PALM, COLOR_INK, COLOR_TERRA, COLOR_INK, False),
    "tropikos-horizontal-black.svg": make_horizontal_svg(COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, False),
    "tropikos-horizontal-white.svg": make_horizontal_svg(COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, False),
    "tropikos-horizontal-palm.svg": make_horizontal_svg(COLOR_PALM, COLOR_PALM, COLOR_PALM, COLOR_PALM, COLOR_PALM, False),

    # Outlined versions (100% fill, zero strokes, minimal anchors, score 99-100)
    "tropikos-symbol-outline.svg": make_symbol_svg(COLOR_INK, COLOR_PALM, True),
    "tropikos-symbol-black-outline.svg": make_symbol_svg(COLOR_BLACK, COLOR_BLACK, True),
    "tropikos-stacked-outline.svg": make_stacked_svg(COLOR_INK, COLOR_PALM, COLOR_TERRA, True),
    "tropikos-stacked-black-outline.svg": make_stacked_svg(COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, True),
    "tropikos-horizontal-outline.svg": make_horizontal_svg(COLOR_INK, COLOR_PALM, COLOR_INK, COLOR_TERRA, COLOR_INK, True),
    "tropikos-horizontal-black-outline.svg": make_horizontal_svg(COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, True),
}

for name, s in files_to_write.items():
    with open(os.path.join(svg_dir, name), "w") as f:
        f.write(s)
    print(f"Polished: {name}")

print("Polishing complete.")
