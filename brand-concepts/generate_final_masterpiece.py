import os
import math
import shutil
import cairosvg
from generate_letters import build_glyphs
from test_offset import offset_cubic

glyphs = build_glyphs()

# -----------------------------------------------------------------------------
# PALETTE DEFINITION
# -----------------------------------------------------------------------------
COLOR_INK = "#191919"         # Onyx — Primary ink of the architecture monograph
COLOR_PALM = "#3D6E60"        # Architectural Palm / Sage — Tropical isoline terrain
COLOR_TERRA = "#BA5424"       # Barro Cozido / Terracotta — Earth & ceramic warmth
COLOR_BLACK = "#000000"       # Pure Black — High contrast / technical drawings
COLOR_WHITE = "#FFFFFF"       # Paper White — Inverted dark-mode / blueprints

# -----------------------------------------------------------------------------
# HELPER: Typeset letterforms into clean path strings
# -----------------------------------------------------------------------------
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
# 1. MATHEMATICAL GEOMETRY: 3x3 MATRIZ & TOPOGRAPHIC COURTYARD
# -----------------------------------------------------------------------------
# Grid specifications:
# Canvas: 256 x 256
# Cell size: 46 x 46, Gap: 15
# Total grid footprint: 46*3 + 15*2 = 168 x 168
# Perfectly centered: x0 = 44, y0 = 44 (margins: left 44, right 44, top 44, bottom 44)
# Letter scale: 0.46 (cap-height = 46px)
# Letters placed in 8 cells; cell (0, 1) is the Topographic Courtyard.

# The 4 Topographic Isoline Curves (Curvas de Nível)
# Defined by cubic Bézier control points inside cell (0, 1) [gx=44, gy=105]
curve_definitions = [
    # Curve 1 (deepest contour)
    ((47.0, 143.0), (59.0, 135.0), (69.0, 147.0), (87.0, 141.0)),
    # Curve 2
    ((47.0, 132.0), (59.0, 124.0), (70.0, 136.0), (87.0, 130.0)),
    # Curve 3
    ((47.0, 121.0), (60.0, 113.0), (72.0, 125.0), (87.0, 119.0)),
    # Curve 4 (uppermost contour)
    ((51.0, 111.0), (62.0, 106.0), (74.0, 114.0), (87.0, 108.0)),
]

def get_stroked_contours(color, sw=3.8):
    paths = []
    for p0, p1, p2, p3 in curve_definitions:
        d = f"M {p0[0]} {p0[1]} C {p1[0]} {p1[1]} {p2[0]} {p2[1]} {p3[0]} {p3[1]}"
        paths.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')
    return "".join(paths)

def get_filled_outline_contours(color, sw=3.8):
    paths = []
    r = sw / 2.0
    for p0, p1, p2, p3 in curve_definitions:
        d = offset_cubic(p0, p1, p2, p3, r)
        paths.append(f'<path d="{d}" fill="{color}"/>')
    return "".join(paths)

def get_grid_letter_paths(color, s=0.46, x0=44, y0=44, gap=15, c_w=46, c_h=46):
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
        paths.append(f'<path d="{g["d"]}" transform="translate({round(lx, 2)}, {round(ly, 2)}) scale({s})"{rule_attr} fill="{color}"/>')
    return "".join(paths)

# -----------------------------------------------------------------------------
# BUILD MASTER SYMBOL (256x256)
# -----------------------------------------------------------------------------
def build_symbol(color_mode="color", outline=False):
    if color_mode == "color":
        c_text, c_garden = COLOR_INK, COLOR_PALM
    elif color_mode == "black":
        c_text, c_garden = COLOR_BLACK, COLOR_BLACK
    elif color_mode == "white":
        c_text, c_garden = COLOR_WHITE, COLOR_WHITE
    elif color_mode == "palm":
        c_text, c_garden = COLOR_PALM, COLOR_PALM
    elif color_mode == "terra":
        c_text, c_garden = COLOR_TERRA, COLOR_TERRA

    letters = get_grid_letter_paths(c_text, s=0.46, x0=44, y0=44)
    contours = get_filled_outline_contours(c_garden) if outline else get_stroked_contours(c_garden)
    suffix = " (Outlined Master)" if outline else ""

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-sym">
  <title id="title-sym">Trópikos Arquitetos — Símbolo 3×3{suffix}</title>
  <g id="symbol">
    {contours}
    {letters}
  </g>
