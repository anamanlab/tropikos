import os
import cairosvg
from pypdf import PdfWriter

W = 842
H = 595

out_dir = "/home/civo/tropikos/brand-kit"
pdf_pages_dir = os.path.join(out_dir, "pdf-pages-v2")
pdf_renders_dir = os.path.join(out_dir, "pdf-renders-v2")
os.makedirs(pdf_pages_dir, exist_ok=True)
os.makedirs(pdf_renders_dir, exist_ok=True)

# Read SVGs
with open("/home/civo/tropikos/brand-kit/svg/tropikos-stacked-color.svg") as f:
    stk_color = f.read()
inner_stk_color = stk_color[stk_color.find('<g id="symbol">'):stk_color.rfind('</svg>')].strip()

with open("/home/civo/tropikos/brand-kit/svg/tropikos-stacked-white.svg") as f:
    stk_white = f.read()
inner_stk_white = stk_white[stk_white.find('<g id="symbol">'):stk_white.rfind('</svg>')].strip()

with open("/home/civo/tropikos/brand-kit/svg/tropikos-horizontal-color.svg") as f:
    horiz_color = f.read()
inner_horiz_color = horiz_color[horiz_color.find('<g id="symbol"'):horiz_color.rfind('</svg>')].strip()

with open("/home/civo/tropikos/brand-kit/architectural-cad/tropikos-carimbo-prancha.svg") as f:
    carimbo_svg = f.read()
inner_carimbo = carimbo_svg[carimbo_svg.find('<!-- Architectural Outer Border -->'):carimbo_svg.rfind('</svg>')].strip()

with open("/home/civo/tropikos/brand-kit/web/tropikos-symbol-app-icon.svg") as f:
    app_icon_svg = f.read()
inner_app_icon = app_icon_svg[app_icon_svg.find('<g id="symbol"'):app_icon_svg.rfind('</svg>')].strip()

font_sans = "'TWK Everett', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
font_mono = "'TWK Everett Mono', 'JetBrains Mono', monospace"

def header_footer(page_num, title):
    return f'''
    <!-- Top Hairline Rule -->
    <line x1="48" y1="44" x2="794" y2="44" stroke="#191919" stroke-width="0.5"/>
    <text x="48" y="34" font-family="{font_sans}" font-size="8.5" font-weight="700" fill="#191919" letter-spacing="2">TRÓPIKOS ARQUITETOS</text>
    <text x="794" y="34" font-family="{font_sans}" font-size="8.5" font-weight="600" text-anchor="end" fill="#6B6B6B" letter-spacing="1.5">{title}</text>
    
    <!-- Bottom Hairline Rule -->
    <line x1="48" y1="550" x2="794" y2="550" stroke="#191919" stroke-width="0.5"/>
    <text x="48" y="568" font-family="{font_mono}" font-size="8" fill="#6B6B6B" letter-spacing="0.5">RECIFE · PE · 08°03′S 34°52′W · ARQUITETURA AUTORAL</text>
    <text x="794" y="568" font-family="{font_mono}" font-size="8.5" font-weight="600" text-anchor="end" fill="#191919">{page_num:02d} / 07</text>
    '''

# -----------------------------------------------------------------------------
# PAGE 1: COVER
# -----------------------------------------------------------------------------
p1_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#FAFAF9"/>
  <!-- Inner Architectural Frame -->
  <rect x="36" y="36" width="{W-72}" height="{H-72}" fill="#FFFFFF" stroke="#191919" stroke-width="0.8"/>
  
  <!-- Header meta -->
  <text x="56" y="66" font-family="{font_sans}" font-size="9" font-weight="700" fill="#191919" letter-spacing="2.5">TRÓPIKOS ARQUITETOS</text>
  <text x="786" y="66" font-family="{font_mono}" font-size="8.5" text-anchor="end" fill="#6B6B6B">DOC. REF: BK-2026-PE</text>
  <line x1="56" y1="78" x2="786" y2="78" stroke="#191919" stroke-width="0.5"/>

  <!-- Plinth with Master Stacked Logo -->
  <g transform="translate(306, 120) scale(0.90)">
    {inner_stk_color}
  </g>

  <!-- Bottom Title Block with strict separation -->
  <line x1="56" y1="440" x2="786" y2="440" stroke="#191919" stroke-width="0.8"/>
  
  <text x="56" y="476" font-family="{font_sans}" font-size="22" font-weight="700" fill="#191919" letter-spacing="-0.5">MANUAL DE IDENTIDADE VISUAL</text>
  <text x="56" y="500" font-family="{font_sans}" font-size="10.5" fill="#6B6B6B" letter-spacing="0.5">Brand Kit de Produção · Sistema Vetorial, Aplicações Executivas &amp; Web</text>

  <!-- Vertical divider -->
  <line x1="600" y1="452" x2="600" y2="512" stroke="#191919" stroke-width="0.5"/>

  <text x="618" y="472" font-family="{font_sans}" font-size="9" font-weight="700" fill="#191919" letter-spacing="1">EDIÇÃO EXECUTIVA</text>
  <text x="618" y="490" font-family="{font_mono}" font-size="8.5" fill="#3D6E60">OUTUBRO / 2026</text>
  <text x="618" y="506" font-family="{font_mono}" font-size="8.5" fill="#6B6B6B">ESPINHEIRO · RECIFE</text>
