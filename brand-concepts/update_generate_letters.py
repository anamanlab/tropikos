with open("/home/civo/tropikos/brand-concepts/generate_letters.py") as f:
    code = f.read()

# Replace Q in generate_letters.py
old_q = """    # Q: width 76
    glyphs['Q'] = {
        'w': 76,
        'd': glyphs['O']['d'] + f" M 46 72 L 66 72 L 76 96 L 62 102 Z",
        'rule': 'evenodd'
    }"""

new_q = """    # Q: width 76 (seamless united outer contour and tail)
    glyphs['Q'] = {
        'w': 76,
        'd': (
            "M 38 0 C 59 0 76 17 76 50 C 76 66 69 80 58 89 "
            "L 72 104 H 54 L 46 95 "
            "C 43 97 41 98 38 98 C 17 98 0 81 0 50 C 0 17 17 0 38 0 Z "
            "M 38 16 C 26 16 16 29 16 50 C 16 71 26 82 38 82 C 50 82 60 71 60 50 C 60 29 50 16 38 16 Z"
        ),
        'rule': 'evenodd'
    }"""

code = code.replace(old_q, new_q)
with open("/home/civo/tropikos/brand-concepts/generate_letters.py", "w") as f:
    f.write(code)

print("Updated generate_letters.py with seamless Q")
