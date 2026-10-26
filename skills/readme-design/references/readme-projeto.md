# README de projeto e catálogo de ideias para perfil

## README de projeto

Base: [awesome-readme](https://github.com/matiassingers/awesome-readme). Os bons têm, nesta ordem:

1. **Banner ou logo** com o nome e uma frase do que faz.
2. **2 a 4 badges** que respondem perguntas reais: o CI passa? qual versão? qual licença? Badge decorativo é ruído.
3. **Uma frase** sem adjetivo de marketing: "X faz Y para Z".
4. **Imagem ou GIF curto** do resultado. Mostrar vence explicar.
5. **Instalação** com um comando que funciona copiado e colado.
6. **Uso** com um exemplo mínimo real e a saída esperada.
7. **Como funciona**, só se o leitor precisar para usar ou contribuir: um parágrafo ou um diagrama.
8. **Contribuindo:** testes, padrão de commit, onde abrir issue.
9. **Licença.**

README com mais de ~5 seções ganha sumário e links "voltar ao topo". Corte a seção sem
conteúdo real; nada de "TODO". Modelo: `templates/project-readme.md`.

### Projeto de grupo com repo de referência

Quando o usuário aponta um repo do grupo como modelo, copie a estrutura dele em vez do
template: cabeçalho, ordem das seções, notas fixas e padrão de nome do repo. Leia o README
dele com `gh api repos/O/R/contents/README.md --jq .content | base64 -d`.

- Logo simples: SVG à mão **sem texto** (formas + cores), com fundo próprio para ler nos dois
  temas. Sem texto não precisa do pipeline de fontes/paths. Confira renderizando com
  `resvg_py.svg_to_bytes(svg_path=..., width=360)` e olhando o PNG.
- Conferência sem navegador: `gh api repos/O/R/readme -H "Accept: application/vnd.github.html" | grep -o '<img[^>]*>'`
  lista o que o GitHub vai renderizar; teste cada URL com `curl -s -o /dev/null -w '%{http_code} %{content_type}'`.
- README que é relatório (trabalho acadêmico): seções com os nomes exatos do enunciado e um
  marcador `<!-- RESPONSÁVEL: @login · tarefa -->` por seção, para cada integrante preencher a
  sua no próprio PR.

## Revisão de documentação de projeto (modo convencional)

Pedido típico: "verifique atualizações necessárias para a documentação do repo X". A
entrega é um PR com as correções, não uma lista de sugestões.

1. **Estado do repo:** `git fetch`, `git status -sb`, `git log --oneline -15`; leia README,
   `CLAUDE.md`/`AGENTS.md` e liste `docs/`. As convenções de escrita do repo (marcador de lista,
   idioma, branch `docs/<slug>`, template de PR) mandam sobre o gosto da skill.
2. **Cada afirmação contra o código**, não contra outro documento:
   - comandos citados vs. `scripts` do `package.json` (ex.: `npm test` pode rodar só unitários);
   - passos de execução vs. `docker-compose*.yml`, `Dockerfile`, `index.js`/boot e scripts de
     migration (o boot ainda cria tabela? o compose roda migration?);
   - arquivo citado ainda existe? `git ls-files | grep <nome>` e `git log -1 -- <caminho>`
     dizem quando saiu;
   - números (cobertura, contagens) vs. o relatório de medição mais recente: número de baseline
     apresentado como atual é o erro mais comum;
   - pendências listadas vs. estado das issues (`gh issue view N --json state`);
   - regras de processo ("merge exige CI verde/aprovação do QA") vs. a proteção real:
     `gh api repos/O/R/branches/main/protection` e `gh api repos/O/R/rulesets`.
3. **Links relativos mortos:** varra todos os `.md` resolvendo cada `](caminho)` relativo ao
   arquivo e testando `os.path.exists`. Ignore specs/templates cujo link é exemplo para um
   documento futuro. Link para entregável ainda não feito vira referência à issue que o entrega.
   URLs externas: `scripts/check_urls.py README.md`.
4. **Pessoas e contas:** confira login de integrante contra `collaborators`, `CODEOWNERS` e
   autores de PR (`gh pr list --state merged --json author`). Se divergir das notas do usuário,
   **não troque sozinho**: trocar o link sem trocar acesso e CODEOWNERS deixa o repo incoerente.
   Reporte como decisão.
5. **Editar com Python** (`str.replace` com `assert count == 1`, gravando com `newline='\n'`),
   um commit por documento, Conventional Commits no padrão do repo.
6. **Rodar o que der** dos comandos documentados (lint, testes unitários) antes de afirmar que
   funcionam; o que exigir Docker/banco fica para a CI do PR.
7. **PR** com o template do repo; aguarde `gh pr checks`; confira o render com
   `gh api repos/O/R/readme?ref=<branch> -H "Accept: application/vnd.github.html"`.
8. **Relatório:** o que foi corrigido, o que foi verificado e como, e as decisões que ficaram com
   o usuário (divergência de configuração, conta de integrante, links que dependem de entregas
   abertas). Configuração (proteção de branch, acesso) não se muda numa revisão de docs.

## Catálogo para perfil

Base: [awesome-github-profile-readme](https://github.com/abhisheknaiidu/awesome-github-profile-readme)
e [10 standout profile READMEs](https://dev.to/github/10-standout-github-profile-readmes-h2o).
Escolha **poucos** e no tema. Isto é um cardápio, não uma lista de tarefas.

| Ideia | Custo | Observação |
|---|---|---|
| Banner próprio em SVG | médio | o momento memorável do perfil |
| Texto digitando | baixo | 3 a 5 linhas, uma pode ser a piada recorrente |
| Ficha/dossiê com foto | médio | substitui a tabela "sobre mim" |
| Cards de projeto (pares a 49%) | médio | creditar só a parte da pessoa |
| Stats + streak tematizados | baixo | parâmetros de cor na URL |
| Cobrinha no gráfico de contribuição | baixo | workflow + `<picture>` claro/escuro |
| Contador de visitas próprio | médio | pixel komarev + card gerado |
| Posts de blog automáticos | médio | `gautamkrishnar/blog-post-workflow`, só se a pessoa escreve |
| Jogo por issues (xadrez, connect4) | alto | só se a pessoa pedir |
| Spotify "tocando agora" | alto | precisa de deploy serverless |
