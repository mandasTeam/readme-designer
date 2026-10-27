---
name: readme-design
description: "Use ao criar, redesenhar ou revisar README de perfil ou de projeto no GitHub, ou a arte de perfil (avatar, social preview). Audita os fatos, planeja o design, gera a arte em SVG próprio e confere o resultado renderizado, gastando poucos tokens."
version: 1.0.0
author: Igor Seberino (igorSeberino)
license: MIT
metadata:
  hermes:
    tags: [github, readme, profile, svg, design, tokens]
    related_skills: [github]
---

# README design

Responda em pt-BR, direto. Entregue README publicado e conferido, não um rascunho.

O README sai como uma pilha de cards SVG gerados por script. Só stats, streak,
cobrinha e visitas continuam vivos, e esses vêm de serviços ou de um workflow.
A identidade visual vem de um plano de design curto, nunca de template.

## Quando usar

- Criar, redesenhar ou "deixar mais bonito" um README de perfil (`<user>/<user>`) ou de projeto.
- Tematizar um perfil (personagem, franquia, empresa) ou trocar widgets por versões no tema.
- Revisar um README existente: fatos velhos, links mortos, visual inconsistente.
- Arte de perfil fora do README: avatar de usuário/org, social preview de repo (1280×640). Receita em `references/svg-pipeline.md` ("Avatar").
- Revisar a documentação de um repo de projeto em **modo convencional** (markdown puro, sem SVG): siga o roteiro "Revisão de documentação de projeto" em `references/readme-projeto.md` e pule os passos 3 e 4.

## Escolher o modo antes de começar

- **Perfil** (`<user>/<user>`) ou pedido explícito de visual: fluxo completo abaixo, com tema e cards SVG.
- **Repo de projeto** (código, trabalho de grupo, produto): README convencional e explicativo, em markdown cru. Sem tema de fã, sem cards SVG, sem banner. No máximo um badge que responda uma pergunta real (CI). O tema pessoal do perfil **nunca** vaza para repo de projeto.

- **Pedido vago de "capa"/"arte" de perfil ou org:** antes de desenhar, cheque o que falta (`gh api orgs/<org> --jq .avatar_url` e veja se é identicon; `gh api graphql` com `usesCustomOpenGraphImage` por repo; README já tem card?) e faça **um** `clarify` com as opções concretas (avatar 500×500, social preview 1280×640, banner do README). Cada uma tem formato e restrição diferente; chutar errado joga o trabalho fora.
- **Já existe direção de arte** (ex.: `BRAND.md` em `team-docs`): ela manda, inclusive no README de um repo do próprio time (ex.: o desta skill) — pedido de "README estilizado" ali segue a marca, não o modo projeto nem o template neutro. Reaproveite tokens e funções do gerador existente (`plate`, `rays`, `dither`, `Glyphs`…) em vez de copiar o template da skill; copie fontes e figura para o repo para o CI gerar sem depender do outro; e atualize o documento da marca citando a peça nova como exemplo.

Não use para: operações gerais de PR, issue ou release (skill `github`), nem para site ou app (CSS/JS de verdade).

## Pré-requisitos

- `gh` autenticado. Editar bio, empresa ou redes sociais exige o escopo `user`: rode `gh auth refresh -h github.com -s user` em background e passe o código do device flow ao usuário.
- Python ≥ 3.11 num venv de rascunho com `pip install fonttools uharfbuzz resvg-py pillow`. Só `fonttools` e `uharfbuzz` vão para o `tools/requirements.txt` do repo do usuário.
- Fontes OFL baixadas com `scripts/fetch_fonts.py` e commitadas em `tools/fonts/`, junto com as licenças.

## Fluxo

Cada passo só termina quando o critério de pronto estiver cumprido.

1. **Auditar os fatos.** Rode `terminal("python scripts/audit_profile.py <user> --contrib <repo-de-grupo>")`. É uma chamada só, com saída curta.
   - Pronto quando houver uma lista de fatos confirmados, links mortos, vazamentos de privacidade e o crédito real de cada projeto. Detalhes em `references/auditoria.md`.
