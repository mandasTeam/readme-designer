<p align="center">
  <img src="assets/readme-designer.svg" width="100%" alt="readme-designer, mandasTeam/readme-designer. README do GitHub com design próprio. Skill no formato SKILL.md que ensina o agente a criar e redesenhar README de perfil e de projeto. Ele confere os fatos, planeja o design, gera a arte em SVG e confere o resultado renderizado antes de dizer que terminou. O que entrega: fatos conferidos na API do GitHub; arte em SVG com texto em path; poucos tokens, sem cortar a conferência. Como funciona: I. Auditoria: audit_profile.py junta perfil, repos, fixados, links mortos e telefone exposto numa saída curta. II. Perguntas: O que a auditoria não resolve vai num lote só, com até cinco perguntas. III. Plano: Cores, fontes, grade, motivo e movimento tirados do assunto e revisados contra os clichês. IV. Arte: svgkit molda o texto com HarfBuzz e desenha cada glifo como path, porque o GitHub não carrega fonte em &lt;img>. V. README: Esqueletos de perfil e de projeto. Stats, cobrinha e visitas no tema, por workflow. VI. Conferência: Folha PNG em fundo claro e escuro, URLs checadas, imagens carregadas e workflow rodado. Poucos tokens: filtrar a saída antes de ela entrar no contexto; nunca ler SVG gerado; conferir tudo com uma imagem só; fazer as perguntas em lote; mandar relatório curto. Nada disso corta a verificação. Instalação: git clone https://github.com/mandasTeam/readme-designer.git. Hermes Agent: adicione &lt;clone>/skills em skills.external_dirs no config.yaml. Claude Code: cp -r readme-designer/skills/readme-design ~/.claude/skills/. Outros agentes: copie skills/readme-design/ para a pasta de skills do agente. Os scripts pedem Python 3.11+: python -m pip install -r requirements-dev.txt. Estrutura: skills/readme-design/; SKILL.md (fluxo, regras de tokens e de design, armadilhas); references/ (carregadas só no passo que pede); auditoria.md (o que conferir antes de desenhar); design.md (plano, clichês, hierarquia, acessibilidade, copy); svg-pipeline.md (texto em path, peças do svgkit, avatar); widgets.md (stats, streak, cobrinha, visitas); readme-projeto.md (README de projeto e revisão de docs); tokens.md (onde o gasto aparece e o que trocar); preferencias-igor.md (gosto geral do dono); scripts/ (svgkit, audit_profile, check_urls, contact_sheet, visits); templates/ (build_assets.py, esqueletos de README, workflow); tests/ (pytest sem rede); tools/build_banner.py (gera esta folha). Para desenvolver: python -m pytest -q &amp;&amp; python tools/build_banner.py. MIT · fontes OFL em tools/fonts. direção de arte: mandasTeam/team-docs.">
</p>

<details>
<summary><b>Comandos para copiar</b></summary>

```bash
git clone https://github.com/mandasTeam/readme-designer.git
cp -r readme-designer/skills/readme-design ~/.claude/skills/   # Claude Code
python -m pip install -r requirements-dev.txt                  # scripts: Python 3.11+
python -m pytest -q && python tools/build_banner.py             # desenvolver
```

No Hermes Agent, adicione `<clone>/skills` em `skills.external_dirs` no `config.yaml`.
Commits seguem Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `ci:`, `chore:`).

</details>

<details>
<summary><b>Referências</b></summary>

Design: [frontend-design](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md),
[agent-skills](https://github.com/vercel-labs/agent-skills),
[ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill).
Tokens: [rtk](https://github.com/rtk-ai/rtk), [caveman](https://github.com/juliusbrussee/caveman),
[caveman output style](https://github.com/carlosduplar/caveman-output-style-claude-code),
[ponytail](https://skillsllm.com/skill/ponytail), [Claude-Skills](https://github.com/valorisa/Claude-Skills).
READMEs: [awesome-readme](https://github.com/matiassingers/awesome-readme),
[awesome-github-profile-readme](https://github.com/abhisheknaiidu/awesome-github-profile-readme),
[10 standout profile READMEs](https://dev.to/github/10-standout-github-profile-readmes-h2o).
Direção de arte: [BRAND.md](https://github.com/mandasTeam/team-docs/blob/main/BRAND.md) do mandasTeam.

</details>

<sub><a href="https://github.com/mandasTeam/readme-designer/actions/workflows/ci.yml"><img src="https://github.com/mandasTeam/readme-designer/actions/workflows/ci.yml/badge.svg" alt="CI"></a> · Licença MIT, veja <a href="LICENSE">LICENSE</a>. Fontes em <code>tools/fonts/</code> (Big Shoulders, Geist Mono, IBM Plex) sob SIL Open Font License, com os textos ao lado. Figura: Hendrick Goltzius, <i>Vulcan</i> (c. 1592), National Gallery of Art, CC0.</sub>
