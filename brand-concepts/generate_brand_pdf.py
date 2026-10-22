import os
import cairosvg
from pypdf import PdfWriter

W = 842
H = 595

out_dir = "/home/civo/tropikos/brand-kit"
pdf_pages_dir = os.path.join(out_dir, "pdf-pages")
os.makedirs(pdf_pages_dir, exist_ok=True)

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

# Base style for all pages
font_family = "'TWK Everett', 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
mono_family = "'TWK Everett Mono', 'JetBrains Mono', monospace"

def header_footer(page_num, title):
    return f'''
    <!-- Top Hairline Rule -->
    <line x1="50" y1="44" x2="792" y2="44" stroke="#191919" stroke-width="0.8" opacity="0.3"/>
    <text x="50" y="36" font-family="{font_family}" font-size="8" font-weight="600" fill="#191919" letter-spacing="1.5">TRÓPIKOS ARQUITETOS · MANUAL DE IDENTIDADE VISUAL</text>
    <text x="792" y="36" font-family="{font_family}" font-size="8" font-weight="600" text-anchor="end" fill="#6B6B6B" letter-spacing="1">{title}</text>
    
    <!-- Bottom Hairline Rule -->
    <line x1="50" y1="550" x2="792" y2="550" stroke="#191919" stroke-width="0.8" opacity="0.3"/>
    <text x="50" y="568" font-family="{mono_family}" font-size="8" fill="#6B6B6B">RECIFE — PE · 08°03′S 34°52′W</text>
    <text x="792" y="568" font-family="{mono_family}" font-size="8" text-anchor="end" fill="#191919">{page_num:02d} / 07</text>
    '''

# -----------------------------------------------------------------------------
# PAGE 1: COVER
# -----------------------------------------------------------------------------
p1_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#FFFFFF"/>
  <rect x="25" y="25" width="{W-50}" height="{H-50}" fill="none" stroke="#191919" stroke-width="1.5"/>
  
  <!-- Header meta -->
  <text x="54" y="60" font-family="{font_family}" font-size="9" font-weight="600" fill="#191919" letter-spacing="2">TRÓPIKOS ARQUITETOS · RECIFE / PE</text>
  <text x="788" y="60" font-family="{mono_family}" font-size="9" text-anchor="end" fill="#6B6B6B">DOC. REF: BK-2026-V2</text>
  <line x1="54" y1="72" x2="788" y2="72" stroke="#191919" stroke-width="1"/>

  <!-- Monumental Center Presentation -->
  <g transform="translate(321, 130) scale(1.0)">
    {inner_stk_color}
  </g>

  <!-- Title & Subtitle Bottom -->
  <line x1="54" y1="440" x2="788" y2="440" stroke="#191919" stroke-width="1"/>
  <text x="54" y="475" font-family="{font_family}" font-size="28" font-weight="bold" fill="#191919" letter-spacing="-0.5">MANUAL DE IDENTIDADE VISUAL &amp; BRAND KIT</text>
  <text x="54" y="500" font-family="{font_family}" font-size="12" fill="#6B6B6B" letter-spacing="0.5">Arquitetura autoral. Obra sob controle. Diretrizes de produção gráfica, digital e executiva.</text>

  <text x="788" y="475" font-family="{font_family}" font-size="11" font-weight="600" text-anchor="end" fill="#191919">EDIÇÃO DE PRODUÇÃO</text>
  <text x="788" y="495" font-family="{mono_family}" font-size="10" text-anchor="end" fill="#3D6E60">OUTUBRO / 2026</text>
