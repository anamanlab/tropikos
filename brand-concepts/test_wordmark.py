import re
import cairosvg
from generate_letters import build_glyphs

glyphs = build_glyphs()

def typeset_path(text, scale=1.0, tracking=10):
    # Returns (total_width, merged_path_d)
    x = 0
    paths = []
    
    # Simple kerning pairs for architectural type
    kerning = {
        ('T', 'R'): -4,
        ('R', 'Ó'): -2,
        ('P', 'I'): 2,
        ('K', 'O'): -2,
        ('A', 'R'): -2,
    }
    
    for i, ch in enumerate(text):
        if ch not in glyphs:
            x += 20 * scale
            continue
        g = glyphs[ch]
        d = g['d']
        
        # Apply kerning
        if i > 0:
            pair = (text[i-1], ch)
            if pair in kerning:
                x += kerning[pair] * scale
                
        # Transform d by scale and x offset
        # Replace numbers in d
        # SVG path command regex
        # Instead of parsing, we can place inside <path transform="translate(x, y) scale(scale)" d="..." />
        paths.append(f'<path d="{d}" transform="translate({round(x, 2)}, 0) scale({scale})"/>')
        x += (g['w'] + tracking) * scale
        
    return x - (tracking * scale), paths

w, p = typeset_path("TRÓPIKOS", scale=0.8, tracking=12)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {round(w + 40)} 120" width="{round(w + 40)}" height="120">
  <g fill="#191919" fill-rule="evenodd" transform="translate(20, 25)">
    {''.join(p)}
  </g>
</svg>'''

with open("/home/civo/tropikos/brand-concepts/test_wordmark.svg", "w") as f:
    f.write(svg)

cairosvg.svg2png(url="/home/civo/tropikos/brand-concepts/test_wordmark.svg",
                 write_to="/home/civo/tropikos/brand-concepts/test_wordmark.png")
print(f"Wordmark generated: width {w}, PNG written.")