</svg>'''

# -----------------------------------------------------------------------------
# PAGE 2: CONCEITO & ANATOMIA DO GRID
# -----------------------------------------------------------------------------
# In the diagram:
# Let's align the dashed boxes exactly with inner_stk_color:
# inner_stk_color has y0 = 24, x0 = 45, c_w = 46, c_h = 46, gap = 14!
# Let's draw the 9 dashed boxes at exactly those coordinates:
p2_boxes = []
for r in range(3):
    for c in range(3):
        bx = 45 + c * (46 + 14)
        by = 24 + r * (46 + 14)
        if c == 0 and r == 1:
            # Garden cell
            p2_boxes.append(f'<rect x="{bx}" y="{by}" width="46" height="46" fill="#EAF2EF" stroke="#3D6E60" stroke-width="1.2"/>')
        else:
            p2_boxes.append(f'<rect x="{bx}" y="{by}" width="46" height="46" fill="none" stroke="#6B6B6B" stroke-dasharray="2 2" stroke-width="0.6"/>')

p2_boxes_svg = "".join(p2_boxes)

p2_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#FFFFFF"/>
  {header_footer(2, "01 · CONCEITO &amp; ANATOMIA DO GRID")}

  <!-- Left Column: Narrative -->
  <text x="48" y="86" font-family="{font_sans}" font-size="16" font-weight="700" fill="#191919">A Síntese entre Rigor e Clima</text>
  <text x="48" y="112" font-family="{font_sans}" font-size="10.5" fill="#191919" width="330">
    <tspan x="48" dy="0">A identidade da Trópikos Arquitetos parte da tensão produtiva</tspan>
    <tspan x="48" dy="16">entre o rigor da arquitetura moderna e a organicidade do relevo,</tspan>
    <tspan x="48" dy="16">da luz e dos ventos do litoral pernambucano.</tspan>
  </text>

  <text x="48" y="185" font-family="{font_sans}" font-size="12" font-weight="700" fill="#191919">A Métrica Silábica 3×3 (TRÓ · PI · KOS)</text>
  <text x="48" y="207" font-family="{font_sans}" font-size="9.5" fill="#6B6B6B">
    <tspan x="48" dy="0">A distribuição das 8 letras respeita rigorosamente a métrica</tspan>
    <tspan x="48" dy="15">fonética da marca. Cada linha de letras atua como uma laje de</tspan>
    <tspan x="48" dy="15">concreto aparente, com proporções neo-grotescas robustas.</tspan>
  </text>

  <text x="48" y="275" font-family="{font_sans}" font-size="12" font-weight="700" fill="#3D6E60">O Pátio Topográfico Interno (9ª Célula)</text>
  <text x="48" y="297" font-family="{font_sans}" font-size="9.5" fill="#6B6B6B">
    <tspan x="48" dy="0">No modernismo brasileiro, o vazio nunca é ausência: é o pátio</tspan>
    <tspan x="48" dy="15">interno, o recanto vegetal ventilado que permite à luz e à brisa</tspan>
    <tspan x="48" dy="15">atravessarem o volume edificado. As 4 curvas desenham o relevo</tspan>
    <tspan x="48" dy="15">e a drenagem natural da paisagem litorânea do Recife.</tspan>
  </text>

  <text x="48" y="380" font-family="{font_sans}" font-size="12" font-weight="700" fill="#BA5424">O Descritor 'ARQUITETOS'</text>
  <text x="48" y="402" font-family="{font_sans}" font-size="9.5" fill="#6B6B6B">
    <tspan x="48" dy="0">Ancorado na base da composição em tom terracota terroso,</tspan>
    <tspan x="48" dy="15">com tracking aberto (15 unidades), assegurando estabilidade</tspan>
    <tspan x="48" dy="15">e clareza de categoria profissional ao estúdio.</tspan>
  </text>

  <!-- Right Column: Diagram Board -->
  <rect x="420" y="74" width="374" height="446" fill="#FBFBFB" stroke="#191919" stroke-width="0.8"/>
  <text x="440" y="102" font-family="{font_sans}" font-size="10.5" font-weight="700" fill="#191919" letter-spacing="1">MALHA GEOMÉTRICA &amp; NORMAS DO GRID</text>
  
  <g transform="translate(480, 130) scale(1.0)">
    {p2_boxes_svg}
    {inner_stk_color}
  </g>

  <!-- Technical specs below diagram -->
  <line x1="440" y1="435" x2="774" y2="435" stroke="#191919" stroke-width="0.5"/>
  <text x="440" y="455" font-family="{font_mono}" font-size="8.5" fill="#191919">DIMENSÃO DA CÉLULA: 46×46 px · GAP: 14 px</text>
  <text x="440" y="472" font-family="{font_mono}" font-size="8.5" fill="#3D6E60">PÁTIO VEGETAL: 4 ISOLINHAS CÚBICAS DE 3.8 px</text>
  <text x="440" y="489" font-family="{font_mono}" font-size="8.5" fill="#BA5424">DESCRITOR: CAP-HEIGHT 19 px · COR BARRO COZIDO</text>
</svg>'''

