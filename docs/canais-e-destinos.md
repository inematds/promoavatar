# Canais e destinos — para quem, e onde fica

Como um reel sabe em que pasta ser publicado, e o que você pode ajustar sem
mexer no bot.

## A regra: duas perguntas, dois donos

| pergunta | quem responde | onde |
|---|---|---|
| **para quem** é este reel? | este repo | `flow.json`, campo `canal` de cada público |
| **onde fica** esse canal no disco? | o bot | `src/dominio/destinos.ts` |

Essa separação é proposital. Se o `flow.json` guardasse o caminho completo, ele
viraria uma segunda cópia da lista de canais — e cópias divergem. Aqui o domínio
só diz o NOME do canal (`lives24`); traduzir isso para uma pasta é problema do
bot, num lugar só.

## Mapa atual dos 12 públicos

Do `flow.json` deste repo:

| público | canal | pasta de entrega |
|---|---|---|
| empreendedores | `lives24` | `~/projetos/yt-pub-lives24/imports/videos` |
| pessoacomum | `lives2` | `~/projetos/yt-pub-lives2/imports/videos` |
| recolocacao | `lives3` | `~/projetos/yt-pub-lives3/imports/videos` |
| mulheres | `lives4` | `~/projetos/yt-pub-lives4/imports/videos` |
| tecnicos | `lives6` | `~/projetos/yt-pub-lives6/imports/videos` |
| 40mais | `lives7` | `~/projetos/yt-pub-lives7/imports/videos` |
| 60mais | `lives8` | `~/projetos/yt-pub-lives8/imports/videos` |
| educadores | `lives9` | `~/projetos/yt-pub-lives9/imports/videos` |
| criadores | `lives11` | `~/projetos/yt-pub-lives11/imports/videos` |
| jovens | `lives22` | `~/projetos/yt-pub-lives22/imports/videos` |
| profissionais | `lives23` | `~/projetos/yt-pub-lives23/imports/videos` |
| familia | `lives32` | `~/projetos/yt-pub-lives32/imports/videos` |

*Remapeado em 2026-07-31 (21→2, 24→4, 25→1, 26→6, 27→7, 28→8, 29→9, 30→11,
31→3). `jovens`, `profissionais` e `familia` seguem nos canais originais. O
mesmo mapa foi aplicado ao `promoclub`.*

A coluna da direita **não está escrita em lugar nenhum** — é derivada. A regra é
sempre `<canal>` → `~/projetos/yt-pub-<canal>/imports/videos`.

## Como ajustar

**Trocar o canal de um público.** Edite o `canal` dele no `flow.json`:

```json
"mulheres": { "canal": "lives24", "gatilho": "..." }
```

Vale no PRÓXIMO fluxo. A definição é congelada na criação, então fluxos que já
existem seguem com o canal antigo — isso é de propósito: um fluxo em andamento
não muda de destino no meio do caminho.

**Criar um canal novo.** Crie a pasta e pronto:

```bash
mkdir -p ~/projetos/yt-pub-lives33/imports/videos
```

Não se edita nem se recompila o bot. Ele descobre os canais varrendo
`~/projetos` atrás de `yt-pub-lives<N>`. Depois é só apontar o público para
`lives33` no `flow.json`.

**Conferir o que existe.** Um destino que não existe é RECUSADO na hora, com a
lista dos válidos na mensagem — não falha calado depois do render.

## O que é entregue

O MP4 final do reel daquele público, copiado (não movido) para a pasta do canal.
O original fica em `state/artefatos/reel/` no bot, que é a fonte canônica que o
`/status` conhece.

O nome do arquivo entregue segue o título do estúdio: `A8-mulheres-v1.mp4`.

## Defeito corrigido em 2026-07-31 (para quem for ler os commits)

O A#8 terminou com 11 reels prontos e **zero entregues**. A configuração estava
certa e o job carregava o destino no `input` — mas a entrega morava dentro do
notificador do chat, que desiste quando o job não tem conversa para responder. E
job de fase de fluxo tem `chat_id` nulo de propósito (senão um fluxo de 12
públicos mandaria 48 mensagens).

Entregar e avisar eram responsabilidades diferentes coladas no mesmo `return`.
Hoje o job sem chat continua mudo, mas entrega.

## O que o canal faz com o arquivo

A pasta `imports/videos` não é arquivo morto: o `import_worker.py` de cada canal
**vigia `imports/` e processa cada SUBPASTA**, move os clipes para
`lives/<video_id>/clips` e apaga a subpasta. Por isso um `imports/` vazio é o
estado normal — significa que já foi consumido.

O `video_id` sai do NOME da subpasta (`import_<data>_videos`), e o worker pula o
que já existe no banco. Consequência a lembrar: **dois lotes no mesmo canal no
mesmo dia colidem** — o segundo é ignorado. Hoje não morde, porque cada público
tem seu próprio canal.
