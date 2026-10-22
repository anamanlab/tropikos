import cairosvg

# In evenodd:
# outer oval: y=0..100
# inner hole: y=16..84
# tail: starts at y=80 outside inner hole, so if tail is from y=84..104, x=50..66, it does not overlap the inner hole!
q_d = (
    "M 38 0 C 59 0 76 17 76 50 C 76 83 59 100 38 100 C 17 100 0 83 0 50 C 0 17 17 0 38 0 Z "
    "M 38 16 C 26 16 16 29 16 50 C 16 71 26 84 38 84 C 50 84 60 71 60 50 C 60 29 50 16 38 16 Z "
    "M 50 84 L 66 84 L 74 104 L 58 104 Z"
)
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" width="100" height="120"><path d="{q_d}" fill-rule="evenodd" fill="#191919"/></svg>'
cairosvg.svg2png(bytestring=svg.encode('utf-8'), write_to="/home/civo/tropikos/brand-concepts/test_q_fixed.png")
print("Rendered test_q_fixed.png")