# -----------------------------------------------------------------------------
# PAGE 3: SISTEMA DE LOGOTIPOS
# -----------------------------------------------------------------------------
p3_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#FFFFFF"/>
  {header_footer(3, "02 · SISTEMA DE LOGOTIPOS")}

  <!-- 1. Horizontal Lockup Card -->
  <rect x="48" y="70" width="746" height="154" fill="#FFFFFF" stroke="#191919" stroke-width="0.8"/>
  <text x="68" y="92" font-family="{font_sans}" font-size="8.5" font-weight="700" fill="#6B6B6B" letter-spacing="1.5">02.1 · VERSÃO HORIZONTAL (CABEÇALHOS DIGITAIS, PAPELARIA &amp; ASSINATURAS)</text>
  
  <g transform="translate(203, 84) scale(0.64)">
    {inner_horiz_color}
  </g>

  <!-- 2. Master Stacked on Light -->
  <rect x="48" y="244" width="360" height="276" fill="#FFFFFF" stroke="#191919" stroke-width="0.8"/>
  <text x="68" y="268" font-family="{font_sans}" font-size="8.5" font-weight="700" fill="#6B6B6B" letter-spacing="1.5">02.2 · MASTER STACKED (CAPAS &amp; PRANCHAS)</text>
  <g transform="translate(133, 298) scale(0.74)">
    {inner_stk_color}
  </g>

  <!-- 3. Inverted Master on Onyx Dark Surface -->
  <rect x="434" y="244" width="360" height="276" fill="#191919"/>
  <text x="454" y="268" font-family="{font_sans}" font-size="8.5" font-weight="700" fill="#FFFFFF" letter-spacing="1.5" opacity="0.8">02.3 · VERSÃO INVERTIDA (SURFACES ESCURAS)</text>
  <g transform="translate(519, 298) scale(0.74)">
    {inner_stk_white}
  </g>