</svg>'''
    return svg

# -----------------------------------------------------------------------------
# BUILD MASTER STACKED LOGO (256x256, Perfect Vertical Margins)
# -----------------------------------------------------------------------------
def build_stacked(color_mode="color", outline=False):
    if color_mode == "color":
        c_text, c_garden, c_desc = COLOR_INK, COLOR_PALM, COLOR_TERRA
    elif color_mode == "black":
        c_text, c_garden, c_desc = COLOR_BLACK, COLOR_BLACK, COLOR_BLACK
    elif color_mode == "white":
        c_text, c_garden, c_desc = COLOR_WHITE, COLOR_WHITE, COLOR_WHITE
    elif color_mode == "palm":
        c_text, c_garden, c_desc = COLOR_PALM, COLOR_PALM, COLOR_PALM
    elif color_mode == "terra":
        c_text, c_garden, c_desc = COLOR_TERRA, COLOR_TERRA, COLOR_TERRA

    # Calibrated vertical placement:
    # 3x3 grid placed at y0 = 24.
    # Height of 3x3 grid = 46*3 + 14*2 = 166. Bottom of grid = 190.
    # Gap = 18px.
    # Descr height = 20px (scale 0.20, cap-h 20).
    # Descr sits at y = 208..228.
    # Bottom margin = 256 - 228 = 28px.
    # Top margin = 24 - 4 (accent overshoot) = 20px.
    # Optical center: center of gravity sits precisely at y = 126 (slightly above 128)!
    s = 0.44
    gap = 14
    c_w = 46
    c_h = 46
    x0 = 45
    y0 = 24

    letters = get_grid_letter_paths(c_text, s=s, x0=x0, y0=y0, gap=gap, c_w=c_w, c_h=c_h)
    
    # Contour points adjusted for y0 = 24 (shifted up by 20px from 44)
    contours_shifted = []
    for p0, p1, p2, p3 in curve_definitions:
        sp0 = (p0[0] + 1, p0[1] - 20)
        sp1 = (p1[0] + 1, p1[1] - 20)
        sp2 = (p2[0] + 1, p2[1] - 20)
        sp3 = (p3[0] + 1, p3[1] - 20)
        if outline:
            d = offset_cubic(sp0, sp1, sp2, sp3, 1.9)
            contours_shifted.append(f'<path d="{d}" fill="{c_garden}"/>')
        else:
            d = f"M {sp0[0]} {sp0[1]} C {sp1[0]} {sp1[1]} {sp2[0]} {sp2[1]} {sp3[0]} {sp3[1]}"
            contours_shifted.append(f'<path d="{d}" fill="none" stroke="{c_garden}" stroke-width="3.8" stroke-linecap="round"/>')
    contour_str = "".join(contours_shifted)

    # Subtitle 'ARQUITETOS' underneath:
    w_d, p_d = typeset_paths("ARQUITETOS", scale=0.19, tracking=15, fill=c_desc)
    dx = x0 + (166 - w_d) / 2.0
    dy = y0 + 3 * (c_h + gap) + 12 # 24 + 180 + 12 = 216

    suffix = " (Outlined Master)" if outline else ""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-stk">
  <title id="title-stk">Trópikos Arquitetos — Logo Stacked{suffix}</title>
  <g id="symbol">
    {contour_str}
    {letters}
  </g>
  <g id="descriptor" transform="translate({round(dx, 2)}, {dy})">
    {''.join(p_d)}
  </g>
</svg>'''
    return svg

# -----------------------------------------------------------------------------
# BUILD MASTER HORIZONTAL LOCKUP (720x256, Perfect Margins & No Tiny Detail)
# -----------------------------------------------------------------------------
def build_horizontal(color_mode="color", outline=False):
    if color_mode == "color":
        c_text, c_garden, c_wm, c_desc, c_rule = COLOR_INK, COLOR_PALM, COLOR_INK, COLOR_TERRA, COLOR_INK
    elif color_mode == "black":
        c_text, c_garden, c_wm, c_desc, c_rule = COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, COLOR_BLACK, COLOR_BLACK
    elif color_mode == "white":
        c_text, c_garden, c_wm, c_desc, c_rule = COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE, COLOR_WHITE
    elif color_mode == "palm":
        c_text, c_garden, c_wm, c_desc, c_rule = COLOR_PALM, COLOR_PALM, COLOR_PALM, COLOR_PALM, COLOR_PALM
    elif color_mode == "terra":
        c_text, c_garden, c_wm, c_desc, c_rule = COLOR_TERRA, COLOR_TERRA, COLOR_TERRA, COLOR_TERRA, COLOR_TERRA

    # Symmetrical layout on 720 width:
    # Left margin: 100px. Content width: 520px. Right margin: 100px!
    ox_sym = 100
    oy_sym = 59
    x_rule = ox_sym + 152
    x_text = x_rule + 36

    # Wordmark and Descriptor:
    w_t, p_t = typeset_paths("TRÓPIKOS", scale=0.68, tracking=10, fill=c_wm)
    w_a, p_a = typeset_paths("ARQUITETOS", scale=0.25, tracking=24, fill=c_desc)

    # Symbol scaled inside lockup (scale = 0.54)
    # Inside symbol:
    letters = get_grid_letter_paths(c_text, s=0.46, x0=44, y0=44)
    contours = get_filled_outline_contours(c_garden) if outline else get_stroked_contours(c_garden)

    # Hairline divider:
    rule_el = (
        f'<rect x="{x_rule}" y="60" width="1.5" height="136" fill="{c_rule}"/>'
        if outline else
        f'<line x1="{x_rule}" y1="60" x2="{x_rule}" y2="196" stroke="{c_rule}" stroke-width="1.5"/>'
    )

    suffix = " (Outlined Master)" if outline else ""
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 256" width="720" height="256" role="img" aria-labelledby="title-horiz">
  <title id="title-horiz">Trópikos Arquitetos — Lockup Horizontal{suffix}</title>
  <g id="symbol" transform="translate({ox_sym}, {oy_sym}) scale(0.54)">
    {contours}
    {letters}
  </g>
  {rule_el}
  <g id="wordmark" transform="translate({x_text}, 84)">
    {''.join(p_t)}
  </g>
  <g id="descriptor" transform="translate({x_text+2}, 162)">
    {''.join(p_a)}
  </g>