</svg>'''

# -----------------------------------------------------------------------------
# PAGE 2: CONCEITO & ANATOMIA
# -----------------------------------------------------------------------------
p2_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#FFFFFF"/>
  {header_footer(2, "01 · CONCEITO &amp; ANATOMIA DO GRID")}

  <!-- Left Column: The Concept Narrative -->
  <text x="50" y="85" font-family="{font_family}" font-size="16" font-weight="bold" fill="#191919">A Síntese entre Rigor e Clima</text>
  <text x="50" y="115" font-family="{font_family}" font-size="10.5" fill="#191919" width="340">
    <tspan x="50" dy="0">O redesign do logotipo da Trópikos Arquitetos preserva</tspan>
    <tspan x="50" dy="16">100% da identidade conceitual que fundou o escritório:</tspan>
    <tspan x="50" dy="16">a tensão produtiva entre a estrutura ortogonal da arquitetura</tspan>
    <tspan x="50" dy="16">e a organicidade do relevo, vento e luz tropical do Recife.</tspan>
  </text>

  <text x="50" y="200" font-family="{font_family}" font-size="12" font-weight="bold" fill="#191919">A Métrica Silábica 3×3 (TRÓ · PI · KOS)</text>
  <text x="50" y="222" font-family="{font_family}" font-size="10" fill="#6B6B6B">
    <tspan x="50" dy="0">A distribuição das 8 letras segue a métrica fonética do nome.</tspan>
    <tspan x="50" dy="15">Cada linha de letras atua como uma laje estrutural de concreto,</tspan>
    <tspan x="50" dy="15">com proporções puras inspiradas no modernismo brasileiro.</tspan>
  </text>

  <text x="50" y="290" font-family="{font_family}" font-size="12" font-weight="bold" fill="#3D6E60">O Pátio Topográfico Interno (9ª Célula)</text>
  <text x="50" y="312" font-family="{font_family}" font-size="10" fill="#6B6B6B">
    <tspan x="50" dy="0">A 9ª célula aberta não é um vazio acidental: é o pátio interno,</tspan>
    <tspan x="50" dy="15">o recanto vegetal ventilado que permite à luz e ao vento</tspan>
    <tspan x="50" dy="15">atravessarem o volume construído. As 4 curvas desenham o relevo</tspan>
    <tspan x="50" dy="15">e a drenagem natural da paisagem litorânea pernambucana.</tspan>
  </text>

  <!-- Right Column: Visual Diagram -->
  <rect x="440" y="75" width="352" height="440" fill="#FBFBFB" stroke="#191919" stroke-width="0.8"/>
  <text x="460" y="105" font-family="{font_family}" font-size="11" font-weight="bold" fill="#191919">MALHA GEOMÉTRICA &amp; NORMAS DO GRID</text>
  
  <!-- Diagram with grid lines -->
  <g transform="translate(490, 140) scale(1.0)">
    <!-- 3x3 background boxes -->
    <rect x="44" y="44" width="46" height="46" fill="none" stroke="#6B6B6B" stroke-dasharray="2 2" stroke-width="0.8"/>
    <rect x="105" y="44" width="46" height="46" fill="none" stroke="#6B6B6B" stroke-dasharray="2 2" stroke-width="0.8"/>
    <rect x="166" y="44" width="46" height="46" fill="none" stroke="#6B6B6B" stroke-dasharray="2 2" stroke-width="0.8"/>
    
    <rect x="44" y="105" width="46" height="46" fill="#EAF2EF" stroke="#3D6E60" stroke-width="1.2"/>
    <rect x="105" y="105" width="46" height="46" fill="none" stroke="#6B6B6B" stroke-dasharray="2 2" stroke-width="0.8"/>
    <rect x="166" y="105" width="46" height="46" fill="none" stroke="#6B6B6B" stroke-dasharray="2 2" stroke-width="0.8"/>
    
    <rect x="44" y="166" width="46" height="46" fill="none" stroke="#6B6B6B" stroke-dasharray="2 2" stroke-width="0.8"/>
    <rect x="105" y="166" width="46" height="46" fill="none" stroke="#6B6B6B" stroke-dasharray="2 2" stroke-width="0.8"/>
    <rect x="166" y="166" width="46" height="46" fill="none" stroke="#6B6B6B" stroke-dasharray="2 2" stroke-width="0.8"/>

    {inner_stk_color}
  </g>

  <!-- Annotations -->
  <line x1="490" y1="460" x2="534" y2="460" stroke="#191919" stroke-width="1"/>
  <text x="540" y="463" font-family="{mono_family}" font-size="8" fill="#191919">CÉLULA 46×46 px · GAP 15 px</text>
  <text x="540" y="475" font-family="{mono_family}" font-size="8" fill="#3D6E60">ÁREA DO PÁTIO: ISOLINHAS 3.8 px</text>
  <text x="540" y="487" font-family="{mono_family}" font-size="8" fill="#BA5424">ARQUITETOS: CAP-HEIGHT 19 px · TRACKING 15</text>
</svg>'''