</svg>'''

# -----------------------------------------------------------------------------
# PAGE 4: CORES & TIPOGRAFIA
# -----------------------------------------------------------------------------
p4_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#FFFFFF"/>
  {header_footer(4, "03 · CORES &amp; TIPOGRAFIA INSTITUCIONAL")}

  <text x="48" y="78" font-family="{font_sans}" font-size="14" font-weight="700" fill="#191919">Paleta Cromática de Produção</text>
  
  <!-- Swatch 1: Onyx -->
  <g transform="translate(48, 96)">
    <rect width="170" height="85" fill="#191919"/>
    <rect y="85" width="170" height="100" fill="#FBFBFB" stroke="#191919" stroke-width="0.5"/>
    <text x="12" y="106" font-family="{font_sans}" font-size="11" font-weight="700" fill="#191919">Onyx Arquitetura</text>
    <text x="12" y="124" font-family="{font_mono}" font-size="8.5" fill="#191919">HEX: #191919</text>
    <text x="12" y="139" font-family="{font_mono}" font-size="8.5" fill="#6B6B6B">RGB: 25, 25, 25</text>
    <text x="12" y="154" font-family="{font_mono}" font-size="8.5" fill="#6B6B6B">CMYK: 70, 65, 65, 80</text>
    <text x="12" y="169" font-family="{font_mono}" font-size="8.5" fill="#6B6B6B">Pantone Black 6 C</text>
  </g>

  <!-- Swatch 2: Verde Palma -->
  <g transform="translate(240, 96)">
    <rect width="170" height="85" fill="#3D6E60"/>
    <rect y="85" width="170" height="100" fill="#FBFBFB" stroke="#191919" stroke-width="0.5"/>
    <text x="12" y="106" font-family="{font_sans}" font-size="11" font-weight="700" fill="#3D6E60">Verde Palma Tropical</text>
    <text x="12" y="124" font-family="{font_mono}" font-size="8.5" fill="#191919">HEX: #3D6E60</text>
    <text x="12" y="139" font-family="{font_mono}" font-size="8.5" fill="#6B6B6B">RGB: 61, 110, 96</text>
    <text x="12" y="154" font-family="{font_mono}" font-size="8.5" fill="#6B6B6B">CMYK: 75, 35, 60, 25</text>
    <text x="12" y="169" font-family="{font_mono}" font-size="8.5" fill="#6B6B6B">Pantone 5555 C</text>
  </g>

  <!-- Swatch 3: Barro Cozido -->
  <g transform="translate(432, 96)">
    <rect width="170" height="85" fill="#BA5424"/>
    <rect y="85" width="170" height="100" fill="#FBFBFB" stroke="#191919" stroke-width="0.5"/>
    <text x="12" y="106" font-family="{font_sans}" font-size="11" font-weight="700" fill="#BA5424">Barro Cozido / Terracota</text>
    <text x="12" y="124" font-family="{font_mono}" font-size="8.5" fill="#191919">HEX: #BA5424</text>
    <text x="12" y="139" font-family="{font_mono}" font-size="8.5" fill="#6B6B6B">RGB: 186, 84, 36</text>
    <text x="12" y="154" font-family="{font_mono}" font-size="8.5" fill="#6B6B6B">CMYK: 18, 78, 98, 8</text>
    <text x="12" y="169" font-family="{font_mono}" font-size="8.5" fill="#6B6B6B">Pantone 7584 C</text>
  </g>

  <!-- Swatch 4: Branco Papel -->
  <g transform="translate(624, 96)">
    <rect width="170" height="85" fill="#FFFFFF" stroke="#191919" stroke-width="0.5"/>
    <rect y="85" width="170" height="100" fill="#FBFBFB" stroke="#191919" stroke-width="0.5"/>
    <text x="12" y="106" font-family="{font_sans}" font-size="11" font-weight="700" fill="#191919">Branco Papel (Base)</text>
    <text x="12" y="124" font-family="{font_mono}" font-size="8.5" fill="#191919">HEX: #FFFFFF</text>
    <text x="12" y="139" font-family="{font_mono}" font-size="8.5" fill="#6B6B6B">RGB: 255, 255, 255</text>
    <text x="12" y="154" font-family="{font_mono}" font-size="8.5" fill="#6B6B6B">CMYK: 0, 0, 0, 0</text>
    <text x="12" y="169" font-family="{font_mono}" font-size="8.5" fill="#6B6B6B">Canvas Limpo</text>
  </g>

  <!-- Divider -->
  <line x1="48" y1="312" x2="794" y2="312" stroke="#191919" stroke-width="0.5"/>

  <!-- Section 2: Typography System -->
  <text x="48" y="340" font-family="{font_sans}" font-size="14" font-weight="700" fill="#191919">Tipografia Institucional</text>

  <g transform="translate(48, 360)">
    <rect width="340" height="150" fill="#FBFBFB" stroke="#191919" stroke-width="0.5"/>
    <text x="16" y="26" font-family="{font_sans}" font-size="10" font-weight="700" fill="#6B6B6B" letter-spacing="1">DISPLAY &amp; INTERFACE</text>
    <text x="16" y="46" font-family="{font_sans}" font-size="12" font-weight="700" fill="#191919">TWK Everett / Inter (Google Fonts)</text>
    <text x="16" y="80" font-family="{font_sans}" font-size="20" font-weight="700" fill="#191919" letter-spacing="-0.5">TRÓPIKOS ARQUITETOS</text>
    <text x="16" y="104" font-family="{font_sans}" font-size="11" fill="#191919">Projetos autorais, execução e acompanhamento.</text>
    <text x="16" y="126" font-family="{font_sans}" font-size="9" fill="#6B6B6B">ABCDEFGHIJKLMNOPQRSTUVWXYZ · 0123456789</text>
  </g>

  <g transform="translate(452, 360)">
    <rect width="342" height="150" fill="#FBFBFB" stroke="#191919" stroke-width="0.5"/>
    <text x="16" y="26" font-family="{font_mono}" font-size="9.5" font-weight="700" fill="#6B6B6B" letter-spacing="1">METADADOS, COTAS &amp; BIM</text>
    <text x="16" y="46" font-family="{font_mono}" font-size="11" font-weight="700" fill="#191919">TWK Everett Mono / JetBrains Mono</text>
    <text x="16" y="78" font-family="{font_mono}" font-size="13" font-weight="700" fill="#191919">ESCALA 1:50 · PE-2026-R02</text>
    <text x="16" y="102" font-family="{font_mono}" font-size="10" fill="#191919">AREA: 480m² · COORD: 08°03′S 34°52′W</text>
    <text x="16" y="126" font-family="{font_mono}" font-size="8.5" fill="#6B6B6B">CAU/PE: 104829-0 · SALA 0303 · ESPINHEIRO</text>
  </g>
</svg>'''

