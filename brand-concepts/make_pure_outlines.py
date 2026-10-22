import math
from test_offset import offset_cubic
from generate_letters import build_glyphs

glyphs = build_glyphs()

# Let's define the 4 curves mathematically:
# Each curve is given by 4 control points:
# gx = 44, gy = 108
curves_pts = [
    ((47, 146), (59, 138), (69, 150), (87, 144)),
    ((47, 135), (59, 127), (70, 139), (87, 133)),
    ((47, 124), (60, 116), (72, 128), (87, 122)),
    ((51, 114), (62, 109), (74, 117), (87, 111)),
]

stroke_radius = 1.9 # width 3.8 / 2

outline_paths = []
for p0, p1, p2, p3 in curves_pts:
    d = offset_cubic(p0, p1, p2, p3, stroke_radius)
    outline_paths.append(f'<path d="{d}" fill="#3D6E60"/>')

print("Created 4 filled outline paths.")
