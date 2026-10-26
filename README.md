<p align="center">
  <img src="assets/banner.svg" width="100%" alt="README DESIGN — skill para agentes. README de perfil e de projeto com cara de design, não de template. Fatos conferidos, arte em SVG próprio, poucos tokens.">
</p>

<p align="center">
  <a href="https://github.com/igorSeberino/readme-design-skill/actions/workflows/ci.yml"><img src="https://github.com/igorSeberino/readme-design-skill/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/github/license/igorSeberino/readme-design-skill" alt="Licença MIT">
</p>

**readme-design** é uma skill no formato `SKILL.md` (Agent Skills) que ensina um agente de código a
criar e redesenhar READMEs do GitHub. O agente confere os fatos antes de escrever, define um plano
de design, gera a arte em SVG com texto convertido em path e confere o resultado renderizado antes de dizer que terminou.

Exemplo real feito com ela: [github.com/igorSeberino](https://github.com/igorSeberino) (tema Robin / Teen Titans).

<img src="assets/h-fluxo.svg" width="100%" alt="Como funciona">

1. **Auditoria.** `audit_profile.py` junta perfil, repos, fixados, links mortos e telefone exposto numa saída curta.
2. **Uma rodada de perguntas.** Tudo o que a auditoria não resolve vai num lote só.
3. **Plano de design.** Cores, fontes, grade, motivo e movimento, revisados contra os clichês de design gerado.
4. **Arte em SVG.** `svgkit.py` molda o texto com HarfBuzz e desenha cada glifo como path, porque o GitHub não carrega fonte dentro de `<img>`.
5. **README e widgets.** Esqueletos de perfil e de projeto; stats, cobrinha e visitas no tema via workflow numa branch `output`.
6. **Conferência.** Folha PNG em fundo escuro e claro para inspecionar com visão, checagem de URLs, imagens carregadas no perfil publicado e execução do workflow.

A skill também traz regras de **economia de tokens**: filtrar a saída antes de ela entrar no
contexto, nunca ler SVG gerado, conferir tudo com uma imagem só, fazer perguntas em lote e
mandar relatório curto. Nada disso corta a verificação.

<img src="assets/h-instalar.svg" width="100%" alt="Instalação">

```bash
git clone https://github.com/igorSeberino/readme-design-skill.git
```

| Agente | Como instalar |
|---|---|
| Hermes Agent | adicione `<clone>/skills` em `skills.external_dirs` no `config.yaml` |
| Claude Code | `cp -r readme-design-skill/skills/readme-design ~/.claude/skills/` |
| Outros com suporte a `SKILL.md` | copie `skills/readme-design/` para a pasta de skills do agente |

Os scripts precisam de Python 3.11+:

```bash
python -m pip install -r requirements-dev.txt   # fonttools, uharfbuzz, resvg-py, pillow, pytest
```

<img src="assets/h-estrutura.svg" width="100%" alt="Estrutura">

```text
skills/readme-design/
├── SKILL.md                 fluxo, regras de tokens e de design, armadilhas
├── references/              carregadas só no passo que pede
│   ├── auditoria.md         o que conferir antes de desenhar
│   ├── design.md            plano em duas passadas, clichês, hierarquia, acessibilidade, copy
│   ├── svg-pipeline.md      texto em path, peças do svgkit, tamanho, prévia
│   ├── widgets.md           stats, streak, cobrinha, visitas, branch output
│   ├── readme-projeto.md    anatomia de README de projeto e cardápio para perfil
│   ├── tokens.md            onde o gasto aparece e o que trocar
│   └── preferencias-igor.md gosto geral do dono (ponto de partida)
├── scripts/                 svgkit, audit_profile, check_urls, contact_sheet, visits, fetch_fonts
└── templates/               build_assets.py, profile-readme.md, project-readme.md, widgets-workflow.yml
tests/                       pytest sem rede (svgkit, URLs, contador, template)
tools/build_banner.py        gera a arte deste README com o próprio template
```

Para desenvolver: `python -m pytest -q` e `python tools/build_banner.py`. Commits seguem
Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `ci:`, `chore:`).

### Referências

Design: [frontend-design](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md),
[agent-skills](https://github.com/vercel-labs/agent-skills),
[ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill).
Tokens: [rtk](https://github.com/rtk-ai/rtk), [caveman](https://github.com/juliusbrussee/caveman),
[caveman output style](https://github.com/carlosduplar/caveman-output-style-claude-code),
[ponytail](https://skillsllm.com/skill/ponytail), [Claude-Skills](https://github.com/valorisa/Claude-Skills).
READMEs: [awesome-readme](https://github.com/matiassingers/awesome-readme),
[awesome-github-profile-readme](https://github.com/abhisheknaiidu/awesome-github-profile-readme),
[10 standout profile READMEs](https://dev.to/github/10-standout-github-profile-readmes-h2o).

### Licença

MIT, veja [LICENSE](LICENSE). As fontes em `tools/fonts/` (Bangers, Barlow Condensed) seguem a SIL Open Font License; os textos estão ao lado delas.