# -----------------------------------------------------------------------------
# PAGE 5: CARIMBO DE PRANCHA TÉCNICO ABNT NBR 6492
# -----------------------------------------------------------------------------
p5_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#FFFFFF"/>
  {header_footer(5, "04 · APLICAÇÃO TÉCNICA (SELO DE PRANCHA ABNT)")}

  <text x="48" y="78" font-family="{font_sans}" font-size="14" font-weight="700" fill="#191919">Carimbo de Prancha Arquitetônica (Norma ABNT NBR 6492)</text>
  <text x="48" y="98" font-family="{font_sans}" font-size="10" fill="#6B6B6B">
    Módulo padronizado de 180mm de largura pronto para pranchas A1 e A0 em AutoCAD, Revit e Archicad.
  </text>

  <!-- Centered Technical Title Block -->
  <g transform="translate(86, 126) scale(0.93)">
    {inner_carimbo}
  </g>

  <!-- 3 Explanatory Columns below -->
  <g transform="translate(48, 380)">
    <line x1="0" y1="0" x2="746" y2="0" stroke="#191919" stroke-width="0.5"/>
    
    <text x="0" y="24" font-family="{font_sans}" font-size="11" font-weight="700" fill="#191919">Normatização ABNT NBR 6492</text>
    <text x="0" y="44" font-family="{font_sans}" font-size="9" fill="#6B6B6B" width="220">
      <tspan x="0" dy="0">Dimensão oficial de 180 mm de largura,</tspan>
      <tspan x="0" dy="14">permitindo dobragem padronizada em</tspan>
      <tspan x="0" dy="14">tamanho A4 com o selo visível.</tspan>
    </text>

    <text x="260" y="24" font-family="{font_sans}" font-size="11" font-weight="700" fill="#191919">Responsabilidade Técnica CAU/PE</text>
    <text x="260" y="44" font-family="{font_sans}" font-size="9" fill="#6B6B6B">
      <tspan x="260" dy="0">Inclusão do registro profissional da</tspan>
      <tspan x="260" dy="14">autoria e coordenação técnica</tspan>
      <tspan x="260" dy="14">exigido pelos órgãos legais e prefeituras.</tspan>
    </text>

    <text x="520" y="24" font-family="{font_sans}" font-size="11" font-weight="700" fill="#3D6E60">Compatibilidade CAD / BIM</text>
    <text x="520" y="44" font-family="{font_sans}" font-size="9" fill="#6B6B6B">
      <tspan x="520" dy="0">Arquivo vetorial mestre disponível em:</tspan>
      <tspan x="520" dy="14" font-family="{font_mono}" font-size="8" fill="#191919">brand-kit/architectural-cad/</tspan>
      <tspan x="520" dy="14" font-family="{font_mono}" font-size="8" fill="#3D6E60">tropikos-carimbo-prancha.svg</tspan>
    </text>
  </g>
