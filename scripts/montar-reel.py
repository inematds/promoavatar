#!/usr/bin/env python3
"""montar-reel.py — do avatar ao MP4 entregavel, numa chamada.

Fecha a fase `reel`. Depois das decisoes de 2026-08-04 (SFX fora, legenda SEM,
revisor virou script — `docs/decisoes-reel.md`) a sequencia nao tem mais
ramificacao: preparar -> portao 1 -> render -> revisor -> CTA -> QC. Isto e um
encadeamento, e encadeamento e trabalho de script.

Por que existe: levantados 7 workspaces do A#22, sairam 7 estruturas
DIFERENTES — a mesma coisa com tres nomes (`reel-body` / `corpo-final` /
`render-high`), listas de concat escritas a mao, e 3 reels que nao chegaram a um
MP4 de corpo. Nada no conteudo daqueles publicos justificava sete caminhos: era
improviso. Aqui os nomes sao FIXOS:

  <ws>/motion/index.html   composicao
  <ws>/motion/corpo.mp4    render sem CTA (e o que o revisor analisa)
  <ws>/final/reel.mp4      ENTREGAVEL (corpo + CTA)
  <ws>/qc/mosaico.png      o que o olho humano ve — uma imagem

O revisor roda no CORPO, nao no final: o CTA tem audio proprio e 3s sem fala,
que o `verify-cut.py` leria como silencio longo. O QC visual roda no FINAL,
justamente para confirmar que o CTA entrou.

O que sobra para o modelo depois disto: olhar o mosaico (a imagem 1 provoca? a
headline le de relance? o fecho tem o CTA?) e reagir a exit != 0. Mais nada.

Uso:
  python3 montar-reel.py --avatar <mp4> --ws <workspace> --alvo <publico> \\
      --textos <repo>/textos/<REF>/<publico>.md
  [--qualidade high|standard|draft] [--sem-cta] [--cta <mp4>] [--pular-preparo]

Exit 0 = entregavel pronto · 3 = algum portao reprovou · 2 = erro de arquivo.
"""
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
REPO = AQUI.parent