# -----------------------------------------------------------------------------
# PAGE 3: SISTEMA DE LOGOTIPOS
# -----------------------------------------------------------------------------
p3_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#FFFFFF"/>
  {header_footer(3, "02 · SISTEMA DE LOGOTIPOS")}

  <!-- 1. Horizontal Lockup Box -->
  <rect x="50" y="70" width="742" height="150" fill="#FFFFFF" stroke="#191919" stroke-width="0.8"/>
  <text x="70" y="92" font-family="{font_family}" font-size="9" font-weight="600" fill="#6B6B6B" letter-spacing="1">VERSÃO HORIZONTAL (CABEÇALHOS WEB, PAPELARIA &amp; ASSINATURAS)</text>
  <g transform="translate(130, 42) scale(0.72)">
    {inner_horiz_color}
  </g>

  <!-- 2. Master Stacked on Light -->
  <rect x="50" y="240" width="360" height="270" fill="#FFFFFF" stroke="#191919" stroke-width="0.8"/>
  <text x="70" y="262" font-family="{font_family}" font-size="9" font-weight="600" fill="#6B6B6B" letter-spacing="1">MASTER STACKED (CAPAS &amp; PRANCHAS)</text>
  <g transform="translate(105, 255) scale(0.95)">
    {inner_stk_color}
  </g>

  <!-- 3. Inverted Master on Onyx Dark Surface -->
  <rect x="432" y="240" width="360" height="270" fill="#191919"/>
  <text x="452" y="262" font-family="{font_family}" font-size="9" font-weight="600" fill="#FFFFFF" letter-spacing="1" opacity="0.7">VERSÃO INVERTIDA (SURFACES ESCURAS &amp; MODO NOTURNO)</text>
  <g transform="translate(487, 255) scale(0.95)">
    {inner_stk_white}
  </g>
