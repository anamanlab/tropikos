import re

with open("/home/civo/tropikos/brand-concepts/polish_all_masters.py") as f:
    code = f.read()

# Fix glyph A counter height:
# Originally: M 37 26 L 43 62 H 31 Z -> height was 36 (62-26)
# Let's make it M 37 22 L 45 66 H 29 Z -> height 44 (44 * 0.25 = 11 > 8!)
code = code.replace("M 37 26 L 43 62 H 31 Z", "M 37 20 L 45 66 H 29 Z")

# In horizontal lockup, shift ox_sym from 78 to 41:
code = code.replace("ox_sym = 78", "ox_sym = 41")

# Make accent on Ó even bolder in horizontal lockup so it is > 8.5px:
code = code.replace("bold_ó_d = glyphs['O']['d'] + \" M 38 -12 L 60 -30 L 70 -20 L 48 -2 Z\"",
                    "bold_ó_d = glyphs['O']['d'] + \" M 36 -14 L 62 -34 L 74 -22 L 48 -2 Z\"")

with open("/home/civo/tropikos/brand-concepts/polish_all_masters.py", "w") as f:
    f.write(code)

