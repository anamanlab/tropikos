import cairosvg

# Outer ring with integrated tail (single seamless contour):
# outer circle top (38, 0) clockwise down right (76, 50) down to (66, 88)
# then diagonal tail to (76, 104) H 58 L 50 98
# and continues up left to (0, 50) and back to (38, 0)
outer_with_tail = (
    "M 38 0 C 59 0 76 17 76 50 C 76 66 69 80 58 89 "
    "L 72 104 H 54 L 46 95 "
    "C 43 97 41 98 38 98 C 17 98 0 81 0 50 C 0 17 17 0 38 0 Z"
)
inner_hole = (
    "M 38 16 C 26 16 16 29 16 50 C 16 71 26 82 38 82 C 50 82 60 71 60 50 C 60 29 50 16 38 16 Z"
)
q_clean = outer_with_tail + " " + inner_hole

svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 120" width="100" height="120"><path d="{q_clean}" fill-rule="evenodd" fill="#191919"/></svg>'
cairosvg.svg2png(bytestring=svg.encode('utf-8'), write_to="/home/civo/tropikos/brand-concepts/test_q_union.png")
print("Rendered test_q_union.png")