</svg>'''

# -----------------------------------------------------------------------------
# PAGE 4: CORES & TIPOGRAFIA
# -----------------------------------------------------------------------------
p4_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#FFFFFF"/>
  {header_footer(4, "03 · CORES &amp; TIPOGRAFIA INSTITUCIONAL")}

  <!-- Section 1: Color Palette -->
  <text x="50" y="80" font-family="{font_family}" font-size="14" font-weight="bold" fill="#191919">Paleta Cromática de Produção</text>
  
  <!-- Swatch 1: Onyx -->
  <rect x="50" y="100" width="168" height="110" fill="#191919"/>
  <text x="50" y="230" font-family="{font_family}" font-size="12" font-weight="bold" fill="#191919">Onyx (Preto Arquitetura)</text>
  <text x="50" y="248" font-family="{mono_family}" font-size="9" fill="#191919">HEX: #191919</text>
  <text x="50" y="262" font-family="{mono_family}" font-size="9" fill="#6B6B6B">RGB: 25, 25, 25</text>
  <text x="50" y="276" font-family="{mono_family}" font-size="9" fill="#6B6B6B">CMYK: 70, 65, 65, 80</text>
  <text x="50" y="290" font-family="{mono_family}" font-size="9" fill="#6B6B6B">Pantone Black 6 C</text>

  <!-- Swatch 2: Verde Palma -->
  <rect x="241" y="100" width="168" height="110" fill="#3D6E60"/>
  <text x="241" y="230" font-family="{font_family}" font-size="12" font-weight="bold" fill="#3D6E60">Verde Palma (Tropical)</text>
  <text x="241" y="248" font-family="{mono_family}" font-size="9" fill="#191919">HEX: #3D6E60</text>
  <text x="241" y="262" font-family="{mono_family}" font-size="9" fill="#6B6B6B">RGB: 61, 110, 96</text>
  <text x="241" y="276" font-family="{mono_family}" font-size="9" fill="#6B6B6B">CMYK: 75, 35, 60, 25</text>
  <text x="241" y="290" font-family="{mono_family}" font-size="9" fill="#6B6B6B">Pantone 5555 C</text>

  <!-- Swatch 3: Barro Cozido -->
  <rect x="432" y="100" width="168" height="110" fill="#BA5424"/>
  <text x="432" y="230" font-family="{font_family}" font-size="12" font-weight="bold" fill="#BA5424">Barro Cozido (Terracota)</text>
  <text x="432" y="248" font-family="{mono_family}" font-size="9" fill="#191919">HEX: #BA5424</text>
  <text x="432" y="262" font-family="{mono_family}" font-size="9" fill="#6B6B6B">RGB: 186, 84, 36</text>
  <text x="432" y="276" font-family="{mono_family}" font-size="9" fill="#6B6B6B">CMYK: 18, 78, 98, 8</text>
  <text x="432" y="290" font-family="{mono_family}" font-size="9" fill="#6B6B6B">Pantone 7584 C</text>

  <!-- Swatch 4: Papel -->
  <rect x="623" y="100" width="168" height="110" fill="#FFFFFF" stroke="#191919" stroke-width="0.8"/>
  <text x="623" y="230" font-family="{font_family}" font-size="12" font-weight="bold" fill="#191919">Branco Papel (Base)</text>
  <text x="623" y="248" font-family="{mono_family}" font-size="9" fill="#191919">HEX: #FFFFFF</text>
  <text x="623" y="262" font-family="{mono_family}" font-size="9" fill="#6B6B6B">RGB: 255, 255, 255</text>
  <text x="623" y="276" font-family="{mono_family}" font-size="9" fill="#6B6B6B">CMYK: 0, 0, 0, 0</text>
  <text x="623" y="290" font-family="{mono_family}" font-size="9" fill="#6B6B6B">Canvas Puro</text>

  <!-- Divider -->
  <line x1="50" y1="320" x2="792" y2="320" stroke="#191919" stroke-width="0.8" opacity="0.3"/>

  <!-- Section 2: Typography System -->
  <text x="50" y="348" font-family="{font_family}" font-size="14" font-weight="bold" fill="#191919">Tipografia Institucional</text>

  <text x="50" y="380" font-family="{font_family}" font-size="12" font-weight="600" fill="#191919">Display &amp; Interface — TWK Everett / Inter</text>
  <text x="50" y="405" font-family="{font_family}" font-size="24" font-weight="bold" fill="#191919" letter-spacing="-0.5">TRÓPIKOS ARQUITETOS · RECIFE</text>
  <text x="50" y="430" font-family="{font_family}" font-size="11" fill="#6B6B6B">
    Projetos residenciais, corporativos e interiores autorais construídos com precisão e disciplina.
  </text>

  <text x="50" y="475" font-family="{font_family}" font-size="12" font-weight="600" fill="#191919">Dados Técnicos &amp; Metadados — TWK Everett Mono / JetBrains Mono</text>
  <text x="50" y="500" font-family="{mono_family}" font-size="12" fill="#191919">
    AREA: 480m² · COORD: 08°03′14″S 34°52′52″W · ESCALA 1:50 · PE-2026-R02
  </text>
</svg>'''

