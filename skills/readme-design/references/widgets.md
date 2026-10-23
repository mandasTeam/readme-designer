# Widgets vivos e a branch `output`

## Serviços externos (continuam dinâmicos)

Antes de usar qualquer um: `python scripts/check_urls.py --url "<url>"` precisa dar `ok`
(HTTP 200 e `image/*`). Serviços gratuitos caem sem aviso.

| Widget | URL base | Tematizar com |
|---|---|---|
| Stats | `github-readme-stats.vercel.app/api?username=U&show_icons=true&include_all_commits=true&count_private=true&locale=pt-br` | `bg_color title_color icon_color text_color border_color border_radius custom_title` |
| Linguagens | `github-readme-stats.vercel.app/api/top-langs/?username=U` | mesmos parâmetros |
| Streak | `streak-stats.demolab.com?user=U&locale=pt_BR` | `background border stroke ring fire currStreakNum sideNums currStreakLabel sideLabels dates border_radius` |
| Texto digitando | `readme-typing-svg.demolab.com?font=<GoogleFont>&center=true&lines=a;b;c` | `color size duration pause`. Roda fora da sandbox, então aceita fonte web |
| Ícones de stack | `skillicons.dev/icons?i=py,js,react&perline=8&theme=dark` | baixe e embuta num card próprio |
| Troféus | `github-profile-trophy.vercel.app` | **402 em out/2026, evite** |

Esses serviços não aceitam fonte nem layout próprios. Se o usuário reclamar que não combinam,
gere a versão própria no workflow (como o contador de visitas abaixo).

## Workflow único publicando em `output`

Modelo: `templates/widgets-workflow.yml`.

- Gatilhos: cron a cada 6 h, `workflow_dispatch`, push na `main`.
- `permissions: contents: write` e um grupo de `concurrency`.
- Ordem: checkout → setup-python → `pip install -r tools/requirements.txt` → **geradores Python** →
  `Platane/snk@v3` → `crazy-max/ghaction-github-pages@v5` (`target_branch: output`, `build_dir: dist`).
- O snk roda em container e deixa `dist/` como root. Gerador Python depois dele falha com `PermissionError`.
- Confira as majors atuais: `git ls-remote --tags https://github.com/<owner>/<action>`.

No README, a cobrinha usa `<picture>` com `prefers-color-scheme` apontando para
`raw.githubusercontent.com/U/U/output/snake-dark.svg` e `-light.svg`. Paleta de `color_dots`
com 5 tons do tema, do vazio ao mais forte.

## Contador de visitas no tema

O selo do komarev.com não aceita estilo. Por isso:

1. O README carrega um pixel que conta: `<img src="https://komarev.com/ghpvc/?username=U&style=flat" width="1" height="1" alt="">`.
2. O README mostra o card próprio: `<img src="https://raw.githubusercontent.com/U/U/output/visits.svg">`.
3. `scripts/visits.py` (no workflow) lê o total do komarev pelo último `<text>`, soma +1 em `bot_hits`
   (a própria leitura conta uma visita), mostra `raw - bot_hits` e grava `visits.svg` + `visits.json`.
   O estado anterior vem de `git fetch --depth=1 origin output && git show FETCH_HEAD:visits.json`.
4. Teste local com `--count N`: sem rede e sem inflar o contador.

Avise o usuário: o número atualiza na cadência do cron, não a cada visita.

## Stats e sequência próprios

Quando os cards de serviço destoam do tema, gere os dois no mesmo script do contador:

- Uma consulta GraphQL com os totais (`pullRequests`, `issues`, `repositories{nodes{stargazerCount}}`,
  `repositoriesContributedTo`) e outra com um alias por ano (`y2025: contributionsCollection(from,to)`),
  porque cada `contributionsCollection` cobre no máximo 1 ano.
- Some `totalCommitContributions` e junte os `contributionDays` para calcular a sequência. Hoje com 0
  ainda não quebra a sequência atual.
- No Actions, `GH_TOKEN: ${{ github.token }}` basta e devolve só números públicos, que batem com
  github-readme-stats e streak-stats. Token pessoal local soma privados: não compare com ele.
- Selo que precisa de link próprio (e-mail) vira imagem separada. Para alturas iguais lado a lado,
  `width` em % proporcional à largura do viewBox (780 e 400 px → 65% e 33%).

## Conferir depois do push

```
terminal("gh run list -R U/U --limit 1")                     # concluiu com success?
terminal("gh api 'repos/U/U/contents?ref=output' --jq '.[].name'")
```

No perfil publicado, `[...document.querySelectorAll('article img')].filter(i => !i.naturalWidth)` precisa voltar vazio.
