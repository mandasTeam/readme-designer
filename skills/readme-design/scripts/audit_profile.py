"""Auditoria de perfil GitHub numa saída só, curta, pronta para virar perguntas ao usuário.

Junta o que antes eram ~8 chamadas soltas (perfil, repos, fixados, README atual, links):
filtra antes de entrar no contexto, como o rtk faz com saída de shell.

    python audit_profile.py igorSeberino
    python audit_profile.py igorSeberino --contrib owner/repo --contrib owner/outro

Requer gh autenticado. Não altera nada.
"""
from __future__ import annotations

import argparse
import base64
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_urls import extract, probe, verdict  # noqa: E402

PHONE_RE = re.compile(r"\(?\b\d{2}\)?\s?9?\d{4}[-\s]?\d{4}\b")


def gh(*args: str, jq: str | None = None):
    cmd = ["gh", "api", *args] + (["--jq", jq] if jq else [])
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        return None
    out = r.stdout.strip()
    return json.loads(out) if out[:1] in "[{" else out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("user")
    ap.add_argument("--contrib", action="append", default=[], help="repo de grupo para conferir PRs do usuário")
    a = ap.parse_args()
    u = a.user

    me = gh(f"users/{u}") or {}
    print("PERFIL")
    for k in ("name", "bio", "company", "location", "blog", "email", "twitter_username"):
        print(f"  {k:<16} {me.get(k) or '—'}")
    socials = gh(f"users/{u}/social_accounts", jq="[.[].url]") or []
    print(f"  {'social':<16} {', '.join(socials) or '—'}")

    repos = gh(f"users/{u}/repos?per_page=100&sort=pushed",
               jq="[.[] | {n:.name, l:(.language//\"-\"), f:.fork, p:.pushed_at[:10], d:((.description//\"\")[:60])}]") or []
    print(f"\nREPOS PÚBLICOS ({len(repos)})")
    for r in repos:
        print(f"  {r['p']} {r['n']:<32} {r['l']:<12} {'fork ' if r['f'] else ''}{r['d']}")

    q = '{user(login:"%s"){pinnedItems(first:6){nodes{... on Repository{nameWithOwner}}}}}' % u
    pinned = subprocess.run(["gh", "api", "graphql", "-f", f"query={q}", "--jq",
                             "[.data.user.pinnedItems.nodes[].nameWithOwner] | join(\", \")"],
                            capture_output=True, text=True).stdout.strip()
    print(f"\nFIXADOS  {pinned or '—'}")

    content = gh(f"repos/{u}/{u}/readme", jq=".content")
    if content:
        text = base64.b64decode(content).decode("utf-8", "replace")
        urls, imgs = extract(text)
        print(f"\nREADME ATUAL  {len(text.splitlines())} linhas, {len(urls)} urls")
        for url in urls:
            st, ct = probe(url)
            v = verdict(url, st, ct, url in imgs)
            if v != "ok":
                print(f"  {v:<10} {st:>3} {url[:100]}")
        if PHONE_RE.search(text):
            print("  PRIVACIDADE  telefone público no README")
        if "linkedin.com" in text:
            print("  aviso        LinkedIn não é verificável por robô (responde 999)")
    else:
        print("\nREADME ATUAL  não existe (crie o repo <user>/<user>)")

    for repo in a.contrib:
        prs = gh(f"search/issues?q=repo:{repo}+author:{u}+type:pr&per_page=30",
                 jq='[.items[] | "#\\(.number) \\(.state) \\(.title[:70])"]') or []
        print(f"\nPRs DE {u} EM {repo} ({len(prs)})")
        for p in prs:
            print(f"  {p}")


if __name__ == "__main__":
    main()
