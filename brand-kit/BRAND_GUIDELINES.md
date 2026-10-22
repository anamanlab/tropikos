# Trópikos Arquitetos — Manual de Identidade Visual (Brand Guidelines)

> Guia prático de aplicação para estúdio, canteiro de obras, projetos executivos e ambiente digital.

---

## 1. O Logotipo & Conceito

- **Conceito:** A síntese entre o **rigor da arquitetura autoral** (grid ortogonal, estrutura de concreto e precisão técnica) e a **organicidade do clima e relevo tropical** de Recife (curvas de nível topográficas, ventilação cruzada e vegetação litorânea).
- **Estrutura:** O nome **TRÓPIKOS** é estruturado em uma matriz 3×3 que reflete suas três sílabas fonéticas (`TRÓ` · `PI` · `KOS`). A 9ª célula funciona como um **Pátio Topográfico Interno** — uma área aberta de vegetação e relevo, ecoando a tradição modernista brasileira de integrar jardins aos blocos edificados.
- **Versões Oficiais:**
  1. **Master Stacked:** Símbolo 3×3 acompanhado do subtítulo `ARQUITETOS` (aplicação principal para capas de projeto, carimbos e papelaria).
  2. **Horizontal:** Símbolo reduzido à esquerda com `TRÓPIKOS ARQUITETOS` à direita (aplicação ideal para barras de navegação web, cabeçalhos de contrato e assinaturas de e-mail).
  3. **Símbolo Autônomo:** Matriz 3×3 pura (para redes sociais, app icons e botões).
  4. **Favicon / Small-Cut:** Versão com espessuras compensadas e 3 curvas reforçadas para exibição nítida em abas de navegadores (16×16 e 32×32 px).

---

## 2. Área de Proteção (Clear Space)

Mantenha uma margem de respiro mínima ao redor de qualquer versão do logotipo equivalente a **1X**, onde **X** é a largura da haste da letra **T** (ou metade da largura de uma célula do grid):

```
       [  X  ]
  +--------------------+
  |      T R Ó         |
X |      ≈ P I       X |
  |      K O S         |
  |    ARQUITETOS      |
  +--------------------+
       [  X  ]
```

Nenhum elemento tipográfico, foto de obra ou borda de página deve invadir essa zona de segurança.

---

## 3. Dimensões Mínimas de Reprodução

| Versão | Ambiente Digital | Impressão Gráfica / Placa |
|---|---|---|
| **Horizontal** | Mínimo 120 px de largura | Mínimo 30 mm de largura |
| **Stacked (Completo)** | Mínimo 64 px de altura | Mínimo 20 mm de altura |
| **Símbolo 3×3** | Mínimo 24 px de altura | Mínimo 10 mm de altura |
| **Favicon / Web-Icon** | 16 px (utilizar `favicon.svg` ou `favicon.ico`) | — |

---

## 4. Cores Institucionais

| Nome da Cor | HEX | RGB | CMYK | Pantone (Aprox.) | Função no Sistema |
|---|---|---|---|---|---|
| **Onyx (Preto Arquitetura)** | `#191919` | `25, 25, 25` | `70, 65, 65, 80` | Pantone Black 6 C | Tipografia principal, estrutura do grid e linha divisória |
| **Verde Palma (Tropical)** | `#3D6E60` | `61, 110, 96` | `75, 35, 60, 25` | Pantone 5555 C | Curvas de nível do pátio topográfico e acentos botânicos |
| **Barro Cozido (Terracota)** | `#BA5424` | `186, 84, 36` | `18, 78, 98, 8` | Pantone 7584 C | Subtítulo `ARQUITETOS`, metadados e detalhes terrosos |
| **Branco Papel** | `#FFFFFF` | `255, 255, 255` | `0, 0, 0, 0` | — | Fundo do canvas, pranchas técnicas e versão invertida |

### Combinações Aprovadas de Fundo:
- **Fundo Branco / Papel:** Versão colorida oficial (`#191919` + `#3D6E60` + `#BA5424`) ou 100% preta (`#000000`).
- **Fundo Escuro / Onyx (`#191919`):** Versão 100% branca invertida (`tropikos-*-white.svg`).
- **Fotografia de Arquitetura:** Aplicar sobre áreas calmas e uniformes da imagem utilizando a versão branca monocromática.

---

## 5. Tipografia do Sistema

- **Identidade do Logotipo:** Desenhada como curvas vetoriais puras baseadas em proporções neo-grotescas modernistas (homenagem à escola de design paulista e pernambucana).
- **Interface e Textos do Site:**
  - **Display & Textos:** `TWK Everett` (substituto Google Fonts: `Inter`, peso 400).
  - **Dados Técnicos & Legendas:** `TWK Everett Mono` (substituto: `JetBrains Mono`, peso 400).

---

## 6. O que NÃO Fazer (Regras de Uso)

- **Não distorcer:** Nunca achatar ou esticar o logotipo desproporcionalmente.
- **Não alterar as cores:** Não utilize matizes fora da paleta aprovada.
- **Não adicionar efeitos:** É estritamente proibido adicionar sombras projetadas (*drop shadows*), chanfros, gradientes ou contornos ao logotipo.
- **Não rotacionar:** O logotipo deve ser aplicado sempre ortogonalmente (horizontal).
- **Não alterar o grid:** Não modifique a posição das letras nem tente preencher a célula do pátio com outros ícones.
- **Não redigitar:** Nunca tente recriar o logotipo digitando com uma fonte padrão; utilize sempre os arquivos vetoriais mestres em SVG.

---

## 7. Diretório de Arquivos & Entregáveis

- **Vetores Mestres:** `brand-kit/svg/` (Símbolo, Stacked e Horizontal em Colorido, Preto, Branco e Monocromático).
- **Rasters de Alta Definição:** `brand-kit/png/` (PNGs transparentes em 512, 1024 e 1440 px).
- **Ícones Web Prontos:** `brand-kit/web/` e `public/` (Favicon `.ico`, `.svg`, Apple Touch Icon, Android Chrome e Webmanifest).
- **Prancha de Apresentação:** `brand-kit/presentation.html` (com mockups de website, placa de obra, cartão de visita e tote bag).
