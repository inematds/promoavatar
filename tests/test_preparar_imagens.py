"""ler_imagens tem que aceitar a variacao de nivel do cabecalho.

Medido em 2026-08-08: os 48 textos de A#49 a A#52 sairam com `### IMAGENS` em
vez de `## IMAGENS`, e TODOS os reels desses quatro fluxos falharam com "sem
segmentos.json (faltou transcript ou secao IMAGENS)". O transcript estava la; o
que faltava era o parser aceitar tres `#`. Retentar nao resolvia — falhava
igual, quantas vezes fosse.

O texto e escrito por LLM: o nivel do cabecalho vai variar de novo. Quem se
adapta e o parser, nao os 48 arquivos.
"""
import importlib.util
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "preparar", AQUI.parent / "scripts" / "preparar.py")
preparar = importlib.util.module_from_spec(spec)
sys.modules["preparar"] = preparar
spec.loader.exec_module(preparar)


CORPO = """IMAGEM 1 — "primeiras palavras" [ATENCAO]
headline: UMA COISA | OUTRA
hook: algo com {acento}
A photorealistic desk with a lamp

IMAGEM 2 — "segundo segmento"
headline: SEGUNDA
A quiet room with a window
"""


def escreve(tmp_path, cabecalho, seguinte="## ESTRUTURA\nfim\n"):
    md = tmp_path / "pub.md"
    md.write_text(f"### FALA\nblabla\n\n{cabecalho}\n{CORPO}\n{seguinte}",
                  encoding="utf-8")
    return md


def test_dois_hashes(tmp_path):
    assert len(preparar.ler_imagens(escreve(tmp_path, "## IMAGENS"))) == 2


def test_tres_hashes(tmp_path):
    """O caso que derrubou A#49-A#52."""
    assert len(preparar.ler_imagens(escreve(tmp_path, "### IMAGENS"))) == 2


def test_um_hash(tmp_path):
    assert len(preparar.ler_imagens(escreve(tmp_path, "# IMAGENS"))) == 2


def test_para_na_proxima_secao_de_qualquer_nivel(tmp_path):
    """Com `### IMAGENS`, a secao seguinte tambem vem com tres `#`."""
    md = escreve(tmp_path, "### IMAGENS", seguinte="### ESTRUTURA\nnao entra\n")
    itens = preparar.ler_imagens(md)
    assert len(itens) == 2
    assert all("nao entra" not in (i.get("prompt") or "") for i in itens)


def test_campos_continuam_sendo_lidos(tmp_path):
    itens = preparar.ler_imagens(escreve(tmp_path, "### IMAGENS"))
    assert itens[0]["headline"] == "UMA COISA | OUTRA"
    assert itens[0]["hook"] == "algo com {acento}"
    assert "photorealistic" in itens[0]["prompt"]


def test_sem_secao_devolve_vazio(tmp_path):
    md = tmp_path / "p.md"
    md.write_text("### FALA\nso fala\n", encoding="utf-8")
    assert preparar.ler_imagens(md) == []