</svg>'''

# -----------------------------------------------------------------------------
# PAGE 6: AMBIENTE DIGITAL & WEB
# -----------------------------------------------------------------------------
p6_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#FFFFFF"/>
  {header_footer(6, "05 · AMBIENTE DIGITAL &amp; IMPLEMENTAÇÃO WEB")}

  <text x="48" y="78" font-family="{font_sans}" font-size="14" font-weight="700" fill="#191919">Ecossistema Web &amp; Favicons Nativos</text>
  <text x="48" y="98" font-family="{font_sans}" font-size="10" fill="#6B6B6B">
    Assets otimizados gerados e já integrados ao diretório public/ do novo site Astro.
  </text>

  <!-- Left: Favicons Package Display -->
  <g transform="translate(48, 120)">
    <rect width="280" height="280" fill="#FBFBFB" stroke="#191919" stroke-width="0.8"/>
    <text x="20" y="28" font-family="{font_sans}" font-size="10" font-weight="700" fill="#191919" letter-spacing="1">PACOTE DE FAVICONS EM PUBLIC/</text>
    
    <!-- Real App Icon Tile Preview -->
    <rect x="20" y="46" width="64" height="64" rx="14" fill="#191919"/>
    <g transform="translate(26, 52) scale(0.20)">
      {inner_stk_white}
    </g>

    <!-- 32px Tile -->
    <rect x="100" y="62" width="36" height="36" rx="8" fill="#191919"/>
    <g transform="translate(104, 66) scale(0.11)">
      {inner_stk_white}
    </g>

    <!-- 16px Tile -->
    <rect x="150" y="74" width="20" height="20" rx="4" fill="#191919"/>
    <g transform="translate(152, 76) scale(0.062)">
      {inner_stk_white}
    </g>

    <line x1="20" y1="128" x2="260" y2="128" stroke="#191919" stroke-width="0.5"/>
    <text x="20" y="148" font-family="{font_mono}" font-size="8.5" fill="#191919">• public/favicon.ico (Multi-res)</text>
    <text x="20" y="166" font-family="{font_mono}" font-size="8.5" fill="#191919">• public/favicon.svg (Vetorial puro)</text>
    <text x="20" y="184" font-family="{font_mono}" font-size="8.5" fill="#191919">• public/apple-touch-icon.png (180)</text>
    <text x="20" y="202" font-family="{font_mono}" font-size="8.5" fill="#191919">• public/favicon-96x96.png</text>
    <text x="20" y="220" font-family="{font_mono}" font-size="8.5" fill="#191919">• public/site.webmanifest</text>
    <text x="20" y="250" font-family="{font_sans}" font-size="9.5" font-weight="700" fill="#3D6E60">✓ 100% instalados no site Astro</text>
  </g>

  <!-- Right: Code Card -->
  <g transform="translate(348, 120)">
    <rect width="446" height="280" fill="#191919"/>
    <!-- Window Chrome -->
    <circle cx="20" cy="18" r="4" fill="#FF5F56"/>
    <circle cx="34" cy="18" r="4" fill="#FFBD2E"/>
    <circle cx="48" cy="18" r="4" fill="#27C93F"/>
    <text x="70" y="22" font-family="{font_mono}" font-size="8.5" fill="#FFFFFF" opacity="0.6">src/components/Logo.astro</text>
    <line x1="0" y1="34" x2="446" y2="34" stroke="#FFFFFF" stroke-width="0.5" opacity="0.15"/>

    <!-- Code Lines -->
    <text x="20" y="60" font-family="{font_mono}" font-size="9" fill="#3D6E60">---</text>
    <text x="20" y="78" font-family="{font_mono}" font-size="9" fill="#D97746">import Logo from '@/components/Logo.astro';</text>
    <text x="20" y="96" font-family="{font_mono}" font-size="9" fill="#3D6E60">---</text>
    
    <text x="20" y="130" font-family="{font_mono}" font-size="8.5" fill="#808080">&lt;!-- Barra de navegação: Lockup Horizontal --&gt;</text>
    <text x="20" y="148" font-family="{font_mono}" font-size="9" fill="#FFFFFF">&lt;Logo variant="horizontal" color="color" class="h-9 w-auto" /&gt;</text>
    
    <text x="20" y="184" font-family="{font_mono}" font-size="8.5" fill="#808080">&lt;!-- Rodapé: Versão Stacked Invertida --&gt;</text>
    <text x="20" y="202" font-family="{font_mono}" font-size="9" fill="#FFFFFF">&lt;Logo variant="stacked" color="white" class="h-16 w-auto" /&gt;</text>
    
    <text x="20" y="238" font-family="{font_mono}" font-size="8.5" fill="#808080">&lt;!-- Símbolo 3x3 Autônomo para Redes / App --&gt;</text>
    <text x="20" y="256" font-family="{font_mono}" font-size="9" fill="#FFFFFF">&lt;Logo variant="symbol" color="palm" class="w-12 h-12" /&gt;</text>
  </g>

  <!-- Bottom: CLS metric -->
  <g transform="translate(48, 424)">
    <line x1="0" y1="0" x2="746" y2="0" stroke="#191919" stroke-width="0.5"/>
    <text x="0" y="24" font-family="{font_sans}" font-size="11" font-weight="700" fill="#191919">Performance Máxima: Cumulative Layout Shift (CLS: 0.00)</text>
    <text x="0" y="44" font-family="{font_sans}" font-size="9.5" fill="#6B6B6B">
      <tspan x="0" dy="0">O componente &lt;Logo /&gt; renderiza SVGs puros em linha com viewBox estático, eliminando qualquer dependência de rede,</tspan>
      <tspan x="0" dy="16">bloqueio de renderização ou salto visual durante o carregamento de páginas estáticas do Astro.</tspan>
    </text>
  </g>
</svg>'''

