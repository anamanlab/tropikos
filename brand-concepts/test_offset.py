import math

def offset_cubic(p0, p1, p2, p3, d):
    # Samples the cubic bezier at N points, computes normal vectors,
    # and constructs the parallel left and right outlines with rounded caps.
    N = 24
    left = []
    right = []
    
    for i in range(N + 1):
        t = i / N
        # Bernstein polynomials
        b0 = (1 - t)**3
        b1 = 3 * (1 - t)**2 * t
        b2 = 3 * (1 - t) * t**2
        b3 = t**3
        
        x = b0*p0[0] + b1*p1[0] + b2*p2[0] + b3*p3[0]
        y = b0*p0[1] + b1*p1[1] + b2*p2[1] + b3*p3[1]
        
        # Derivative
        dx = 3*(1-t)**2*(p1[0]-p0[0]) + 6*(1-t)*t*(p2[0]-p1[0]) + 3*t**2*(p3[0]-p2[0])
        dy = 3*(1-t)**2*(p1[1]-p0[1]) + 6*(1-t)*t*(p2[1]-p1[1]) + 3*t**2*(p3[1]-p2[1])
        
        length = math.hypot(dx, dy)
        if length == 0:
            nx, ny = 0, 1
        else:
            # Normal vector (-dy, dx) normalized
            nx = -dy / length
            ny = dx / length
            
        left.append((x + nx * d, y + ny * d))
        right.append((x - nx * d, y - ny * d))
        
    # Build path: left forward, semicircle cap at end, right backwards, semicircle cap at start
    # End cap: from left[-1] to right[-1]
    # Arc command: A r r 0 0 1 right[-1]
    d_path = [f"M {left[0][0]:.2f} {left[0][1]:.2f}"]
    for pt in left[1:]:
        d_path.append(f"L {pt[0]:.2f} {pt[1]:.2f}")
    # Arc at end:
    d_path.append(f"A {d:.2f} {d:.2f} 0 0 1 {right[-1][0]:.2f} {right[-1][1]:.2f}")
    for pt in reversed(right[:-1]):
        d_path.append(f"L {pt[0]:.2f} {pt[1]:.2f}")
    # Arc at start:
    d_path.append(f"A {d:.2f} {d:.2f} 0 0 1 {left[0][0]:.2f} {left[0][1]:.2f} Z")
    
    return " ".join(d_path)

# Test with curve 1
p0 = (47, 146)
p1 = (59, 138)
p2 = (69, 150)
p3 = (87, 144)
path_d = offset_cubic(p0, p1, p2, p3, 1.9)
print("Generated outline path:", path_d[:120], "...")
