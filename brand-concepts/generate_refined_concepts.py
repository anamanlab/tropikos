import os
import math
import cairosvg
from generate_letters import build_glyphs

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

# ==============================================================================
# CONCEPT A: Plano & Topografia
# ==============================================================================
def build_concept_a_symbol():
    # 3x3 grid centered in 256x256
    # Total width/height: 168x168 -> start at (44, 44)
    # Cell size: 46x46, gap: 15
    # Total = 46*3 + 15*2 = 138 + 30 = 168.
    s = 0.46
    gap = 15
    c_w = 46
    c_h = 46
    x0 = 44
    y0 = 44
    
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
        
    # Topography garden at (0, 1):
    gx = x0
    gy = y0 + 1 * (c_h + gap) # 44 + 61 = 105
    # 4 clean, organic contour curves with stroke-width 4.5
    contours = [
        f"M {gx+2} {gy+38} C {gx+14} {gy+30} {gx+24} {gy+42} {gx+44} {gy+36}",
        f"M {gx+2} {gy+27} C {gx+15} {gy+19} {gx+26} {gy+31} {gx+44} {gy+25}",
        f"M {gx+2} {gy+16} C {gx+16} {gy+8} {gx+28} {gy+20} {gx+44} {gy+14}",
        f"M {gx+6} {gy+6} C {gx+18} {gy+1} {gx+30} {gy+9} {gx+44} {gy+3}",
    ]
    contour_paths = "".join([f'<path d="{c}" fill="none" stroke="#191919" stroke-width="4" stroke-linecap="round"/>' for c in contours])
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-a">
  <title id="title-a">Trópikos Arquitetos — Conceito A: Plano &amp; Topografia</title>
  <g id="symbol-a">
    {contour_paths}
    {''.join(paths)}
  </g>
</svg>'''
    return svg

def build_concept_a_lockup():
    # Horizontal lockup: height 256, width 800
    # Left: Symbol scaled to 140x140 at (48, 58)
    # Divider rule at x=224, from y=60 to 196
    # Right: TRÓPIKOS (scale 0.65) at x=260, y=110
    #        ARQUITETOS (scale 0.22, wide tracking) at x=262, y=168
    sym_svg = build_concept_a_symbol()
    # extract inner content of symbol
    s_start = sym_svg.find('<g id="symbol-a">')
    s_end = sym_svg.rfind('</svg>')
    inner = sym_svg[s_start:s_end].strip()
    
    w_t, p_t = typeset_paths("TRÓPIKOS", scale=0.68, tracking=10, fill="#191919")
    w_a, p_a = typeset_paths("ARQUITETOS", scale=0.22, tracking=26, fill="#191919")
    
    # Scale symbol to 130x130 (130/256 = 0.5078)
    s_sym = 0.52
    ox_sym = 45
    oy_sym = 62
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 256" width="820" height="256" role="img" aria-labelledby="title-a-lockup">
  <title id="title-a-lockup">Trópikos Arquitetos — Lockup A</title>
  <g id="symbol" transform="translate({ox_sym}, {oy_sym}) scale({s_sym})">
    {inner}
  </g>
  <line x1="225" y1="62" x2="225" y2="194" stroke="#191919" stroke-width="1.5" opacity="0.3"/>
  <g id="wordmark" transform="translate(265, 82)">
    {''.join(p_t)}
  </g>
  <g id="descriptor" transform="translate(267, 164)">
    {''.join(p_a)}
  </g>
</svg>'''
    return svg

