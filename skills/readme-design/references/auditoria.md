# Auditoria de fatos

Antes de desenhar, confira o que é verdade hoje. README de perfil envelhece rápido: cargo,
semestre, portfólio, certificações. Um README bonito com informação errada é pior que o antigo.

## O que rodar

```
terminal("python scripts/audit_profile.py <user> --contrib dono/repo-de-grupo")
```

A saída traz: campos do perfil, redes sociais, repos públicos (data, linguagem, fork,
descrição cortada), repos fixados, links do README atual que falham e alerta de telefone.

## O que procurar

| Achado | Ação |
|---|---|
| Link 404 (portfólio no Pages, repo apagado) | Remover do README **e** do campo `blog` do perfil |
| Telefone, endereço, e-mail pessoal | Perguntar se mantém. O padrão é tirar |
| Repo citado é privado | Não linkar. Perguntar se cita sem link |
| Projeto de grupo | Conferir PRs e commits do usuário (`--contrib`) e creditar **só** o que ele fez |
| Nome da instituição | Conferir no site oficial (ex.: "Católica SC – Centro Universitário", não "PUCSC") |
| Cargo no crachá vs. trabalho real | Perguntar. Às vezes o título oficial não descreve o dia a dia |
| Certificados | Testar os links. Se a pessoa já está empregada, perguntar se ainda fazem sentido |
| `bio`, `company` vazios | Oferecer preencher (precisa do escopo `user`) |

## Endpoints úteis (escopo `user`)

- Bio, empresa, site: `gh api -X PATCH user -f bio="..." -f company="..." -f blog=""`
- Remover rede social: `echo '{"account_urls":["https://linkedin.com/in/x/"]}' | gh api -X DELETE user/social_accounts --input -`
- O e-mail público só aceita um endereço já verificado em Settings → Emails. O agente não consegue trocar.

## Saída do passo

Uma lista curta, em 3 grupos: **confirmado**, **corrigir** (com a fonte) e **perguntar**.
O grupo "perguntar" vira o `clarify` do passo 2.
