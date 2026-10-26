# Design de README

Base: [frontend-design](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md)
(plano em duas passadas, contenção, clichês), [web-design-guidelines](https://github.com/vercel-labs/agent-skills)
(acessibilidade, movimento) e [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
(sistema de design como tokens), adaptados ao que o GitHub permite: HTML sanitizado,
sem CSS de página, sem JS, e SVG em `<img>` dentro de sandbox.

## 1. Fundamentar no assunto

O tema sai do mundo da pessoa: o personagem do avatar, o setor, o vocabulário visual.
Use `vision_analyze` no avatar para tirar a paleta real. Liste 3 a 5 elementos desse mundo
que viram forma. Cada elemento precisa responder:

- que tipografia, textura ou recurso gráfico é típico desse mundo;
- que cores dele viram um motivo que se repete em todos os cards;
- que objetos dele viram metáfora de seção (stack, contato, estatísticas), se couber sem forçar.

## 2. Plano em duas passadas

**Passada 1:** escreva os tokens antes de codar.

```
Cor:       fundo · card · texto · acento · cores do motivo (hex, com nome e papel)
Tipo:      display <fonte> (títulos, números) · corpo <fonte> <pesos>
Grade:     cards 1200 de largura (600 para pares a 49%), raio, forma dos chips
Motivo:    o elemento do tema que se repete em todo card
Movimento: um gesto por card (pulsar, piscar, onda); reduced-motion desliga tudo
Princípio: uma frase que diz o que o perfil parece e o que ele não parece
```

**Passada 2:** revise contra os padrões que denunciam design gerado. Eles são escolha
legítima **só** quando o tema pede.

- Fundo creme com serifa e acento terracota; ou preto com um único verde-ácido.
- Tudo em cards idênticos, mesmo raio em tudo, a mesma sombra cinza suave, gradiente de enfeite.
- Rótulo em CAIXA-ALTA espaçada acima de cada título; metadados ligados por " · "; "→" no fim de link.
- Numeração 01/02/03 em conteúdo que não é sequência.
- Destacar uma palavra só no título com cor ou itálico.

O briefing vence: se o tema pede um desses padrões, ele **é** o vocabulário. Use e diga por quê.
Fora disso, troque cada padrão que você usaria em qualquer perfil por uma escolha do tema.

## 3. Hierarquia dentro do card

| Nível | Fonte | Cor | Tamanho na origem (1200 px) |
|---|---|---|---|
| Rótulo | corpo bold, tracking 2 | acento ou cor da faixa | 15–18 |
| Valor | corpo semibold | texto claro | 26–30 (use `fit()` para caber) |
| Apoio | corpo regular | cinza (muted) | 18–22 |
| Título do card | display | branco ou acento | 32–58 |

No desktop, o GitHub exibe 1200 px em ~830 px (escala 0,69). Abaixo de 15 px na origem fica ilegível.

## 4. Composição

- **Ousadia num lugar só.** O banner é o momento memorável; os cards seguem o motivo, quietos.
- **Uma linguagem.** Título de seção, texto corrido, ficha, stack, contato e contador: tudo SVG
  no mesmo motivo. Tabela markdown, `##` e selo padrão destoam e a pessoa percebe.
- **Pares lado a lado:** dois cards de 600 px com `width="49%"` no mesmo `<p align="center">`.
- **Tema claro e escuro:** cards com fundo próprio. Elemento transparente (balão, título) precisa
  de contorno forte. Confira sobre `#0d1117` e sobre `#ffffff`.
- **Widgets externos** recebem as cores dos tokens nos parâmetros da URL (`bg_color`, `title_color`…).
- **Tire um acessório:** antes de publicar, remova o enfeite que não informa nada.

## 5. Movimento

- CSS `@keyframes` e SMIL funcionam dentro do SVG em `<img>`. Use pouco: pulsar o emblema,
  estrelas piscando, LED, ondas de sinal.
- Objeto atravessando o banner distrai e compete com o texto. Evite por padrão.
- Inclua sempre `@media (prefers-reduced-motion:reduce){*{animation:none!important}}` (`svgkit.REDUCED_MOTION`).

## 6. Acessibilidade

- `alt` do `<img>` com o **texto inteiro** do card. Para leitor de tela e busca, o card é só esse texto.
- `<title>` dentro do SVG com o mesmo resumo (`svgkit.svg()` já faz).
- Nunca passe informação só pela cor. Rótulo escrito sempre.
- Contraste de texto ≥ 4,5:1 contra o fundo do card.

## 7. Copy

- Frase normal, verbo simples, uma função por elemento. Fale do jeito que a pessoa fala.
- Nada de piada forçada nem aparte de tiozão ("leia-se: …", "sem medo de …").
  Uma piada recorrente escolhida pela pessoa já basta.
- Sem disclaimer de rodapé ("X é marca de…", "feito com…") se ninguém pediu.
- README de quem já está empregado não é currículo: cargo e stack na frente, formação em uma
  linha, sem certificações nem telefone.
- Marca de terceiros: desenhe silhueta e emblema próprios. Nunca use arte oficial.

## 8. Crítica

Folha de conferência → lista de problemas concretos (sobreposição, texto cortado, desalinhamento,
contraste) → corrigir no gerador → nova folha. Pare quando a lista estiver vazia, não quando "parecer ok".