# ==============================================================================
# CONCEPT B (Recommended): Monograma Trópico
# ==============================================================================
def build_concept_b_symbol():
    # Canvas 256x256
    # Architectural T + Topographic Contours in single unified harmony
    # T structure:
    # Lintel (top bar): x=40 to 216 (width 176), y=42 to 80 (height 38)
    # Column (vertical stem): x=80 to 118 (width 38), y=80 to 214 (height 134)
    # The right area under the lintel (x=118..216, y=80..214):
    # 4 concentric isoline curves with stroke-width 7.5, perfectly nested
    
    # Precise concentric arcs:
    # Outer contour 4: arcs from ground (y=214) to right boundary
    # Center of concentric arcs: let's anchor them at (118, 214) or flowing from (130, 214)
    # Line 1 (inner):
    c1 = "M 132 214 C 132 170 144 140 174 122 C 188 114 202 112 216 112"
    # Line 2:
    c2 = "M 152 214 C 152 178 162 152 186 138 C 196 132 206 130 216 130"
    # Line 3:
    c3 = "M 172 214 C 172 188 180 166 198 156 C 204 152 210 150 216 150"
    # Line 4:
    c4 = "M 192 214 C 192 198 198 182 210 174 C 212 172 214 170 216 170"
    
    # Wait, let's reverse the sweep so contours echo natural hill contours ascending:
    # Curves curving outward from column (x=118) down to ground (y=214):
    contours = [
        "M 124 96 C 150 96 166 112 166 138 C 166 168 146 196 124 204",
        "M 142 84 C 176 84 194 106 194 138 C 194 174 170 206 138 214",
        "M 166 80 C 198 84 216 110 216 142 C 216 182 192 212 162 214",
        "M 190 80 C 212 92 222 116 222 144 C 222 178 208 206 184 214",
    ]
    # Let's inspect these 4 curves:
    # c0: radius ~42, from (124, 96) to (124, 204)
    # c1: radius ~60
    # c2: radius ~78
    # c3: radius ~94
    contour_paths = "".join([f'<path d="{c}" fill="none" stroke="#191919" stroke-width="7" stroke-linecap="round"/>' for c in contours])
    
    t_path = "M 40 42 H 216 V 78 H 118 V 214 H 80 V 78 H 40 Z"
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-b">
  <title id="title-b">Trópikos Arquitetos — Conceito B: Monograma Trópico</title>
  <g id="symbol-b">
    <path d="{t_path}" fill="#191919"/>
    {contour_paths}
  </g>
</svg>'''
    return svg

def build_concept_b_lockup():
    sym_svg = build_concept_b_symbol()
    s_start = sym_svg.find('<g id="symbol-b">')
    s_end = sym_svg.rfind('</svg>')
    inner = sym_svg[s_start:s_end].strip()
    
    w_t, p_t = typeset_paths("TRÓPIKOS", scale=0.74, tracking=10, fill="#191919")
    w_a, p_a = typeset_paths("ARQUITETOS", scale=0.24, tracking=28, fill="#191919")
    
    # Symbol scaled to 134x134 (134/256 = 0.523)
    s_sym = 0.54
    ox_sym = 45
    oy_sym = 59
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 256" width="840" height="256" role="img" aria-labelledby="title-b-lockup">
  <title id="title-b-lockup">Trópikos Arquitetos — Lockup B</title>
  <g id="symbol" transform="translate({ox_sym}, {oy_sym}) scale({s_sym})">
    {inner}
  </g>
  <line x1="228" y1="58" x2="228" y2="198" stroke="#191919" stroke-width="1.5" opacity="0.3"/>
  <g id="wordmark" transform="translate(268, 80)">
    {''.join(p_t)}
  </g>
  <g id="descriptor" transform="translate(270, 166)">
    {''.join(p_a)}
  </g>
</svg>'''
    return svg

