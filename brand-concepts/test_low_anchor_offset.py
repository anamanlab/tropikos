import math
from generate_letters import build_glyphs

def offset_cubic_smooth(p0, p1, p2, p3, d, N=6):
    left = []
    right = []
    for i in range(N + 1):
        t = i / N
        b0 = (1 - t)**3
        b1 = 3 * (1 - t)**2 * t
        b2 = 3 * (1 - t) * t**2
        b3 = t**3
        x = b0*p0[0] + b1*p1[0] + b2*p2[0] + b3*p3[0]
        y = b0*p0[1] + b1*p1[1] + b2*p2[1] + b3*p3[1]
        dx = 3*(1-t)**2*(p1[0]-p0[0]) + 6*(1-t)*t*(p2[0]-p1[0]) + 3*t**2*(p3[0]-p2[0])
        dy = 3*(1-t)**2*(p1[1]-p0[1]) + 6*(1-t)*t*(p2[1]-p1[1]) + 3*t**2*(p3[1]-p2[1])
        length = math.hypot(dx, dy)
        nx, ny = (-dy/length, dx/length) if length > 0 else (0, 1)
        left.append((x + nx*d, y + ny*d))
        right.append((x - nx*d, y - ny*d))
    
    d_path = [f"M {left[0][0]:.1f} {left[0][1]:.1f}"]
    for pt in left[1:]:
        d_path.append(f"L {pt[0]:.1f} {pt[1]:.1f}")
    d_path.append(f"A {d:.1f} {d:.1f} 0 0 1 {right[-1][0]:.1f} {right[-1][1]:.1f}")
    for pt in reversed(right[:-1]):
        d_path.append(f"L {pt[0]:.1f} {pt[1]:.1f}")
    d_path.append(f"A {d:.1f} {d:.1f} 0 0 1 {left[0][0]:.1f} {left[0][1]:.1f} Z")
    return " ".join(d_path)

p0, p1, p2, p3 = (47.0, 143.0), (59.0, 135.0), (69.0, 147.0), (87.0, 141.0)
res = offset_cubic_smooth(p0, p1, p2, p3, 1.9, N=6)
print("Anchor count per curve with N=6:", res.count("L") + 2)
