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
`build_assets.py` dele (função `motif()`), não no svgkit. Exemplo de estilo próprio sobre o
esqueleto: `tools/build_banner.py` deste repositório.

## Receitas

- **Contorno legível sobre fundo agitado:** `stroke` + `paint-order="stroke"` atrás do preenchimento.
- **Centralizar na vertical:** `baseline = centro + cap_height(size) / 2`.
- **Forma inclinada (skewX), se o plano pedir:** com `skewX(-a)`, x desloca `-y·tan(a)`. Some `y·tan(a)` ao x de quem fica dentro do grupo inclinado.
- **Foto:** `data_uri("tools/avatar.jpg")` num `<image>` com `clip-path` de retângulo arredondado.
  Baixe o avatar com `curl -L "https://avatars.githubusercontent.com/u/<id>?s=400"`.
- **Ícones de terceiros (skillicons):** baixe o SVG uma vez para `tools/` e embuta com `data_uri`.
- **Símbolo ausente na fonte:** `MissingGlyph` avisa. Desenhe o símbolo (triângulo, seta) como path.

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
