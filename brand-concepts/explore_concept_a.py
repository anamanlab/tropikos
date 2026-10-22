import os
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

# Let's explore 3 subtle refinements of Concept A:
# A1: The Pátio Courtyard (Pure Black / Onyx)
# A2: The Brand Colors (Onyx letters, Tropical Palm #3D6E60 contour curves, Terracotta #BA5424 'arquitetos')
# A3: Complete Stacked Emblem with 'ARQUITETOS' underneath

# Let's write generator functions
def make_a_stacked(color_mode="mono"):
    # color_mode: "mono", "color", "inverted"
    if color_mode == "mono":
        c_text = "#191919"
        c_garden = "#191919"
        c_desc = "#191919"
    elif color_mode == "color":
        c_text = "#191919"
        c_garden = "#3D6E60" # Palm / Sage
        c_desc = "#BA5424"   # Terracotta
    elif color_mode == "inverted":
        c_text = "#FFFFFF"
        c_garden = "#649B8D"
        c_desc = "#D97746"
        
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
    
    # Subtitle 'ARQUITETOS' underneath:
    # Width of the 3x3 block: x0 to x0 + 2*(46+14) + 46 = 45 + 120 + 46 = 211 (width = 166)
    # Typeset 'ARQUITETOS' to span width ~166
    w_d, p_d = typeset_paths("ARQUITETOS", scale=0.18, tracking=15, fill=c_desc)
    # center under block: (166 - w_d)/2
    dx = x0 + (166 - w_d)/2
    dy = y0 + 3 * (c_h + gap) + 12 # 32 + 3*60 + 12 = 224
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title">
  <title id="title">Trópikos Arquitetos</title>
  <g id="symbol">
    {contour_paths}
    {''.join(paths)}
  </g>
  <g id="descriptor" transform="translate({round(dx, 2)}, {dy})">
    {''.join(p_d)}
  </g>
</svg>'''
    return svg

os.makedirs("/home/civo/tropikos/brand-concepts/refinements", exist_ok=True)

with open("/home/civo/tropikos/brand-concepts/refinements/tropikos-stacked-mono.svg", "w") as f:
    f.write(make_a_stacked("mono"))

with open("/home/civo/tropikos/brand-concepts/refinements/tropikos-stacked-color.svg", "w") as f:
    f.write(make_a_stacked("color"))

cairosvg.svg2png(url="/home/civo/tropikos/brand-concepts/refinements/tropikos-stacked-mono.svg",
                 write_to="/home/civo/tropikos/brand-concepts/refinements/tropikos-stacked-mono.png",
                 output_width=512, output_height=512)

cairosvg.svg2png(url="/home/civo/tropikos/brand-concepts/refinements/tropikos-stacked-color.svg",
                 write_to="/home/civo/tropikos/brand-concepts/refinements/tropikos-stacked-color.png",
                 output_width=512, output_height=512)

print("Exploration rendered successfully.")