# -----------------------------------------------------------------------------
# PAGE 7: DIRETRIZES DE USO & GOVERNANÇA
# -----------------------------------------------------------------------------
p7_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#FFFFFF"/>
  {header_footer(7, "06 · DIRETRIZES DE USO &amp; GOVERNANÇA")}

  <text x="48" y="78" font-family="{font_sans}" font-size="14" font-weight="700" fill="#191919">Regras de Proteção &amp; O Que NÃO Fazer</text>

  <!-- Left: Clear Space Box -->
  <g transform="translate(48, 106)">
    <rect width="360" height="210" fill="#FBFBFB" stroke="#191919" stroke-width="0.8"/>
    <text x="20" y="26" font-family="{font_sans}" font-size="10" font-weight="700" fill="#191919" letter-spacing="1">ÁREA DE PROTEÇÃO MÍNIMA (1X)</text>
    
    <!-- Boundary guide mathematically calculated with X=22px padding -->
    <rect x="123" y="47" width="114" height="142" fill="none" stroke="#BA5424" stroke-dasharray="3 3" stroke-width="0.8"/>
    
    <!-- Dimension lines and labels -->
    <text x="104" y="121" font-family="{font_mono}" font-size="8.5" font-weight="700" fill="#BA5424" text-anchor="middle">1X</text>
    <line x1="113" y1="118" x2="123" y2="118" stroke="#BA5424" stroke-width="0.6"/>
    <line x1="123" y1="114" x2="123" y2="122" stroke="#BA5424" stroke-width="0.6"/>

    <text x="254" y="121" font-family="{font_mono}" font-size="8.5" font-weight="700" fill="#BA5424" text-anchor="middle">1X</text>
    <line x1="237" y1="118" x2="247" y2="118" stroke="#BA5424" stroke-width="0.6"/>
    <line x1="237" y1="114" x2="237" y2="122" stroke="#BA5424" stroke-width="0.6"/>

    <text x="180" y="41" font-family="{font_mono}" font-size="8.5" font-weight="700" text-anchor="middle" fill="#BA5424">1X</text>
    <text x="180" y="202" font-family="{font_mono}" font-size="8.5" font-weight="700" text-anchor="middle" fill="#BA5424">1X</text>
    
    <g transform="translate(124, 63) scale(0.44)">
      {inner_stk_color}
    </g>
  </g>

  <!-- Right: Strict Don'ts -->
  <g transform="translate(434, 106)">
    <rect width="360" height="210" fill="#FFFFFF" stroke="#191919" stroke-width="0.8"/>
    <text x="20" y="26" font-family="{font_sans}" font-size="10" font-weight="700" fill="#BA5424" letter-spacing="1">PROIBIÇÕES ESTRITAS DE USO (DON'TS)</text>
    
    <text x="20" y="56" font-family="{font_sans}" font-size="9" fill="#191919">
      <tspan x="20" dy="0" font-weight="700">✖ NÃO esticar ou achatar:</tspan>
      <tspan x="180" dy="0" fill="#6B6B6B">Mantenha a proporção 1:1.</tspan>
      <tspan x="20" dy="24" font-weight="700">✖ NÃO alterar cores:</tspan>
      <tspan x="180" dy="0" fill="#6B6B6B">Use somente a paleta aprovada.</tspan>
      <tspan x="20" dy="24" font-weight="700">✖ NÃO aplicar efeitos:</tspan>
      <tspan x="180" dy="0" fill="#6B6B6B">Proibido sombras, chanfros ou gradientes.</tspan>
      <tspan x="20" dy="24" font-weight="700">✖ NÃO rotacionar:</tspan>
      <tspan x="180" dy="0" fill="#6B6B6B">Aplicação sempre ortogonal e plana.</tspan>
      <tspan x="20" dy="24" font-weight="700">✖ NÃO redigitar a marca:</tspan>
      <tspan x="180" dy="0" fill="#6B6B6B">Use os arquivos vetoriais mestres.</tspan>
      <tspan x="20" dy="24" font-weight="700">✖ NÃO alterar o pátio:</tspan>
      <tspan x="180" dy="0" fill="#6B6B6B">As curvas de nível são proprietárias.</tspan>
    </text>
  </g>

  <!-- Minimum Sizes -->
  <g transform="translate(48, 336)">
    <text x="0" y="20" font-family="{font_sans}" font-size="11" font-weight="700" fill="#191919">Dimensões Mínimas Recomendadas:</text>
    <text x="0" y="42" font-family="{font_sans}" font-size="9.5" fill="#6B6B6B">
      <tspan x="0" dy="0">• Versão Horizontal: Mínimo 120 px na web · Mínimo 30 mm em pranchas e impressos.</tspan>
      <tspan x="0" dy="16">• Versão Stacked: Mínimo 64 px na web · Mínimo 20 mm em impressos e placas.</tspan>
      <tspan x="0" dy="16">• Símbolo Autônomo: Mínimo 16 px (utilizar tropikos-symbol-small.svg / favicon.svg).</tspan>
    </text>
  </g>

  <!-- Sign-off Footer -->
  <g transform="translate(48, 440)">
    <line x1="0" y1="0" x2="746" y2="0" stroke="#191919" stroke-width="0.8"/>
    <text x="0" y="26" font-family="{font_sans}" font-size="10.5" font-weight="700" fill="#191919">TRÓPIKOS ARQUITETOS · ESCRITÓRIO DE ARQUITETURA E INTERIORES</text>
    <text x="0" y="46" font-family="{font_sans}" font-size="9" fill="#6B6B6B">Rua Ferreira Lopes, 334 — Salas 201/202/203 · Parnamirim, Recife — PE · 52060-235 · tropikosarquitetura@gmail.com</text>
    <text x="0" y="64" font-family="{font_mono}" font-size="8.5" fill="#3D6E60">Identidade aprovada para implantação imediata em todos os canais físicos e digitais.</text>
  </g>
</svg>'''

pages = [
    ("page-1.svg", p1_svg),
    ("page-2.svg", p2_svg),
    ("page-3.svg", p3_svg),
    ("page-4.svg", p4_svg),
    ("page-5.svg", p5_svg),
    ("page-6.svg", p6_svg),
    ("page-7.svg", p7_svg),
]

writer = PdfWriter()

for fname, svg_content in pages:
    svg_path = os.path.join(pdf_pages_dir, fname)
    pdf_path = svg_path.replace(".svg", ".pdf")
    png_path = os.path.join(pdf_renders_dir, fname.replace(".svg", ".png"))
    with open(svg_path, "w") as f:
        f.write(svg_content)
    # Vector PDF
    cairosvg.svg2pdf(url=svg_path, write_to=pdf_path)
    # High-res PNG preview
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=1684, output_height=1190)
    writer.append(pdf_path)
    print(f"Rendered: {fname} -> PDF & PNG")

final_pdf = os.path.join(out_dir, "Tropikos-Brand-Kit.pdf")
with open(final_pdf, "wb") as f:
    writer.write(f)

print(f"Monograph PDF completely rebuilt: {final_pdf}")