</svg>'''
    return svg

# -----------------------------------------------------------------------------
# 5. ARCHITECTURAL TITLE BLOCK (Carimbo de Prancha ABNT / BIM / CAD)
# -----------------------------------------------------------------------------
def build_title_block():
    # Standard architectural title block (selo/carimbo de prancha)
    # Width: 180mm standard -> in SVG: 720 x 240
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 720 240" width="720" height="240" role="img" aria-labelledby="title-selo">
  <title id="title-selo">Trópikos Arquitetos — Carimbo de Prancha Técnico</title>
  <!-- Architectural Outer Border -->
  <rect x="0" y="0" width="720" height="240" fill="#FFFFFF" stroke="#191919" stroke-width="2"/>
  
  <!-- Vertical Division -->
  <line x1="240" y1="0" x2="240" y2="240" stroke="#191919" stroke-width="1.5"/>
  <line x1="520" y1="0" x2="520" y2="240" stroke="#191919" stroke-width="1.5"/>
  
  <!-- Left Column: Brand Identity -->
  <g transform="translate(42, 24) scale(0.62)">
    {build_stacked('color', outline=True)[build_stacked('color', outline=True).find('<g id="symbol">'):build_stacked('color', outline=True).rfind('</svg>')]}
  </g>
  <line x1="0" y1="200" x2="240" y2="200" stroke="#191919" stroke-width="1"/>
  <text x="120" y="222" font-family="'TWK Everett', 'Inter', sans-serif" font-size="10" font-weight="600" text-anchor="middle" fill="#191919" letter-spacing="1.5">CAU/PE: 104829-0 · RECIFE/PE</text>

  <!-- Middle Column: Project & Client Data -->
  <line x1="240" y1="48" x2="520" y2="48" stroke="#191919" stroke-width="1"/>
  <text x="252" y="24" font-family="'TWK Everett', 'Inter', sans-serif" font-size="8" fill="#6B6B6B" letter-spacing="1">PROJETO</text>
  <text x="252" y="40" font-family="'TWK Everett', 'Inter', sans-serif" font-size="13" font-weight="bold" fill="#191919">RESIDÊNCIA ALDEIA (CASA ALDEIA)</text>
  
  <line x1="240" y1="96" x2="520" y2="96" stroke="#191919" stroke-width="1"/>
  <text x="252" y="68" font-family="'TWK Everett', 'Inter', sans-serif" font-size="8" fill="#6B6B6B" letter-spacing="1">CONTEÚDO DA PRANCHA</text>
  <text x="252" y="86" font-family="'TWK Everett', 'Inter', sans-serif" font-size="12" font-weight="600" fill="#191919">IMPLANTAÇÃO, PLANTA BAIXA &amp; NÍVEIS</text>
  
  <line x1="240" y1="144" x2="520" y2="144" stroke="#191919" stroke-width="1"/>
  <text x="252" y="116" font-family="'TWK Everett', 'Inter', sans-serif" font-size="8" fill="#6B6B6B" letter-spacing="1">ENDEREÇO / LOCALIZAÇÃO</text>
  <text x="252" y="134" font-family="'TWK Everett', 'Inter', sans-serif" font-size="11" fill="#191919">ALDEIA DOS CAMARÁS — CAMARAGIBE / PE</text>
  
  <line x1="240" y1="192" x2="520" y2="192" stroke="#191919" stroke-width="1"/>
  <text x="252" y="164" font-family="'TWK Everett', 'Inter', sans-serif" font-size="8" fill="#6B6B6B" letter-spacing="1">AUTORIA &amp; COORDENAÇÃO</text>
  <text x="252" y="182" font-family="'TWK Everett', 'Inter', sans-serif" font-size="11" font-weight="600" fill="#191919">TRÓPIKOS ARQUITETOS · EQUIPE TÉCNICA</text>
  
  <text x="252" y="212" font-family="'TWK Everett', 'Inter', sans-serif" font-size="8" fill="#6B6B6B" letter-spacing="1">FASE</text>
  <text x="252" y="228" font-family="'TWK Everett', 'Inter', sans-serif" font-size="11" font-weight="bold" fill="#3D6E60">PROJETO EXECUTIVO (PE)</text>
  
  <line x1="380" y1="192" x2="380" y2="240" stroke="#191919" stroke-width="1"/>
  <text x="392" y="212" font-family="'TWK Everett', 'Inter', sans-serif" font-size="8" fill="#6B6B6B" letter-spacing="1">DATA</text>
  <text x="392" y="228" font-family="'JetBrains Mono', monospace" font-size="11" fill="#191919">OUT / 2026</text>

  <!-- Right Column: Numbering & Scale -->
  <line x1="520" y1="120" x2="720" y2="120" stroke="#191919" stroke-width="1"/>
  <text x="532" y="28" font-family="'TWK Everett', 'Inter', sans-serif" font-size="9" fill="#6B6B6B" letter-spacing="1">ESCALA</text>
  <text x="532" y="60" font-family="'JetBrains Mono', monospace" font-size="20" font-weight="bold" fill="#191919">1:50 · 1:100</text>
  <text x="532" y="90" font-family="'TWK Everett', 'Inter', sans-serif" font-size="9" fill="#6B6B6B" letter-spacing="1">REVISÃO: R02</text>
  
  <text x="532" y="148" font-family="'TWK Everett', 'Inter', sans-serif" font-size="9" fill="#6B6B6B" letter-spacing="1">PRANCHA Nº</text>
  <text x="620" y="210" font-family="'TWK Everett', 'Inter', sans-serif" font-size="64" font-weight="bold" text-anchor="middle" fill="#191919">01</text>
  <text x="690" y="210" font-family="'TWK Everett', 'Inter', sans-serif" font-size="14" fill="#6B6B6B">/ 12</text>
</svg>'''
    return svg

