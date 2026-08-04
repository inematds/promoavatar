# Layout × template de avatar — regra acertada, ainda NÃO implementada

Registrado em 2026-08-04, a pedido do dono, para fazer depois. **Nada disto está
no código hoje.** Está aqui porque a decisão já foi tomada uma vez em conversa,
não virou arquivo, e se perdeu — a sessão seguinte não sabia que existiam dois
templates no HeyGen e o prompt continuou apontando para um nome só.

## O que existe no HeyGen (e não estava escrito em lugar nenhum)

Dois projetos de origem, não um:

- **`TEMPLATE-AVATAR16`** — avatar horizontal (16:9);
- **`TEMPLATE-AVATAR9`** — avatar vertical (9:16), com a legenda desativada.

> A legenda **não importa** para este sistema (decisão do dono, 2026-08-04):
> o pipeline não usa legenda do HeyGen, e o layout se ajusta vindo ela ou não.
> Não é critério de escolha entre os dois.

O `prompts/fase-navega-avatar.md` hoje busca **`TEMPLATE-AVATAR`**, sem sufixo.
Isso casa com os dois por prefixo — e o prompt manda **parar e reportar quando a
busca devolve mais de um resultado**. Vale conferir se a busca do HeyGen é exata
ou por prefixo antes de mexer: se for por prefixo, a regra de ambiguidade já
está sendo contornada de alguma forma, e é preciso entender qual.

## A regra

**1. O mapa classifica o layout em vertical ou horizontal.** Ele já traduz
`Formato escolhido:` → layout; passa a dizer também de que tipo é o layout.

| layout | faixa do avatar | tipo |
|---|---|---|
| `empilhado-capa` | 1080×608 (1,78 = 16:9) | horizontal |
| `empilhado-explicativo` | 1080×608 (1,78 = 16:9) | horizontal |
| `diptico` | 1080×960 (1,12) | vertical |
| `imagem-plena` | PiP 468×264 | vertical |

**2. Horizontal → `TEMPLATE-AVATAR16`**, o avatar preenche a faixa deitada.

**3. Vertical → `TEMPLATE-AVATAR9`.** Pode-se usar o 16 num layout vertical,
**mas só como PiP** — nunca aberto ocupando a faixa.

**4. Dentro do vertical, full ou PiP decorre da mídia, não de escolha:**

- avatar veio **9:16** → **rosto full** na faixa;
- avatar veio **16:9** → **PiP**.

Este passo 4 **já é automatizável hoje**: o `preparar.py` sonda largura/altura
do avatar (`sonda()`) e grava no manifesto. Basta o template ler isso em vez de
ter a forma fixa — `imagem-plena` já traz `"forma": "pip"` cravado.

## O que impede: a ordem das fases

```
texto → [portão] → navega-avatar → baixar → [portão] → reel
                        ↑                                ↑
                  gera o avatar                  resolve o layout
```

O avatar é gerado **antes** de o layout existir. A `navega-avatar` não tem como
saber se o reel será `imagem-plena` ou `empilhado-capa`, então não tem como
escolher entre o `-16` e o `-9`.

**A saída:** subir a resolução do layout para a **fase texto**. O formato
editorial já é decidido lá (`Formato escolhido:`, aprovado por você no portão) e
o mapa já é determinístico — então o layout pode ser resolvido e gravado junto
com o texto. A cadeia fica:

```
formato editorial → layout → tipo (vertical/horizontal) → qual TEMPLATE-AVATAR
        ✅ existe      ✅ existe          ❌ falta                ❌ falta
```

O `preparar.py` continuaria resolvendo o layout como faz hoje (a precedência
`--template` > alvo > mapa > padrão não muda) — o que muda é que a decisão passa
a estar disponível **antes**, para quem precisa dela antes.

## Estado atual, para não confundir depois

- Os 12 alvos do `flow.json` **não** têm campo `template`. Quem decide é o mapa,
  com `empilhado-capa` como padrão da raiz.
- No A#23 (primeiro fluxo com o conserto de 2026-08-04) o mapa resolveu sozinho:
  jovens → `imagem-plena`, tecnicos → `diptico`. Nos 18 reels do A#21/A#22 o
  campo era `None` e quem escolhia era o agente na hora do render.
- A `navega-avatar` usa um template fixo e não sabe nada de layout.
