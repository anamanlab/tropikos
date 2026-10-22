import cairosvg

# Test Q with nonzero rule:
q_d = (
    "M 38 0 C 59 0 76 17 76 50 C 76 83 59 100 38 100 C 17 100 0 83 0 50 C 0 17 17 0 38 0 Z "
    "M 38 16 C 50 16 60 29 60 50 C 60 71 50 84 38 84 C 26 84 16 71 16 50 C 16 29 26 16 38 16 Z "
    "M 48 74 L 66 74 L 76 98 L 58 102 Z"
)
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" width="100" height="120"><path d="{q_d}" fill="#191919"/></svg>'
cairosvg.svg2png(bytestring=svg.encode('utf-8'), write_to="/home/civo/tropikos/brand-concepts/test_q.png")
print("Rendered test_q.png")
