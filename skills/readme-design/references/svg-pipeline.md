# Pipeline de SVG (texto vira path)

## Por que path

O GitHub serve imagens por proxy (camo) e o SVG dentro de `<img>` roda em modo seguro:
sem fonte web, sem imagem externa, sem script. Texto em `<text>` cai na fonte do sistema e
muda de máquina para máquina. A solução: moldar o texto com HarfBuzz (kerning, ligaturas,
acentos) e desenhar cada glifo como `<path>` com fontTools. O resultado sai igual em qualquer lugar.

## Preparar

```
terminal("python -m venv .venv-readme && .venv-readme/Scripts/python -m pip install fonttools uharfbuzz resvg-py pillow")
terminal("python scripts/fetch_fonts.py tools/fonts bangers/Bangers-Regular.ttf barlowcondensed/BarlowCondensed-SemiBold.ttf barlowcondensed/BarlowCondensed-Bold.ttf")
```

Combinação que funciona: uma fonte display de personalidade (títulos e números) e uma
condensada legível para o corpo, com 2 ou 3 pesos. Bangers só tem caixa-alta.

## Peças do `svgkit.py`

| Peça | Para quê |
|---|---|
| `Font.path(text, size, x, y, anchor, tracking)` | texto → `d` do path, linha de base em y |
| `Font.width / cap_height / wrap / fit` | medir, centralizar na vertical, quebrar linha, encolher até caber |
| `rich_lines + rich_paths` | parágrafo com trechos em negrito/cor, quebrando só nos espaços |
| `svg(w, h, title, body, style)` | raiz com `<title>` acessível |
| `card_frame(w, h, theme)` | fundo, borda, retícula no canto, faixa de cores do tema |
| `heading(text, display, theme)` | título de seção 1200×72 (caixa inclinada + régua) |
| `chip`, `balloon`, `warning_icon`, `halftone`, `data_uri` | legenda inclinada, balão de fala sem emenda, ⚠ desenhado, retícula, base64 |

`Theme` concentra as cores do plano. Trocar o tema é trocar um objeto, não caçar hex no código.

## Receitas

- **Contorno legível sobre fundo agitado:** `stroke` + `paint-order="stroke"` + uma cópia
  deslocada (5–6 px) em cor escura atrás, que vira sombra sólida de HQ.
- **Centralizar na vertical:** `baseline = centro + cap_height(size) / 2`.
- **skewX:** com `skewX(-12)`, x desloca `-y·tan(12°)`. Some `y·0,2126` ao x de quem fica dentro do grupo inclinado.
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
terminal("python scripts/contact_sheet.py sheet.png assets/ --pair 'mission-*.svg'")
vision_analyze(image_url="sheet.png", question="sobreposição, texto cortado, alinhamento?")
vision_analyze(image_url="sheet.png", region=[0, 0, 1248, 480], question="...")   # zoom num card
```

O resvg desenha o SVG estático: não mostra animação nem `prefers-color-scheme`.
Movimento se confere depois, no perfil publicado.