# ==============================================================================
# CONCEPT C: O Cobogó Trópico
# ==============================================================================
def build_concept_c_symbol():
    # 2x2 Architectural Screen Tile (Cobogó)
    # Total square: 176x176, from (40, 40) to (216, 216)
    # Divided by horizontal hairline gap y=124..132 (gap=8) and vertical gap x=124..132 (gap=8)
    # 4 equal quadrants of 84x84:
    # Q1 (top-left, 40..124, 40..124): Solid block with clean negative T
    # Q2 (top-right, 132..216, 40..124): 3 concentric solar ventilation arcs (cobogó louver)
    # Q3 (bottom-left, 40..124, 132..216): 3 concentric breeze ventilation arcs
    # Q4 (bottom-right, 132..216, 132..216): Solid block with clean negative Ó with sun accent
    
    # Q1: Outer rect x=40, y=40, w=84, h=84.
    # Cutout T: bar x=50..114, y=52..68; stem x=74..90, y=68..112
    # Combined with fill-rule="evenodd"
    q1_path = (
        "M 40 40 H 124 V 124 H 40 Z "
        "M 52 54 H 112 V 68 H 89 V 110 H 75 V 68 H 52 Z"
    )
    
    # Q2 (top-right): 3 concentric arcs radiating from top-right corner (216, 40)
    # Radii: 24, 48, 72
    q2_arcs = [
        "M 192 40 A 24 24 0 0 0 216 64",
        "M 168 40 A 48 48 0 0 0 216 88",
        "M 144 40 A 72 72 0 0 0 216 112",
    ]
    q2_paths = "".join([f'<path d="{a}" fill="none" stroke="#191919" stroke-width="6.5" stroke-linecap="round"/>' for a in q2_arcs])
    
    # Q3 (bottom-left): 3 concentric arcs radiating from bottom-left corner (40, 216)
    # Radii: 24, 48, 72
    q3_arcs = [
        "M 40 192 A 24 24 0 0 1 64 216",
        "M 40 168 A 48 48 0 0 1 88 216",
        "M 40 144 A 72 72 0 0 1 112 216",
    ]
    q3_paths = "".join([f'<path d="{a}" fill="none" stroke="#191919" stroke-width="6.5" stroke-linecap="round"/>' for a in q3_arcs])
    
    # Q4 (bottom-right): Outer rect x=132..216, y=132..216.
    # Cutout Ó: outer circle cx=174, cy=174, r=26; inner hole r=14; sun accent at 45°
    q4_path = (
        "M 132 132 H 216 V 216 H 132 Z "
        "M 174 148 A 26 26 0 1 0 174.1 148 Z "
        "M 174 160 A 14 14 0 1 1 173.9 160 Z "
        "M 188 142 L 198 132 L 204 138 L 194 148 Z"
    )
    
    # Architectural frame borders for Q2 and Q3 to anchor the cobogó block:
    # Outer bounding frame for the 4-tile ensemble
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

def build_concept_c_lockup():
    sym_svg = build_concept_c_symbol()
    s_start = sym_svg.find('<g id="symbol-c">')
    s_end = sym_svg.rfind('</svg>')
    inner = sym_svg[s_start:s_end].strip()
    
    w_t, p_t = typeset_paths("TRÓPIKOS", scale=0.74, tracking=10, fill="#191919")
    w_a, p_a = typeset_paths("ARQUITETOS", scale=0.24, tracking=28, fill="#191919")
    
    s_sym = 0.54
    ox_sym = 45
    oy_sym = 59
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 256" width="840" height="256" role="img" aria-labelledby="title-c-lockup">
  <title id="title-c-lockup">Trópikos Arquitetos — Lockup C</title>
  <g id="symbol" transform="translate({ox_sym}, {oy_sym}) scale({s_sym})">
    {inner}
  </g>
  <line x1="228" y1="58" x2="228" y2="198" stroke="#191919" stroke-width="1.5" opacity="0.3"/>
  <g id="wordmark" transform="translate(268, 80)">
    {''.join(p_t)}
  </g>
  <g id="descriptor" transform="translate(270, 166)">
    {''.join(p_a)}
  </g>
</svg>'''
    return svg

base = "/home/civo/tropikos/brand-concepts"
files = {
    "concept-a-symbol.svg": build_concept_a_symbol(),
    "concept-a-lockup.svg": build_concept_a_lockup(),
    "concept-b-symbol.svg": build_concept_b_symbol(),
    "concept-b-lockup.svg": build_concept_b_lockup(),
    "concept-c-symbol.svg": build_concept_c_symbol(),
    "concept-c-lockup.svg": build_concept_c_lockup(),
}

for name, content in files.items():
    p = os.path.join(base, name)
    with open(p, "w") as f:
        f.write(content)
    print(f"Wrote {name}")

print("All 6 files generated successfully.")
