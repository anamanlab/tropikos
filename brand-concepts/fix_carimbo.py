import cairosvg

# Re-read and fix carimbo layout
with open("/home/civo/tropikos/brand-kit/architectural-cad/tropikos-carimbo-prancha.svg") as f:
    text = f.read()

# Fix the division line at 400 instead of 380, and adjust labels
text = text.replace('<line x1="380" y1="192" x2="380" y2="240" stroke="#191919" stroke-width="1"/>',
                    '<line x1="410" y1="192" x2="410" y2="240" stroke="#191919" stroke-width="1"/>')
text = text.replace('<text x="392" y="212"', '<text x="422" y="212"')
text = text.replace('<text x="392" y="228"', '<text x="422" y="228"')
text = text.replace('PROJETO EXECUTIVO (PE)', 'PROJETO EXECUTIVO')

with open("/home/civo/tropikos/brand-kit/architectural-cad/tropikos-carimbo-prancha.svg", "w") as f:
    f.write(text)

cairosvg.svg2png(url="/home/civo/tropikos/brand-kit/architectural-cad/tropikos-carimbo-prancha.svg",
                 write_to="/home/civo/tropikos/brand-kit/png/tropikos-carimbo-prancha.png",
                 output_width=1440)

cairosvg.svg2png(url="/home/civo/tropikos/brand-kit/svg/tropikos-horizontal-color.svg",
                 write_to="/home/civo/tropikos/brand-kit/png/tropikos-horizontal-color.png",
                 output_width=1440)

cairosvg.svg2png(url="/home/civo/tropikos/brand-kit/svg/tropikos-stacked-color.svg",
                 write_to="/home/civo/tropikos/brand-kit/png/tropikos-stacked-color.png",
                 output_width=1024)

print("Re-rendered carimbo and horizontal PNGs.")