# -----------------------------------------------------------------------------
# PAGE 5: CARIMBO DE PRANCHA TÉCNICO ABNT NBR 6492
# -----------------------------------------------------------------------------
p5_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#FFFFFF"/>
  {header_footer(5, "04 · APLICAÇÃO TÉCNICA (SELO DE PRANCHA ABNT)")}

  <text x="50" y="80" font-family="{font_family}" font-size="14" font-weight="bold" fill="#191919">Carimbo de Prancha Arquitetônica (Norma ABNT NBR 6492)</text>
  <text x="50" y="100" font-family="{font_family}" font-size="10" fill="#6B6B6B">
    Módulo oficial padronizado (largura 180mm standard) pronto para pranchas A1 e A0 em AutoCAD, Revit e Archicad.
  </text>

  <!-- Embed Technical Title Block -->
  <g transform="translate(61, 130) scale(1.0)">
    {inner_carimbo}
  </g>

  <!-- Explanatory notes below -->
  <text x="50" y="410" font-family="{font_family}" font-size="11" font-weight="bold" fill="#191919">Especificações de Execução Técnica:</text>
  <text x="50" y="432" font-family="{font_family}" font-size="10" fill="#6B6B6B">
    <tspan x="50" dy="0">• Bloco esquerdo: aplicação da marca institucional com registro de responsabilidade técnica CAU/PE.</tspan>
    <tspan x="50" dy="16">• Bloco central: campos normatizados de identificação de projeto, fase executiva, endereço e coordenação.</tspan>
    <tspan x="50" dy="16">• Bloco direito: escala numérica em monoespaçada, controle de revisões e numeração serial de pranchas.</tspan>
    <tspan x="50" dy="16">• Arquivo vetorial pronto disponível em: <tspan fill="#3D6E60" font-weight="600">brand-kit/architectural-cad/tropikos-carimbo-prancha.svg</tspan></tspan>
  </text>