# -----------------------------------------------------------------------------
# EXECUTE GENERATION
# -----------------------------------------------------------------------------
base_dir = "/home/civo/tropikos/brand-kit"
svg_dir = os.path.join(base_dir, "svg")
cad_dir = os.path.join(base_dir, "architectural-cad")
os.makedirs(svg_dir, exist_ok=True)
os.makedirs(cad_dir, exist_ok=True)

# Generate masters
all_files = {
    # Stroked versions (ideal for SVG animations / web)
    "tropikos-symbol-color.svg": build_symbol("color", outline=False),
    "tropikos-symbol-black.svg": build_symbol("black", outline=False),
    "tropikos-symbol-white.svg": build_symbol("white", outline=False),
    "tropikos-symbol-palm.svg": build_symbol("palm", outline=False),
    "tropikos-symbol-terra.svg": build_symbol("terra", outline=False),

    "tropikos-stacked-color.svg": build_stacked("color", outline=False),
    "tropikos-stacked-black.svg": build_stacked("black", outline=False),
    "tropikos-stacked-white.svg": build_stacked("white", outline=False),
    "tropikos-stacked-palm.svg": build_stacked("palm", outline=False),

    "tropikos-horizontal-color.svg": build_horizontal("color", outline=False),
    "tropikos-horizontal-black.svg": build_horizontal("black", outline=False),
    "tropikos-horizontal-white.svg": build_horizontal("white", outline=False),
    "tropikos-horizontal-palm.svg": build_horizontal("palm", outline=False),

    # Pure Outlined masters (100% fill, zero stroke, laser-cut / CNC / print production ready)
    "tropikos-symbol-outline.svg": build_symbol("color", outline=True),
    "tropikos-symbol-black-outline.svg": build_symbol("black", outline=True),
    "tropikos-stacked-outline.svg": build_stacked("color", outline=True),
    "tropikos-stacked-black-outline.svg": build_stacked("black", outline=True),
    "tropikos-horizontal-outline.svg": build_horizontal("color", outline=True),
    "tropikos-horizontal-black-outline.svg": build_horizontal("black", outline=True),
}

for name, content in all_files.items():
    with open(os.path.join(svg_dir, name), "w") as f:
        f.write(content)
    print(f"Generated: {name}")

# Write carimbo de prancha
with open(os.path.join(cad_dir, "tropikos-carimbo-prancha.svg"), "w") as f:
    f.write(build_title_block())
print("Generated architectural title block in architectural-cad/")

print("Masterpiece generation completed.")
