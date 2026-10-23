# Economia de tokens

Base: [rtk](https://github.com/rtk-ai/rtk) (filtrar saída antes do contexto),
[caveman](https://github.com/juliusbrussee/caveman) (resposta enxuta, todo fato preservado),
[ponytail](https://skillsllm.com/skill/ponytail) (a menor mudança que resolve tudo),
[rescue-tokens](https://github.com/valorisa/Claude-Skills) (as armadilhas que gastam em silêncio).
O objetivo é custo menor **sem** perder verificação. Uma negação perdida custa mais que
todos os tokens economizados.

## Onde o gasto aparece num trabalho de README

| Armadilha | Custo típico | Troca |
|---|---|---|
| Ler um SVG gerado para "conferir" | 50–250 KB por arquivo | folha PNG + `vision_analyze`; `grep -c` para checar uma string |
| Imprimir base64 (avatar, ícones) | dezenas de KB | nunca imprimir; `ls -la` para tamanho |
| JSON cru de `gh api` | 5–30 KB por chamada | `--jq` com os campos que decidem algo, ou `audit_profile.py` |
| Página inteira de referência | 15–60 KB | `gh api .../contents/<SKILL.md> -H "Accept: application/vnd.github.raw" \| head -n 60` ou `web_extract` com `char_limit` |
| Um screenshot por card | 1 imagem por card | uma folha + recortes com `region` |
| Folha de 5000 px de altura | a imagem é reduzida e o detalhe some | recortar por região em vez de pedir outra captura |
| Perguntas em vários turnos | contexto reenviado a cada turno | um `clarify` com até 5 perguntas |
| Reescrever arquivo inteiro para mudar 1 linha | o arquivo todo, duas vezes | `patch` ou edição via Python |
| Editar SVG à mão | ler + escrever o SVG | mudar o `CONFIG` do gerador e rodar de novo |
| Log de CI inteiro | milhares de linhas | `gh run view <id> --log-failed`, depois só o traceback |

## Regras de leitura (entrada)

- Filtre na origem: `--jq`, `head -n`, scripts que imprimem só falhas (`check_urls.py` sem `--all`).
- Carregue as referências da skill sob demanda, no passo que pede. A descrição da skill é paga
  todo turno; o corpo, só quando ela é usada; as referências, só quando abertas.
- Quem já está no contexto não precisa ser relido.

## Regras de ação

- Junte chamadas independentes no mesmo turno. Serialize só o que depende do resultado anterior.
- Um script re-rodável vence dez edições manuais.
- Sem widget, seção ou serviço que ninguém pediu (ponytail: "precisa existir?").
- Prefira o que já existe: `svgkit`, serviços tematizáveis, `gh`.

## Regras de resposta (saída)

- Resposta primeiro. Sem saudação, sem "vou agora…", sem recapitular o pedido.
- Relatório final: o que mudou, o que foi conferido (com a prova: commit, run, URL), o que ficou pendente.
- Comandos, caminhos, hashes e URLs vão exatos. Comprima a prosa, nunca o fato.
- Mostrar resultado (prévia, link) vence descrever resultado.

## Nunca cortar

- A checagem de fatos do passo 1.
- `alt` completo e `prefers-reduced-motion`.
- A conferência renderizada antes e depois do push.
- O teste de script com lógica (parser, contador): um teste pequeno fica.