def sh(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def erro(msg: str, code: int = 2):
    print(f"ERRO: {msg}", file=sys.stderr)
    sys.exit(code)


def passo(n: str):
    print(f"\n=== {n}", flush=True)


def duracao(v: str) -> float:
    r = sh(["ffprobe", "-v", "error", "-of", "json",
            "-show_entries", "format=duration", v])
    try:
        return float(json.loads(r.stdout)["format"]["duration"])
    except Exception:
        return 0.0


def npx_hyperframes(args, cwd):
    """A skill exige `npx --no-install` em toda invocacao (nada de baixar no meio
    do job)."""
    return sh(["npx", "--no-install", "hyperframes"] + args, cwd=cwd)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--avatar", required=True)
    ap.add_argument("--ws", required=True)
    ap.add_argument("--alvo", default="reel")
    ap.add_argument("--textos", default=None)
    ap.add_argument("--qualidade", default="high", choices=["high", "standard", "draft"])
    ap.add_argument("--cta", default=str(REPO / "cta" / "cta-9x16.mp4"))
    ap.add_argument("--sem-cta", action="store_true")
    ap.add_argument("--pular-preparo", action="store_true",
                    help="ja existe index.html e voce so quer render/QC")
    a = ap.parse_args()

    ws = Path(os.path.expanduser(a.ws))
    motion, final = ws / "motion", ws / "final"
    final.mkdir(parents=True, exist_ok=True)

    # ---- 1. preparar: midia, imagens, tempos, template, index.html ----
    if not a.pular_preparo:
        passo("1/6 preparar (midia, transcricao, imagens, tempos, template, HTML)")
        cmd = [sys.executable, str(AQUI / "preparar.py"), "--avatar",
               os.path.expanduser(a.avatar), "--ws", str(ws), "--alvo", a.alvo]
        if a.textos:
            cmd += ["--textos", os.path.expanduser(a.textos)]
        r = sh(cmd)
        print(r.stdout.rstrip() or r.stderr.rstrip())
        if r.returncode != 0:
            return 3 if r.returncode == 3 else 2
    index = motion / "index.html"
    if not index.exists():
        erro(f"sem {index} — rode sem --pular-preparo")

    # ---- 2. portao 1: o determinismo ANTES de renderizar ----
    # Renderizar para descobrir com o olho o que o lint diria de graca e o
    # desperdicio mais caro da fase.
    passo("2/6 portao 1 (lint + ritmo visual) — antes de gastar render")
    r = npx_hyperframes(["lint", "."], cwd=str(motion))
    print((r.stdout or r.stderr).strip()[-400:])
    if r.returncode != 0:
        print("REPROVADO no lint — nao renderizei.")
        return 3
    lt = AQUI / "lint-timeline.py"
    if not lt.exists():
        lt = Path.home() / ".claude/skills/reel-edita-inema/scripts/lint-timeline.py"
    if lt.exists():
        r = sh([sys.executable, str(lt), str(index)])
        print((r.stdout or r.stderr).strip()[-300:])
        if r.returncode != 0:
            print("REPROVADO no ritmo visual (beat > 4s) — nao renderizei.")
            return 3

    # ---- 3. render do CORPO ----
    passo(f"3/6 render do corpo (--quality {a.qualidade})")
    r = npx_hyperframes(["render", ".", "-o", "corpo.mp4", "-q", a.qualidade],
                        cwd=str(motion))
    corpo = motion / "corpo.mp4"
    if r.returncode != 0 or not corpo.exists():
        print((r.stdout or r.stderr).strip()[-600:])
        erro("render falhou")
    print(f"corpo {corpo}  {duracao(str(corpo)):.2f}s")

    # ---- 4. revisor, sobre o CORPO ----
    passo("4/6 revisor (audio do render, silencio, ritmo)")
    r = sh([sys.executable, str(AQUI / "revisor.py"), "--video", str(corpo),
            "--ws", str(ws)])
    print((r.stdout or r.stderr).rstrip())
    if r.returncode != 0:
        print("REPROVADO no revisor.")
        return 3

    # ---- 5. CTA no fim ----
    passo("5/6 CTA + entregavel")
    entrega = final / "reel.mp4"
    cta = os.path.expanduser(a.cta)
    if a.sem_cta:
        shutil.copy(corpo, entrega)
        print("CTA pulado (--sem-cta)")
    elif not os.path.exists(cta):
        erro(f"CTA nao existe: {cta}")
    else:
        # Mesmos parametros nos dois (h264/yuv420p/30fps, aac 48k stereo), entao
        # o concat demuxer copia sem reencodar. Se algum dia divergirem, o copy
        # falha ou sai com duracao errada — por isso a duracao e CONFERIDA
        # abaixo, e ai reencodamos.
        lista = ws / "concat.txt"
        lista.write_text(f"file '{corpo}'\nfile '{cta}'\n", encoding="utf-8")
        r = sh(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                "-i", str(lista), "-c", "copy", str(entrega)])
        esperado = duracao(str(corpo)) + duracao(cta)
        if r.returncode != 0 or abs(duracao(str(entrega)) - esperado) > 0.2:
            print("concat por copia nao bateu a duracao — reencodando")
            r = sh(["ffmpeg", "-y", "-v", "error", "-i", str(corpo), "-i", cta,
                    "-filter_complex",
                    "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]",
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    str(entrega)])
            if r.returncode != 0:
                erro("concat do CTA falhou: " + r.stderr.strip()[:300])
    print(f"entregavel {entrega}  {duracao(str(entrega)):.2f}s")

    # ---- 6. QC visual, sobre o ENTREGAVEL (para o CTA entrar no quadro) ----
    passo("6/6 QC (portoes 2 e 3)")
    r = sh([sys.executable, str(AQUI / "qc-frames.py"), "--video", str(entrega),
            "--ws", str(ws)])
    print((r.stdout or r.stderr).rstrip())
    if r.returncode != 0:
        print("REPROVADO no QC.")
        return 3

    print(f"\nPRONTO      {entrega}")
    print(f"OLHE        {ws/'qc'/'mosaico.png'}  — uma imagem, nao a serie de frames.")
    print("            imagem 1 provoca? headline le de relance? o fecho tem o CTA?")
    return 0


if __name__ == "__main__":
    sys.exit(main())