</svg>'''

# -----------------------------------------------------------------------------
# PAGE 6: AMBIENTE DIGITAL & WEB
# -----------------------------------------------------------------------------
p6_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#FFFFFF"/>
  {header_footer(6, "05 · AMBIENTE DIGITAL &amp; IMPLEMENTAÇÃO WEB")}

  <text x="50" y="80" font-family="{font_family}" font-size="14" font-weight="bold" fill="#191919">Ecossistema Web &amp; Favicons Nativos</text>
  <text x="50" y="100" font-family="{font_family}" font-size="10" fill="#6B6B6B">
    Todos os assets foram gerados e já integrados ao diretório public/ do novo site Astro.
  </text>

  <!-- 3 Boxes of Digital Assets -->
  <!-- Box 1: Favicons -->
  <rect x="50" y="120" width="230" height="260" fill="#FBFBFB" stroke="#191919" stroke-width="0.8"/>
  <text x="65" y="145" font-family="{font_family}" font-size="11" font-weight="bold" fill="#191919">PACOTE DE FAVICONS</text>
  <!-- Mini 16, 32, 48 previews -->
  <rect x="65" y="165" width="48" height="48" fill="#191919" rx="10"/>
  <rect x="130" y="173" width="32" height="32" fill="#191919" rx="6"/>
  <rect x="180" y="181" width="16" height="16" fill="#191919" rx="3"/>
  <text x="65" y="240" font-family="{mono_family}" font-size="8" fill="#191919">public/favicon.ico (Multi-res)</text>
  <text x="65" y="255" font-family="{mono_family}" font-size="8" fill="#191919">public/favicon.svg (Vetorial)</text>
  <text x="65" y="270" font-family="{mono_family}" font-size="8" fill="#191919">public/apple-touch-icon.png (180)</text>
  <text x="65" y="285" font-family="{mono_family}" font-size="8" fill="#191919">public/favicon-96x96.png</text>
  <text x="65" y="300" font-family="{mono_family}" font-size="8" fill="#191919">public/site.webmanifest</text>
  <text x="65" y="325" font-family="{font_family}" font-size="9" fill="#3D6E60">✓ 100% instalados no site Astro</text>

  <!-- Box 2: Native Astro Component -->
  <rect x="306" y="120" width="486" height="260" fill="#191919"/>
  <text x="325" y="145" font-family="{mono_family}" font-size="10" font-weight="bold" fill="#FFFFFF">COMPONENTE NATIVO: src/components/Logo.astro</text>
  <text x="325" y="175" font-family="{mono_family}" font-size="9" fill="#3D6E60">---</text>
  <text x="325" y="190" font-family="{mono_family}" font-size="9" fill="#D97746">import Logo from '@/components/Logo.astro';</text>
  <text x="325" y="205" font-family="{mono_family}" font-size="9" fill="#3D6E60">---</text>
  <text x="325" y="235" font-family="{mono_family}" font-size="9" fill="#A8D0C0">&lt;!-- Navbar: Lockup Horizontal Colorido --&gt;</text>
  <text x="325" y="250" font-family="{mono_family}" font-size="9" fill="#FFFFFF">&lt;Logo variant="horizontal" color="color" class="h-9 w-auto" /&gt;</text>
  
  <text x="325" y="280" font-family="{mono_family}" font-size="9" fill="#A8D0C0">&lt;!-- Rodapé: Versão Stacked Invertida --&gt;</text>
  <text x="325" y="295" font-family="{mono_family}" font-size="9" fill="#FFFFFF">&lt;Logo variant="stacked" color="white" class="h-16 w-auto" /&gt;</text>
  
  <text x="325" y="325" font-family="{mono_family}" font-size="9" fill="#A8D0C0">&lt;!-- Símbolo Puro para Avatares &amp; App --&gt;</text>
  <text x="325" y="340" font-family="{mono_family}" font-size="9" fill="#FFFFFF">&lt;Logo variant="symbol" color="palm" class="w-12 h-12" /&gt;</text>

  <!-- Bottom Rules for Web -->
  <text x="50" y="420" font-family="{font_family}" font-size="12" font-weight="bold" fill="#191919">Performance &amp; Zero Layout Shift (CLS 0.00)</text>
  <text x="50" y="442" font-family="{font_family}" font-size="10" fill="#6B6B6B">
    <tspan x="50" dy="0">O componente &lt;Logo /&gt; renderiza SVGs puros em linha com viewBox estático, garantindo carregamento instantâneo,</tspan>
    <tspan x="50" dy="16">zero requisições de rede adicionais e perfeita nitidez em telas Retina, 4K e dispositivos móveis.</tspan>
  </text>
</svg>'''

