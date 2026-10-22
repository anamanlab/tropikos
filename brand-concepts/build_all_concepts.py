import os
import math
import cairosvg
from generate_letters import build_glyphs

glyphs = build_glyphs()

def get_glyph_path(ch, x, y, scale):
    g = glyphs.get(ch)
    if not g:
        return ""
    d = g['d']
    return f'<path d="{d}" transform="translate({round(x, 2)}, {round(y, 2)}) scale({scale})" fill="currentColor"/>'

def typeset_horizontal(text, scale, tracking):
    # Returns (total_width, list of path strings)
    x = 0
    paths = []
    kerning = {
        ('T', 'R'): -4,
        ('R', 'Ó'): -2,
        ('P', 'I'): 2,
        ('K', 'O'): -2,
        ('A', 'R'): -2,
        ('R', 'Q'): -2,
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
        paths.append(f'<path d="{g["d"]}" transform="translate({round(x, 2)}, 0) scale({scale})" fill="currentColor"/>')
        x += (g['w'] + tracking) * scale
    return x - (tracking * scale), paths

# -------------------------------------------------------------
# CONCEPT A: Plano & Topografia (Typographic Cadence 3x3 Grid)
# -------------------------------------------------------------
# Canvas: 256x256
# 3x3 grid:
# Row 0: T, R, Ó
# Row 1: [Topography Garden], P, I
# Row 2: K, O, S
def make_concept_a_symbol():
    # Grid coordinates
    # Total size 176x176, centered in 256x256 -> start at (40, 40)
    # Cell size: 48x48, gap = 16
    # Letters scaled to fit 48h (scale = 48/100 = 0.48)
    s = 0.48
    gap = 16
    c_w = 48
    c_h = 48
    x0 = 40
    y0 = 40
    
    paths = []
    
    # Cells:
    # (col, row): char
    grid = {
        (0, 0): 'T',
        (1, 0): 'R',
        (2, 0): 'Ó',
        # (0, 1) is garden!
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
        # center letter in cell
        lx = cx + (c_w - g['w'] * s) / 2
        ly = cy + (c_h - 100 * s) / 2
        paths.append(f'<path d="{g["d"]}" transform="translate({round(lx, 2)}, {round(ly, 2)}) scale({s})" fill="#191919"/>')
        
    # Topography Garden at (0, 1): cx = 40, cy = 40 + 48 + 16 = 104
    gx = x0
    gy = y0 + 1 * (c_h + gap) # 104
    # A crisp square with 4 smooth contour isolines
    # We can create a subtle container or organic isolines
    # To be production-ready and work in 1-color, we draw smooth topographic curves with stroke-width 3
    # Or filled ribbon contours:
    # 4 contour curves flowing diagonally through the cell:
    contours = [
        f"M {gx+4} {gy+38} C {gx+14} {gy+30} {gx+20} {gy+42} {gx+38} {gy+44}",
        f"M {gx+4} {gy+26} C {gx+16} {gy+16} {gx+28} {gy+34} {gx+44} {gy+32}",
        f"M {gx+4} {gy+14} C {gx+18} {gy+6} {gx+32} {gy+22} {gx+44} {gy+18}",
        f"M {gx+14} {gy+4} C {gx+26} {gy+4} {gx+38} {gy+10} {gx+44} {gy+6}",
    ]
    # We can draw these with a solid fill ribbon or stroke
    # To pass svg_audit and scale cleanly, let's use filled outline paths or stroke:
    contour_paths = "".join([f'<path d="{c}" fill="none" stroke="#191919" stroke-width="3.5" stroke-linecap="round"/>' for c in contours])
    
    # Subtle architectural corner markers for the garden cell (like an architectural floor plan plot)
    corner_marker = f'<rect x="{gx}" y="{gy}" width="{c_w}" height="{c_h}" fill="none" stroke="#191919" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.3"/>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-a">
  <title id="title-a">Trópikos Arquitetos — Plano &amp; Topografia</title>
  <g fill-rule="evenodd">
    {corner_marker}
    {contour_paths}
    {''.join(paths)}
  </g>
</svg>'''
    return svg

# -------------------------------------------------------------
# CONCEPT B (Recommended): Monograma Trópico (Topographic T)
# -------------------------------------------------------------
# Canvas: 256x256
# A powerful architectural monogram:
# Inside an architectural square or shield:
# A bold modernist T whose right side seamlessly flows into 4 topographic contour layers
# In one-color black on white, with absolute clarity at 16px!
def make_concept_b_symbol():
    # Construction:
    # Box from x=36, y=36, width 184, height 184, rx=12 (architectural softened block)
    # The T structure:
    # Top bar: spans x=36 to 220, y=36 to 76 (thickness 40)
    # Vertical column: x=76 to 116, y=76 to 220 (thickness 40)
    # In the right void (x=116..220, y=76..220), 4 rhythmic topographic isolines flow smoothly
    # from the ground up towards the column, evoking the meeting of coastal Recife topography and structure!
    
    # Let's craft the exact paths:
    # Top bar:
    # M 36 36 H 220 V 76 H 36 Z
    # Column:
    # M 76 76 H 116 V 220 H 76 Z
    # Contour curves in the right quadrant (x: 128..220, y: 88..208):
    # Smooth Béziers that ripple outward like contour lines on an architectural topography model:
    contours = [
        # Line 1: inner contour
        "M 126 94 C 146 94 158 108 158 126 C 158 144 146 160 126 164",
        # Line 2: mid contour
        "M 126 80 C 162 80 182 102 182 132 C 182 162 162 186 126 192",
        # Line 3: outer contour
        "M 148 76 C 182 76 208 100 208 136 C 208 174 182 208 138 214",
        # Line 4: outermost contour
        "M 178 76 C 204 88 220 114 220 144 C 220 178 202 210 168 220",
    ]
    contour_svg = "".join([f'<path d="{c}" fill="none" stroke="#191919" stroke-width="7" stroke-linecap="round"/>' for c in contours])
    
    # Solid T:
    t_path = (
        "M 36 36 H 220 V 74 H 118 V 220 H 76 V 74 H 36 Z"
    )
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-b">
  <title id="title-b">Trópikos Arquitetos — Monograma Trópico</title>
  <g fill="#191919">
    <path d="{t_path}"/>
  </g>
  {contour_svg}
</svg>'''
    return svg

# -------------------------------------------------------------
# CONCEPT C: O Cobogó / Pátio (Bioclimatic Geometry)
# -------------------------------------------------------------
# Canvas: 256x256
# Inspired by Brazilian Modernist screen blocks (cobogós) and Burle Marx landscape architecture:
# A circular emblem or 4-quadrant square containing:
# Top-Left: Pure architectural T column & beam
# Top-Right: Pure architectural Ó with acute sun-beam
# Bottom: Interlocking circular arcs forming the permeable cobogó ventilation matrix
def make_concept_c_symbol():
    # 4-quadrant modular circle emblem, diameter 184 (radius 92), centered at (128, 128)
    # Hairline cross separating quadrants (gap = 8)
    # Top-Left quadrant (x: 36..124, y: 36..124): The "T"
    # Top-Right quadrant (x: 132..220, y: 36..124): The "Ó"
    # Bottom-Left & Bottom-Right: Modernist wave cobogó curves (brise-soleil)
    
    # Let's make an architectural round emblem:
    # Outer circle r=92, cx=128, cy=128
    # Cut by horizontal gap y=124..132 and vertical gap x=124..132
    
    # Q1 (top-left, x: 36..124, y: 36..124):
    # Semicircular quadrant with a bold T knocked out or positive T:
    # Let's make positive geometric forms:
    # T in top-left:
    # bar: x=46..122, y=52..68; stem: x=76..92, y=68..122
    t_q1 = "M 46 52 H 122 V 68 H 92 V 122 H 76 V 68 H 46 Z"
    
    # Q2 (top-right, x: 132..220, y: 36..124):
    # Geometric Ó:
    # Outer circle in Q2: cx=168, cy=88, r=32; inner r=18
    # Sun accent at 45°
    o_q2 = (
        "M 168 56 A 32 32 0 1 1 167.9 56 Z "
        "M 168 70 A 18 18 0 1 0 168.1 70 Z "
        "M 184 46 L 198 32 L 206 40 L 192 54 Z"
    )
    
    # Bottom half (y: 132..220):
    # Concentric cobogó ripples / breeze curves:
    # Semicircular concentric arcs centered at (128, 132) curving down:
    arcs = [
        "M 60 134 A 68 68 0 0 0 196 134",
        "M 76 134 A 52 52 0 0 0 180 134",
        "M 92 134 A 36 36 0 0 0 164 134",
        "M 108 134 A 20 20 0 0 0 148 134",
    ]
    arc_svg = "".join([f'<path d="{a}" fill="none" stroke="#191919" stroke-width="6" stroke-linecap="round"/>' for a in arcs])
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-c">
  <title id="title-c">Trópikos Arquitetos — O Cobogó Trópico</title>
  <g fill="#191919" fill-rule="evenodd">
    <path d="{t_q1}"/>
    <path d="{o_q2}"/>
  </g>
  {arc_svg}
</svg>'''
    return svg

os.makedirs("/home/civo/tropikos/brand-concepts", exist_ok=True)

with open("/home/civo/tropikos/brand-concepts/concept-a-symbol.svg", "w") as f:
    f.write(make_concept_a_symbol())

with open("/home/civo/tropikos/brand-concepts/concept-b-symbol.svg", "w") as f:
    f.write(make_concept_b_symbol())

with open("/home/civo/tropikos/brand-concepts/concept-c-symbol.svg", "w") as f:
    f.write(make_concept_c_symbol())

print("Built 3 symbols in SVG.")