2. **Perguntar uma vez.** Faça um `clarify` com até 5 perguntas em lote: contatos, cargo real vs. título, formação, projetos em destaque, toques pessoais e permissão para editar a bio.
   - Pronto quando cada lacuna da auditoria tiver resposta ou decisão sua registrada.
3. **Planejar o design** antes de qualquer SVG. Escreva um plano de ~10 linhas:
   - 4 a 6 cores nomeadas;
   - 2 fontes, cada uma com seu papel;
   - grade de 1200/600 px;
   - um motivo visual que se repete;
   - a regra de movimento.

   Depois revise o plano contra a lista de clichês (`references/design.md`).
   - Pronto quando o plano estiver escrito e cada escolha tiver motivo ligado ao tema.
4. **Gerar a arte.** Copie `templates/build_assets.py` para `<repo>/tools/` e `scripts/svgkit.py` junto. Preencha o `CONFIG` com os tokens do plano, desenhe o motivo em `motif()` e rode o script. O template e o `svgkit` são estrutura neutra: o estilo é sempre do projeto, nunca um padrão da skill.
   - Pronto quando o build rodar sem `MissingGlyph` e cada SVG tiver < 250 KB. Receita em `references/svg-pipeline.md`.
5. **Montar o README** a partir de `templates/profile-readme.md` ou `templates/project-readme.md`. Para widgets vivos, copie `templates/widgets-workflow.yml` (detalhes em `references/widgets.md`).
   - Pronto quando todo `<img>` tiver `alt` com o texto inteiro do card e não sobrar `##` solto, porque o título também é SVG.
6. **Conferir e publicar.**
   - `terminal("python scripts/contact_sheet.py sheet.png assets/ --pair 'card-*.svg'")` e depois `vision_analyze`, recortando por região onde houver texto pequeno.
   - `python scripts/check_urls.py README.md`.
   - Push com Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `ci:`).
   - Abra `github.com/<user>` e confirme que todo `article img` tem `naturalWidth > 0`. Sem navegador, confira pelo HTML que o GitHub renderiza: `gh api repos/<owner>/<repo>/readme -H "Accept: application/vnd.github.html"`, extraia cada `src` de `<img>`, faça `curl -sL` em cada um (200 e `image/svg+xml`; caminho relativo vira `github.com/<owner>/<repo>/raw/main/<src>`) e `cmp` do SVG baixado com o local.
   - Confirme a última execução do workflow com `gh run view` e a branch `output` com os arquivos.
   - Pronto quando tudo isso passar. Só então reporte.

## Economia de tokens

Cada regra corta custo sem cortar verificação. O detalhe está em `references/tokens.md`.

- **Filtrar antes de ler:** scripts e `--jq` imprimem só o que decide algo. Nunca despeje JSON cru da API.
- **Nunca ler SVG gerado.** São 50 a 250 KB de paths e base64. Confira pelo PNG da folha de conferência.
- **Uma imagem, várias regiões:** uma folha de conferência e recortes com `region`, em vez de um screenshot por card.
- **Lotes:** chamadas independentes no mesmo turno e um `clarify` com todas as perguntas.
- **Mudar o gerador, não o SVG:** ajuste o `CONFIG` e rode de novo. Para trocar um trecho de texto, use `patch` em vez de reescrever.
- **Fazer só o pedido:** nenhum widget, serviço ou seção que o usuário não pediu. Reaproveite o `svgkit`.
- **Relatório curto:** o que mudou, o que foi conferido, o que ficou pendente. Comandos, caminhos e commits vão intactos.
- **Nunca economizar em:** `alt`, `prefers-reduced-motion`, conferência renderizada e checagem de fatos.

## Design em uma tela

O detalhe está em `references/design.md`.

- O tema vem do assunto: avatar, personagem, setor, vocabulário visual. Tire a paleta da imagem real com visão.
- Use uma linguagem visual em tudo: títulos, texto, contato e contador viram cards no mesmo padrão. Se o usuário reclamar de uma seção, refaça no mesmo passe todas as que ainda estão "cruas".
- Concentre a ousadia num lugar só, o banner. O resto fica disciplinado. Antes de publicar, tire um acessório.
- Hierarquia em todo card: rótulo pequeno na cor de acento, valor claro e maior, apoio em cinza.
- O card precisa ler bem no tema claro e no escuro do GitHub: tenha fundo próprio e confira nos dois.
- Movimento só sutil: pulsar, piscar, onda. Objeto cruzando a tela é vetado. Sempre inclua `prefers-reduced-motion`.
- Copy em frase normal, verbo simples, cada elemento com uma função só. Nada de piada forçada.