# -----------------------------------------------------------------------------
# PAGE 7: DIRETRIZES DE USO & DON'TS
# -----------------------------------------------------------------------------
p7_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <rect width="{W}" height="{H}" fill="#FFFFFF"/>
  {header_footer(7, "06 · DIRETRIZES DE USO &amp; GOVERNANÇA")}

  <text x="50" y="80" font-family="{font_family}" font-size="14" font-weight="bold" fill="#191919">Regras de Proteção &amp; O Que NÃO Fazer</text>

  <!-- Clear Space Diagram -->
  <rect x="50" y="110" width="350" height="200" fill="#FBFBFB" stroke="#191919" stroke-width="0.8"/>
  <text x="70" y="135" font-family="{font_family}" font-size="11" font-weight="bold" fill="#191919">ÁREA DE PROTEÇÃO MÍNIMA (1X)</text>
  <!-- Bounding box with X guides -->
  <rect x="150" y="150" width="150" height="130" fill="none" stroke="#BA5424" stroke-dasharray="3 3"/>
  <text x="130" y="215" font-family="{mono_family}" font-size="9" fill="#BA5424">1X</text>
  <text x="310" y="215" font-family="{mono_family}" font-size="9" fill="#BA5424">1X</text>
  <text x="220" y="145" font-family="{mono_family}" font-size="9" text-anchor="middle" fill="#BA5424">1X</text>
  <text x="220" y="295" font-family="{mono_family}" font-size="9" text-anchor="middle" fill="#BA5424">1X</text>
  <g transform="translate(170, 155) scale(0.45)">
    {inner_stk_color}
  </g>

  <!-- Don'ts List -->
  <rect x="420" y="110" width="372" height="200" fill="#FFFFFF" stroke="#BA5424" stroke-width="1.2"/>
  <text x="440" y="135" font-family="{font_family}" font-size="11" font-weight="bold" fill="#BA5424">PROIBIÇÕES ESTRITAS DE USO (DON'TS)</text>
  <text x="440" y="160" font-family="{font_family}" font-size="10" fill="#191919">
    <tspan x="440" dy="0">✖ NUNCA estique, comprima ou distorça as proporções.</tspan>
    <tspan x="440" dy="18">✖ NUNCA altere as cores da paleta oficial.</tspan>
    <tspan x="440" dy="18">✖ NUNCA aplique sombras (drop shadows), gradientes ou chanfros.</tspan>
    <tspan x="440" dy="18">✖ NUNCA rotacione o logotipo em ângulos diagonais.</tspan>
    <tspan x="440" dy="18">✖ NUNCA tente redigitar o logotipo usando fontes comerciais.</tspan>
    <tspan x="440" dy="18">✖ NUNCA substitua as curvas de nível por texturas aleatórias.</tspan>
  </text>

  <!-- Summary of Minimum Sizes -->
  <text x="50" y="345" font-family="{font_family}" font-size="12" font-weight="bold" fill="#191919">Dimensões Mínimas Recomendadas:</text>
  <text x="50" y="370" font-family="{font_family}" font-size="10" fill="#6B6B6B">
    <tspan x="50" dy="0">• Versão Horizontal: Mínimo 120 px na web · Mínimo 30 mm em pranchas e impressos.</tspan>
    <tspan x="50" dy="16">• Versão Stacked: Mínimo 64 px na web · Mínimo 20 mm em impressos e placas.</tspan>
    <tspan x="50" dy="16">• Símbolo Autônomo: Mínimo 16 px (utilizar tropikos-symbol-small.svg / favicon.svg).</tspan>
  </text>

  <!-- Closing Sign-off -->
  <line x1="50" y1="440" x2="792" y2="440" stroke="#191919" stroke-width="1"/>
  <text x="50" y="470" font-family="{font_family}" font-size="11" font-weight="bold" fill="#191919">TRÓPIKOS ARQUITETOS · ESCRITÓRIO DE ARQUITETURA E INTERIORES</text>
  <text x="50" y="490" font-family="{font_family}" font-size="10" fill="#6B6B6B">Rua Ferreira Lopes, 334 — Salas 201/202/203 · Parnamirim, Recife — PE · 52060-235 · tropikosarquitetura@gmail.com</text>
  <text x="50" y="508" font-family="{mono_family}" font-size="9" fill="#3D6E60">Identidade aprovada para implantação imediata em todos os canais físicos e digitais.</text>
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
    with open(svg_path, "w") as f:
        f.write(svg_content)
    # Convert to vector PDF via cairosvg
    cairosvg.svg2pdf(url=svg_path, write_to=pdf_path)
    writer.append(pdf_path)
    print(f"Rendered vector PDF page: {pdf_path}")

final_pdf = os.path.join(out_dir, "Tropikos-Brand-Kit.pdf")
with open(final_pdf, "wb") as f:
    writer.write(f)

print(f"COMPLETE: Merged publication-grade PDF written to: {final_pdf}")
