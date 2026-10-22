import os
import cairosvg
from generate_letters import build_glyphs

glyphs = build_glyphs()

def typeset_paths(text, scale, tracking, fill="#191919"):
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
# CONCEPT A: Plano & Topografia
# -----------------------------------------------------------------------------
def build_a_symbol():
    # Centered in 256x256
    # Total: 168x168 -> x0=44, y0=47 (optical center: top 36, bottom 41 due to accent)
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
        # (0, 1): Garden
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
        paths.append(f'<path d="{g["d"]}" transform="translate({round(lx, 2)}, {round(ly, 2)}) scale({s})"{rule_attr} fill="#191919"/>')
        
    gx = x0
    gy = y0 + 1 * (c_h + gap) # 47 + 61 = 108
    contours = [
        f"M {gx+3} {gy+38} C {gx+15} {gy+30} {gx+25} {gy+42} {gx+43} {gy+36}",
        f"M {gx+3} {gy+27} C {gx+15} {gy+19} {gx+26} {gy+31} {gx+43} {gy+25}",
        f"M {gx+3} {gy+16} C {gx+16} {gy+8} {gx+28} {gy+20} {gx+43} {gy+14}",
        f"M {gx+7} {gy+6} C {gx+18} {gy+1} {gx+30} {gy+9} {gx+43} {gy+3}",
    ]
    contour_paths = "".join([f'<path d="{c}" fill="none" stroke="#191919" stroke-width="3.8" stroke-linecap="round"/>' for c in contours])
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-a">
  <title id="title-a">Trópikos Arquitetos — Conceito A: Plano &amp; Topografia</title>
  <g id="symbol-a">
    {contour_paths}
    {''.join(paths)}
  </g>
</svg>'''
    return svg

def build_a_lockup():
    w_t, p_t = typeset_paths("TRÓPIKOS", scale=0.64, tracking=9, fill="#191919")
    w_a, p_a = typeset_paths("ARQUITETOS", scale=0.25, tracking=24, fill="#191919")
    
    # Sym: scale 0.54 (138px)
    # Content: sym (138) + rule gap (30) + text (320) = 488px
    # Canvas width = 680 -> left margin = (680 - 488) / 2 = 96
    ox_sym = 92
    oy_sym = 59
    x_rule = ox_sym + 150
    x_text = x_rule + 36
    
    sym_svg = build_a_symbol()
    inner = sym_svg[sym_svg.find('<g id="symbol-a">'):sym_svg.rfind('</svg>')].strip()
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 256" width="720" height="256" role="img" aria-labelledby="title-a-lockup">
  <title id="title-a-lockup">Trópikos Arquitetos — Lockup A</title>
  <g id="symbol" transform="translate({ox_sym}, {oy_sym}) scale(0.54)">
    {inner}
  </g>
  <line x1="{x_rule}" y1="62" x2="{x_rule}" y2="194" stroke="#191919" stroke-width="1.2"/>
  <g id="wordmark" transform="translate({x_text}, 86)">
    {''.join(p_t)}
  </g>
  <g id="descriptor" transform="translate({x_text+2}, 162)">
    {''.join(p_a)}
  </g>
</svg>'''
    return svg

# -----------------------------------------------------------------------------
# CONCEPT B (Recommended): Monograma Trópico
# -----------------------------------------------------------------------------
def build_b_symbol():
    # Canvas 256x256
    # Exact geometric harmony:
    # Lintel: x=40 to 216 (width 176), y=42 to 78 (height 36)
    # Column: x=78 to 114 (width 36), y=78 to 214 (height 136)
    # 4 contour curves in the right quadrant (x: 114..216, y: 78..214):
    # Rightmost peak touches x=216 flush with the lintel.
    # Bottom points touch y=214 flush with the column baseline.
    contours = [
        # Line 1 (inner):
        "M 126 96 C 148 96 162 110 162 134 C 162 164 144 192 124 204",
        # Line 2:
        "M 144 84 C 174 84 190 104 190 136 C 190 172 168 204 140 214",
        # Line 3:
        "M 168 80 C 196 82 210 108 210 138 C 210 176 188 208 162 214",
        # Line 4 (outermost, flush with lintel x=216):
        "M 194 78 C 212 90 216 114 216 140 C 216 178 204 206 184 214",
    ]
    contour_paths = "".join([f'<path d="{c}" fill="none" stroke="#191919" stroke-width="6.5" stroke-linecap="round"/>' for c in contours])
    t_path = "M 40 42 H 216 V 78 H 114 V 214 H 78 V 78 H 40 Z"
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-b">
  <title id="title-b">Trópikos Arquitetos — Conceito B: Monograma Trópico</title>
  <g id="symbol-b">
    <path d="{t_path}" fill="#191919"/>
    {contour_paths}
  </g>
