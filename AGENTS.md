# AGENTS.md

Regras para agentes que editam este repositório.

- Idioma: pt-BR em tudo (skill, referências, commits, README).
- Commits: Conventional Commits simples (`feat:`, `fix:`, `docs:`, `test:`, `ci:`, `chore:`), assunto curto no imperativo.
- `skills/readme-design/SKILL.md` fica enxuto (~150 linhas). Detalhe vai para `references/`, carregado sob demanda.
- Ao aprender algo novo, corrija o texto que ficou errado em vez de empilhar uma exceção.
- Script com lógica ganha teste em `tests/` (sem rede). Rode `python -m pytest -q` antes do commit.
- Não leia os SVGs gerados (`assets/`): são paths enormes. Rode `python tools/build_banner.py` e confira com `skills/readme-design/scripts/contact_sheet.py`.
