from check_urls import extract, verdict

MD = """
<img src="https://a.dev/x.svg" alt="">
<a href="https://site.dev/"><img src="https://b.dev/y.svg"></a>
<source srcset="https://c.dev/dark.svg">
![logo](https://d.dev/logo.png) e [doc](https://e.dev/doc)
<img src="assets/local.svg"> <a href="mailto:x@y.z">mail</a>
<img src="https://a.dev/x.svg">
"""


def test_extrai_urls_http_sem_repetir_e_marca_imagens():
    urls, imgs = extract(MD)
    assert urls == ["https://a.dev/x.svg", "https://site.dev/", "https://b.dev/y.svg",
                    "https://c.dev/dark.svg", "https://d.dev/logo.png", "https://e.dev/doc"]
    assert imgs >= {"https://a.dev/x.svg", "https://b.dev/y.svg", "https://c.dev/dark.svg", "https://d.dev/logo.png"}
    assert "https://e.dev/doc" not in imgs


def test_veredito():
    assert verdict("u", 200, "image/svg+xml", True) == "ok"
    assert verdict("u", 200, "text/plain", True) == "NÃO-IMAGEM"
    assert verdict("u", 200, "text/html", False) == "ok"
    assert verdict("u", 402, "text/plain", True) == "FALHA"