</svg>'''
    return svg

def build_b_lockup():
    w_t, p_t = typeset_paths("TRÓPIKOS", scale=0.70, tracking=9, fill="#191919")
    w_a, p_a = typeset_paths("ARQUITETOS", scale=0.26, tracking=26, fill="#191919")
    
    ox_sym = 88
    oy_sym = 57
    x_rule = ox_sym + 152
    x_text = x_rule + 36
    
    sym_svg = build_b_symbol()
    inner = sym_svg[sym_svg.find('<g id="symbol-b">'):sym_svg.rfind('</svg>')].strip()
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 256" width="740" height="256" role="img" aria-labelledby="title-b-lockup">
  <title id="title-b-lockup">Trópikos Arquitetos — Lockup B</title>
  <g id="symbol" transform="translate({ox_sym}, {oy_sym}) scale(0.55)">
    {inner}
  </g>
  <line x1="{x_rule}" y1="58" x2="{x_rule}" y2="198" stroke="#191919" stroke-width="1.2"/>
  <g id="wordmark" transform="translate({x_text}, 84)">
    {''.join(p_t)}
  </g>
  <g id="descriptor" transform="translate({x_text+2}, 164)">
    {''.join(p_a)}
  </g>
</svg>'''
    return svg

# -----------------------------------------------------------------------------
# CONCEPT C: O Cobogó Trópico
# -----------------------------------------------------------------------------
def build_c_symbol():
    # 2x2 Architectural Tile
    # Quadrants:
    # Q1: 40..124, 40..124 (Solid with negative T)
    # Q2: 132..216, 40..124 (Concentric cobogó arcs)
    # Q3: 40..124, 132..216 (Concentric cobogó arcs)
    # Q4: 132..216, 132..216 (Solid with negative Ó)
    
    q1_path = (
        "M 40 40 H 124 V 124 H 40 Z "
        "M 52 54 H 112 V 68 H 89 V 110 H 75 V 68 H 52 Z"
    )
    q2_arcs = [
        "M 192 40 A 24 24 0 0 0 216 64",
        "M 168 40 A 48 48 0 0 0 216 88",
        "M 144 40 A 72 72 0 0 0 216 112",
    ]
    q2_paths = "".join([f'<path d="{a}" fill="none" stroke="#191919" stroke-width="6.5" stroke-linecap="round"/>' for a in q2_arcs])
    
    q3_arcs = [
        "M 40 192 A 24 24 0 0 1 64 216",
        "M 40 168 A 48 48 0 0 1 88 216",
        "M 40 144 A 72 72 0 0 1 112 216",
    ]
    q3_paths = "".join([f'<path d="{a}" fill="none" stroke="#191919" stroke-width="6.5" stroke-linecap="round"/>' for a in q3_arcs])
    
    q4_path = (
        "M 132 132 H 216 V 216 H 132 Z "
        "M 174 148 A 26 26 0 1 0 174.1 148 Z "
        "M 174 160 A 14 14 0 1 1 173.9 160 Z "
        "M 188 142 L 198 132 L 204 138 L 194 148 Z"
    )
    
    frame = (
        '<rect x="40" y="40" width="176" height="176" rx="4" fill="none" stroke="#191919" stroke-width="2"/>'
        '<line x1="128" y1="40" x2="128" y2="216" stroke="#191919" stroke-width="2"/>'
        '<line x1="40" y1="128" x2="216" y2="128" stroke="#191919" stroke-width="2"/>'
    )
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-c">
  <title id="title-c">Trópikos Arquitetos — Conceito C: O Cobogó Trópico</title>
  <g id="symbol-c">
    {frame}
    <path d="{q1_path}" fill="#191919" fill-rule="evenodd"/>
    {q2_paths}
    {q3_paths}
    <path d="{q4_path}" fill="#191919" fill-rule="evenodd"/>
  </g>
</svg>'''
    return svg

def build_c_lockup():
    w_t, p_t = typeset_paths("TRÓPIKOS", scale=0.70, tracking=9, fill="#191919")
    w_a, p_a = typeset_paths("ARQUITETOS", scale=0.26, tracking=26, fill="#191919")
    
    ox_sym = 88
    oy_sym = 57
    x_rule = ox_sym + 152
    x_text = x_rule + 36
    
    sym_svg = build_c_symbol()
    inner = sym_svg[sym_svg.find('<g id="symbol-c">'):sym_svg.rfind('</svg>')].strip()
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 740 256" width="740" height="256" role="img" aria-labelledby="title-c-lockup">
  <title id="title-c-lockup">Trópikos Arquitetos — Lockup C</title>
  <g id="symbol" transform="translate({ox_sym}, {oy_sym}) scale(0.55)">
    {inner}
  </g>
  <line x1="{x_rule}" y1="58" x2="{x_rule}" y2="198" stroke="#191919" stroke-width="1.2"/>
  <g id="wordmark" transform="translate({x_text}, 84)">
    {''.join(p_t)}
  </g>
  <g id="descriptor" transform="translate({x_text+2}, 164)">
    {''.join(p_a)}
  </g>
</svg>'''
    return svg

base = "/home/civo/tropikos/brand-concepts"
files = {
    "concept-a-symbol.svg": build_a_symbol(),
    "concept-a-lockup.svg": build_a_lockup(),
    "concept-b-symbol.svg": build_b_symbol(),
    "concept-b-lockup.svg": build_b_lockup(),
    "concept-c-symbol.svg": build_c_symbol(),
    "concept-c-lockup.svg": build_c_lockup(),
}

for name, content in files.items():
    with open(os.path.join(base, name), "w") as f:
        f.write(content)
    print(f"Updated {name}")
