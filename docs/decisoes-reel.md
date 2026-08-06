# Decisões da fase reel — o que mudou, por quê, e como voltar

Registro para quem chegar depois (inclusive nós). Cada decisão traz a
**evidência** que a sustenta, o **caminho de volta** e **o que a invalidaria** —
sem isso, daqui a três meses ninguém sabe se a regra ainda vale ou se está
copiando um acidente.

Base do levantamento: `segunda-metade-do-reel.md` (2026-08-04).
Contexto que vale para todas: o avatar deste pipeline é **TTS do HeyGen**, não
gravação humana. Boa parte da receita herdada da skill global
`reel-edita-inema` pressupõe bruto gravado por pessoa. **Se um dia a entrada
virar vídeo gravado de verdade, as três decisões abaixo mudam juntas.**

---

## 1. SFX saem da receita — 2026-08-04

**O que muda:** `make-sfx.sh` e `mix-sfx.py` não fazem parte do pipeline do
promoavatar. Não gere, não mixe, não crie a pasta `sfx/`.

**Por quê:** a skill global manda mixar SFX sutis, e em **18 de 18** reels
(A#21 + A#22) **nenhum** workspace tem pasta `sfx/`. Estava na receita e não
acontecia. Uma instrução que ninguém segue não é padrão: é ruído que faz o
agente gastar decidindo se desta vez segue.

**Como voltar:** os scripts continuam na skill global, intactos —
`~/.claude/skills/reel-edita-inema/scripts/`. Voltar é reintroduzir o passo em
`prompts/reel-regras.md` e rodar `mix-sfx.py --base <render> --sfx-dir sfx
--events '[["boom",0.0],...]'` **depois** do QC visual (ele usa `-c:v copy`: o
vídeo sai bit a bit idêntico, então rever imagem depois não faz sentido).

**O que invalidaria:** medir que reel com SFX retém mais. Hoje não há essa
medição — os SFX saíram por não existirem na prática, não por terem sido
testados e reprovados.

---

## 2. Legenda continua com default SEM — 2026-08-04

**O que muda:** nada em relação a hoje; fica **registrado** para não se inverter
por acidente de novo.

**Por quê:** quem decide legenda é o estúdio, não o pipeline (commit `69ed8b5`,
"legenda: default SEM, porque quem decide é o estúdio"). Já se inverteu uma vez
por engano nesta base: o A#22 nasceu na janela em que o default estava ligado e
pediu legenda que o promoavatar não usa — **isso contaminou toda a comparação
de custo A#22 × A#19**, que ficou inutilizável. O prejuízo de mexer nisso sem
querer não é estético, é perder a medição.

**Como voltar (ligar legenda):** `captions.py --transcript <corte-word.json>
--keywords "..."` gera os beats; a composição pinta a palavra-chave no acento,
**na altura do peito, nunca no terço inferior** (a interface da rede cobre o
rodapé). O único parâmetro editorial é `--keywords` — e ele deve vir da **fase
1**, como `headline:` e `hook:` já vêm pela regra 11b, não ser inventado na hora
do render. Ligar sem isso repete o erro que a 11b corrigiu para as imagens.

**O que invalidaria:** o estúdio passar a querer legenda por padrão. Aí a
mudança certa é na fase 1 (trazer `keywords:`), não no render.

---

## 3. O revisor da fase 5 vira script — 2026-08-04

**O que muda:** a FASE 5 da skill global manda spawnar um **subagente
independente obrigatório** que re-transcreve o render final e o lê inteiro
procurando repetição. Neste pipeline isso é substituído por
`scripts/revisor.py`.

**Por quê:** era o maior gasto de modelo que restava na fase, e o que ele
procura ou já é script, ou nunca ocorreu:

- repetição/silêncio → `verify-cut.py`, e `repeticoes=0` em **18 de 18** reels
  (o avatar é TTS: não tem falso começo, blooper nem tomada repetida);
- ritmo visual → `lint-timeline.py`;
- render truncado/mudo → já coberto por `qc-frames.py` (portão 2 absorvido).

Um subagente lendo transcrição inteira para confirmar o que três scripts
verificam de graça é caro **e** menos confiável: ele julga, eles medem. O
julgamento que sobra (a imagem provoca? a headline lê?) continua sendo humano,
sobre o mosaico do `qc-frames.py` — não era isso que a fase 5 fazia.

**Achado ao implementar (2026-08-04):** o `verify-cut.py` mistura **silêncio
longo** e **repetição de n-grama** num único exit, e os dois não têm o mesmo
peso aqui. Ele foi escrito para bruto humano, onde n-grama repetido significa
**tomada dobrada**. Em TTS tomada dobrada não existe por construção: repetição
só pode vir do **texto**, que já passou pelo portão humano da fase 1. No
primeiro teste do `revisor.py` ele reprovou o reel por `"o professor"` repetido
— paralelismo retórico, não defeito. Então, neste pipeline:

- **silêncio longo no corpo → REPROVA** (indica montagem quebrada), mas o
  limiar subiu de **0,6s para 2,0s** em 2026-08-05. Os 0,6s vinham do
  `verify-cut`, pensado para bruto humano JÁ CORTADO, onde uma pausa dessas
  significa corte mal feito. Aqui o áudio é a fala inteira do avatar, sem corte
  nenhum — e TTS respira: no A#25/profissionais, pausas de **0,84s e 1,07s**
  reprovaram um reel que estava perfeito. Buraco de montagem de verdade é da
  ordem de segundos, não de décimos;
- **repetição de n-grama → informativa**, sai no relatório e não derruba.

**Isto se inverte junto com a decisão 1 e 2 se a entrada virar gravação
humana** — é o mesmo pressuposto (TTS) sustentando as três.

**Como voltar:** `references/05-revisor.md` na skill global descreve o subagente
e continua lá, intacto. Voltar é reintroduzir o spawn em
`prompts/reel-regras.md`. Para voltar só a severidade da repetição, é a seção
"2. silencio longo no corpo + repeticao audivel" do `revisor.py`.

**O que invalidaria:** a entrada deixar de ser TTS. Com bruto humano voltam
repetição e blooper de verdade, e aí `islands.py`/`cut.py` voltam junto — a
`revisor.py` sozinha não cobre esse caso (ela verifica, não decide qual tomada
fica).

---

## Nota de método

As três decisões seguem o mesmo padrão que se repetiu nesta base o dia inteiro:
**instrução em prompt não é portão.** Foram medidas 5 ocasiões em que o agente
ignorou regra escrita. Por isso cada decisão aqui só é considerada aplicada
quando existe script ou quando o caminho alternativo foi removido — anotar no
doc é memória, não garantia.

---

## 4. haiku na fase reel: reprovado (2026-08-06)

**Decisão:** a fase reel roda em **sonnet**. `flow.json` volta a
`reel: {perfil: {modelo: sonnet}}`.

**O que foi testado:** o A#29 disparou os 12 reels com `modelo: haiku`,
`esforco: low`, na noite de 2026-08-05 (23:38).

**O que aconteceu — dois defeitos, nenhum reel entregue:**

- **Job 582** (`A#29/40mais/reel`) morreu em **58 segundos**:
  `o agente reportou erro: ** sistema bloqueou redirecionamento para
  .../reelpromo/582.mp4.log`. O haiku escreveu um redirecionamento de shell que
  o portão de permissão recusou. É o comando que a própria instrução da tarefa
  manda usar (`nohup bash -c '...' > ....log 2>&1 &`) — o sonnet o executa há
  quatro fluxos sem problema.
- **Job 583** (`A#29/60mais/reel`) ficou **1h47 sem produzir uma linha de log
  nem um arquivo**, e sem processo filho vivo. Contra **3,7 min de mediana** do
  sonnet no A#28. Segurou a fila `render` (1 por vez) e travou os 11 restantes,
  além do A#30 e do A#31 atrás dele.

**Por que não é questão de preço:** medido em `inemaccbot/docs/custo-por-fase-a19-a29.md`,
o reel em sonnet custa **US$ 0,18 por público** (US$ 2,08–2,37 por fluxo de 12) —
11% do custo do fluxo. A navegação é 85%. Trocar o modelo da fase reel para
economizar mira a fatia errada e comprou dois defeitos de produção.

**O que a medição mostrou do haiku antes de travar** (2 jobs casados, A#29):
saída de **4,6k tokens** contra **1,0k** do sonnet — escreve ~4× mais para
disparar o mesmo comando. `cache_read` igual (198k contra ~180k).

**Como voltar:** trocar `perfil.modelo` da fase `reel` no `flow.json`. Fluxos já
criados têm a definição congelada no banco — para eles vale o `modelo` gravado
na linha do job, que vence na resolução (`src/fila/skills.ts:179`).

**O que invalidaria:** a fase reel virar `kind: function`. Aí não há modelo
nenhum a escolher — e é para lá que ela está indo, já que o agente hoje só
resolve nome de arquivo e dispara um comando.