## Armadilhas

- **SVG em `<img>` roda em sandbox.** Fonte web e imagem externa não carregam: converta texto em path e imagem em base64. Avatar embutido não acompanha troca de foto, então avise o usuário.
- **Fontes sem glifo:** ▸ ✓ ⚠ ✉ e emojis costumam faltar. Desenhe o símbolo como path (`svgkit.warning_icon`).
- **Serviço gratuito cai.** Confira cada widget com `check_urls.py` antes de usar. Em out/2026, `github-profile-trophy.vercel.app` respondia 402.
- **O `snk` deixa `dist/` como root.** Rode os geradores Python antes dele no workflow.
- **Escrita bloqueada no Hermes:** `write_file` recusa sobrescrever arquivo lido só em parte. Apague o arquivo e escreva de novo, ou edite via Python. Em arquivo com CRLF o `patch` erra: normalize `\r\n`, edite e restaure.
- **Sequência de escape em literal Python vira quebra de linha real** quando passa por `patch` ou heredoc+`replace`, e o gerador para com `SyntaxError`. Edite essas linhas com um script `.py` que monta a barra com `chr(92)`, e confira com `grep -n` antes de rodar.
- **Chrome headless pode não abrir** no Windows. Para conferir a arte, `resvg-py` (folha de conferência) dispensa navegador; para o publicado, use a checagem por `gh api … vnd.github.html` do passo 6.
- **Perfil de organização** fica em `<org>/.github/profile/README.md`; imagens com `../assets/x.svg` resolvem para `github.com/<org>/.github/raw/main/assets/x.svg` (conferido).
- **Peça nova entra no gerador existente, não num script irmão.** Geradores costumam limpar `assets/*.svg` antes de escrever, e apagam a saída do outro script. Acrescente a função e o arquivo ao `main()` do mesmo build e rode tudo para confirmar que as peças antigas saíram idênticas (`git status` limpo nelas).
- **Avatar de organização não muda por API.** Gere o PNG, commite e passe o roteiro: `github.com/organizations/<org>/settings/profile` → Profile picture → Edit → Upload a photo. Só faça pelo navegador se houver login salvo no cofre.
- **README em folha única é só a folha.** Nada embaixo: nem `<details>` com comandos ou referências, nem linha de selo/licença. O Igor chamou isso de lixo. Comando, instalação e licença vão dentro do card; o `alt` sai do `<title>` pelo script.
- **`alt` com URL ou `<>` vaza texto no GitHub.** O sanitizador corta o atributo e o resto aparece como texto embaixo da imagem. Em card grande, o `alt` é um resumo sem URL nem `<>`. Antes do push, renderize com `gh api markdown -f mode=gfm -f text="$(cat README.md)"` e confira que não sobra texto visível.
- **`Path.write_text` no Windows grava CRLF.** Em gerador que escreve README ou SVG, passe `newline` com LF (barra-n); ao reler para substituir, normalize CRLF antes do `re.sub`.
- **LinkedIn responde 999 a robôs.** Não dá para verificar; pergunte ao usuário.

## Referências (carregue só no passo que pede)

| Arquivo | Quando |
|---|---|
| `references/auditoria.md` | passo 1: o que conferir e como |
| `references/design.md` | passo 3: plano, clichês, hierarquia, acessibilidade, copy |
| `references/svg-pipeline.md` | passo 4: texto em path, peças do svgkit, tamanho, prévia, avatar em PNG |
| `references/widgets.md` | passo 5: stats, streak, cobrinha, visitas, branch `output` |
| `references/readme-projeto.md` | README de projeto, revisão de docs de repo contra o código, catálogo de ideias para perfil |
| `references/tokens.md` | economia de tokens em detalhe |
| `references/preferencias-igor.md` | sempre que o usuário for o Igor (ponto de partida, não receita) |
