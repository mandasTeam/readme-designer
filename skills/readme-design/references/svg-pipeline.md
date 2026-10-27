# Pipeline de SVG (texto vira path)

## Por que path

O GitHub serve imagens por proxy (camo) e o SVG dentro de `<img>` roda em modo seguro:
sem fonte web, sem imagem externa, sem script. Texto em `<text>` cai na fonte do sistema e
muda de máquina para máquina. A solução: moldar o texto com HarfBuzz (kerning, ligaturas,
acentos) e desenhar cada glifo como `<path>` com fontTools. O resultado sai igual em qualquer lugar.

## Preparar

```
terminal("python -m venv .venv-readme && .venv-readme/Scripts/python -m pip install fonttools uharfbuzz resvg-py pillow")
terminal("python scripts/fetch_fonts.py tools/fonts \"<familia>/<Arquivo>.ttf\" ...")
```

As fontes saem do plano de design do projeto: em geral uma display para títulos e números e
uma legível para o corpo, com 2 ou 3 pesos. Antes de fechar a escolha, confira se a família tem
caixa-baixa, acentos do pt-BR e os símbolos que o texto usa (`MissingGlyph` avisa no build).
Fonte variável (`Arquivo[wght].ttf`) vale um arquivo para todos os pesos: `Font(p, wght=700)`.

## Peças do `svgkit.py`

| Peça | Para quê |
|---|---|
| `Font.path(text, size, x, y, anchor, tracking)` | texto → `d` do path, linha de base em y |
| `Font.width / cap_height / wrap / fit` | medir, centralizar na vertical, quebrar linha, encolher até caber |
| `rich_lines + rich_paths` | parágrafo com trechos em negrito/cor, quebrando só nos espaços |
| `svg(w, h, title, body, style)` | raiz com `<title>` acessível |
| `card_frame(w, h, theme, rx, stroke)` | fundo e borda do card, sem enfeite |
| `heading(text, font, theme)` | título de seção 1200×64 com fundo próprio e régua opcional |
| `pill`, `warning_icon`, `data_uri` | etiqueta com fundo, ⚠ desenhado, imagem em base64 |

O svgkit não tem estilo: são peças estruturais neutras. `Theme` guarda os tokens de cor do
plano (motivo em `extra`), e forma, textura e motivo do projeto são desenhados no
`build_assets.py` dele (função `motif()`), não no svgkit. Exemplo de marca existente aplicada
sobre o svgkit (folha única, glifos reaproveitados, gravura em dithering): `tools/build_banner.py`
deste repositório, que segue o BRAND.md de `mandasTeam/team-docs`.

## Receitas

- **Contorno legível sobre fundo agitado:** `stroke` + `paint-order="stroke"` atrás do preenchimento.
- **Centralizar na vertical:** `baseline = centro + cap_height(size) / 2`.
- **Forma inclinada (skewX), se o plano pedir:** com `skewX(-a)`, x desloca `-y·tan(a)`. Some `y·tan(a)` ao x de quem fica dentro do grupo inclinado.
- **Foto:** `data_uri("tools/avatar.jpg")` num `<image>` com `clip-path` de retângulo arredondado.
  Baixe o avatar com `curl -L "https://avatars.githubusercontent.com/u/<id>?s=400"`.
- **Glifo reaproveitado (`<defs>` + `<use>`):** desenhe cada glifo uma vez em unidades da fonte
  (`<path id="gN">`) e cada ocorrência como `<use href="#gN" x=…>` dentro de
  `<g transform="translate(x,y) scale(size/upem)">`. Um card de 1200×1400 com muito texto caiu
  de 314 KB para 84 KB. Classe pronta em `mandasTeam/team-docs/tools/build_assets.py` (`Glyphs`).
- **Card único:** empilhar `<img>` deixa vãos entre elas; se o usuário quer "um card só", faça
  uma folha única e gere o README pelo script, com o `alt` copiado do `<title>`. Uma `<img>`
  tem um link só: em perfil de org, os repos já aparecem listados abaixo do README.
- **Recortar figura do fundo (gravura em nicho):** `rembg` com `isnet`/`u2net`/`birefnet` falhou em
  hachura densa; `rembg` com `sam` e ~12 pontos positivos + ~7 negativos isolou bem. Una com
  isnet dentro da máscara SAM dilatada, `binary_closing`, `fill_holes` e maior componente.
- **Gravura/foto em dithering (estilo site do Hermes):** `ImageOps.fit` na grade `w//px`, `autocontrast`,
  `quantize(palette=<3 cores do plano>, dither=FLOYDSTEINBERG)`, PNG com `transparency=0, bits=2` e
  `style="image-rendering:pixelated"`. Um busto 300×330 sai com ~25 KB. Dissolva a base compondo um
  gradiente para o branco antes de quantizar. Obra de domínio público (Wikimedia, filtrar por CC0/PD).
- **Figura em dithering sobre motivo (raios, auréola):** no dithering o tom mais claro vira
  transparente (`transparency=0`), então o motivo atrás aparece pelas luzes do corpo. Ponha por
  baixo uma `<image>` da silhueta (alfa do recorte ≥128) chapada na cor do fundo.
- **Estudar site de referência sem navegador:** baixe o HTML e os `.css` com curl e grep nas
  variáveis `--*color*`/`--font*`; as artes `.webp` viram uma folha PNG para `vision_analyze`.
- **Ícones de terceiros (skillicons):** baixe o SVG uma vez para `tools/` e embuta com `data_uri`.
- **Símbolo ausente na fonte:** `MissingGlyph` avisa. Desenhe o símbolo (triângulo, seta) como path.

## Avatar (PNG quadrado)

- 500 × 500, gerado como SVG pelo mesmo build e rasterizado com
  `resvg_py.svg_to_bytes(svg_string=..., width=500, height=500)`; ponha `resvg-py` no `requirements.txt`.
- Sem texto: no GitHub o avatar aparece com 20 a 40 px e o nome já vem ao lado.
- Figura: recorte justo de cabeça e peito, com o rosto grande (~1/4 da largura) e centrado na
  horizontal. O corte lateral fica fora da moldura (a figura sangra) para não aparecer borda reta.
- Dithering com ponto de 2 px, não 1: com 1 px o rosto vira borrão quando o GitHub reduz.
- Estático: PNG não anima, então tire o que só existe para piscar.
- Conferência: folha com o avatar em 500, 260, 96, 40 e 20 px, com cantos arredondados, sobre
  `#ffffff` e `#0d1117`. Pronto quando o rosto e o motivo ainda leem em 40 px.
- Social preview de repo segue a mesma receita em 1280 × 640 (PNG < 1 MB), em Settings → Social preview.

## Tamanho

- `num()` arredonda para 1 casa decimal: corta ~40% do path sem perda visível.
- Referências reais: título 6–10 KB, card de texto 50–200 KB, card com foto 240 KB.
- Passou de 250 KB? Menos texto no card, menos pesos de fonte ou foto menor (200 px bastam).

## Prévia sem navegador

```
terminal("python scripts/contact_sheet.py sheet.png assets/ --pair 'card-*.svg'")
vision_analyze(image_url="sheet.png", question="sobreposição, texto cortado, alinhamento?")
vision_analyze(image_url="sheet.png", region=[0, 0, 1248, 480], question="...")   # zoom num card
```

O resvg desenha o SVG estático: não mostra animação nem `prefers-color-scheme`.
Movimento se confere depois, no perfil publicado.
