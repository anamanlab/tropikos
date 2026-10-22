with open("/home/civo/tropikos/brand-kit/svg/tropikos-stacked-color.svg") as f:
    stk_svg = f.read()

inner_stk = stk_svg[stk_svg.find('<g id="symbol">'):stk_svg.rfind('</svg>')].strip()

with open("/home/civo/tropikos/brand-kit/architectural-cad/tropikos-carimbo-prancha.svg") as f:
    carimbo = f.read()

# Replace the inner logo in the carimbo
start_tag = "<!-- Left Column: Brand Identity -->"
end_tag = "<line x1=\"0\" y1=\"200\""

new_left_col = f'''{start_tag}
  <g id="carimbo-brand" transform="translate(42, 16) scale(0.68)">
    {inner_stk}
  </g>
  '''

p1 = carimbo[:carimbo.find(start_tag)]
p2 = carimbo[carimbo.find(end_tag):]

updated_carimbo = p1 + new_left_col + p2
with open("/home/civo/tropikos/brand-kit/architectural-cad/tropikos-carimbo-prancha.svg", "w") as f:
    f.write(updated_carimbo)

import cairosvg
cairosvg.svg2png(url="/home/civo/tropikos/brand-kit/architectural-cad/tropikos-carimbo-prancha.svg",
                 write_to="/home/civo/tropikos/brand-kit/png/tropikos-carimbo-prancha.png",
                 output_width=1440)
print("Updated carimbo with polished logo.")
