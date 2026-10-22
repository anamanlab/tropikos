import math

def build_glyphs():
    # cap_h = 100, sw = 16
    H = 100
    SW = 16
    glyphs = {}

    # T: width 66
    glyphs['T'] = {
        'w': 66,
        'd': f"M 0 0 H 66 V {SW} H {33 + SW//2} V {H} H {33 - SW//2} V {SW} H 0 Z"
    }

    # I: width 16
    glyphs['I'] = {
        'w': SW,
        'd': f"M 0 0 H {SW} V {H} H 0 Z"
    }

    # E: width 60
    glyphs['E'] = {
        'w': 60,
        'd': f"M 0 0 H 60 V {SW} H {SW} V 42 H 54 V 58 H {SW} V {H-SW} H 60 V {H} H 0 Z"
    }

    # P: width 68
    # stem 0..SW, bowl outer to x=68, y=56; inner counter 18..50, 16..40
    # outer bowl: right arc r=28
    glyphs['P'] = {
        'w': 68,
        'd': (
            f"M 0 0 H 40 C 55.5 0 68 12.5 68 28 C 68 43.5 55.5 56 40 56 H {SW} V {H} H 0 Z "
            f"M {SW} {SW} H 40 C 46.6 {SW} 52 21.4 52 28 C 52 34.6 46.6 40 40 40 H {SW} Z"
        ),
        'rule': 'evenodd'
    }

    # R: width 70
    # P bowl + diagonal leg
    glyphs['R'] = {
        'w': 70,
        'd': (
            f"M 0 0 H 42 C 57.5 0 70 12.5 70 28 C 70 41.5 60.5 52.5 48 55.2 L 70 {H} H 50 L 30 56 H {SW} V {H} H 0 Z "
            f"M {SW} {SW} H 42 C 48.6 {SW} 54 21.4 54 28 C 54 34.6 48.6 40 42 40 H {SW} Z"
        ),
        'rule': 'evenodd'
    }

    # O: width 76
    glyphs['O'] = {
        'w': 76,
        'd': (
            f"M 38 0 C 59 0 76 17 76 50 C 76 83 59 100 38 100 C 17 100 0 83 0 50 C 0 17 17 0 38 0 Z "
            f"M 38 {SW} C 26 {SW} {SW} 29 {SW} 50 C {SW} 71 26 84 38 84 C 50 84 {76-SW} 71 {76-SW} 50 C {76-SW} 29 50 {SW} 38 {SW} Z"
        ),
        'rule': 'evenodd'
    }

    # Ó: width 76 with acute accent
    glyphs['Ó'] = {
        'w': 76,
        'd': glyphs['O']['d'] + f" M 40 -8 L 56 -24 L 66 -16 L 50 0 Z",
        'rule': 'evenodd'
    }

    # K: width 68
    glyphs['K'] = {
        'w': 68,
        'd': (
            f"M 0 0 H {SW} V 45 L 48 0 H 68 L 30 52 L 68 {H} H 46 L {SW} 60 V {H} H 0 Z"
        )
    }

    # S: width 66
    glyphs['S'] = {
        'w': 66,
        'd': (
            "M 58 24 L 46 29 C 43 20 37 16 33 16 C 25 16 20 21 20 27 C 20 34 26 37 38 42 "
            "C 54 48 64 54 64 68 C 64 86 49 100 33 100 C 15 100 4 87 2 72 L 17 68 "
            "C 19 79 26 84 33 84 C 42 84 48 78 48 70 C 48 61 41 58 29 52 "
            "C 16 46 4 40 4 27 C 4 12 17 0 33 0 C 48 0 56 10 58 24 Z"
        )
    }

    # A: width 74
    glyphs['A'] = {
        'w': 74,
        'd': (
            f"M 37 0 L 74 {H} H 55 L 47 76 H 27 L 19 {H} H 0 Z "
            f"M 37 26 L 43 62 H 31 Z"
        ),
        'rule': 'evenodd'
    }

    # Q: width 76 (seamless united outer contour and tail)
    glyphs['Q'] = {
        'w': 76,
        'd': (
            "M 38 0 C 59 0 76 17 76 50 C 76 66 69 80 58 89 "
            "L 72 104 H 54 L 46 95 "
            "C 43 97 41 98 38 98 C 17 98 0 81 0 50 C 0 17 17 0 38 0 Z "
            "M 38 16 C 26 16 16 29 16 50 C 16 71 26 82 38 82 C 50 82 60 71 60 50 C 60 29 50 16 38 16 Z"
        ),
        'rule': 'evenodd'
    }

    # U: width 72
    glyphs['U'] = {
        'w': 72,
        'd': (
            f"M 0 0 H {SW} V 62 C {SW} 76 25 84 36 84 C 47 84 56 76 56 62 V 0 H 72 V 62 "
            f"C 72 86 56 100 36 100 C 16 100 0 86 0 62 Z"
        )
    }

    return glyphs

glyphs = build_glyphs()
print("Built glyphs:", list(glyphs.keys()))
