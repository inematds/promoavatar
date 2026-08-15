# Melhorias criativas do roteiro e do reel

Anotação. O item 1 (gancho) e a crítica dos 12 pontos JÁ viraram as REGRAS DE
ESCRITA de `prompts/fase1-texto.md` em 2026-07-31. O item 2 (CTA como clipe)
continua sem implementação.

## 1. Falta a frase de gatilho na ENTRADA

Os roteiros da fase 1 abrem indo direto ao assunto. Falta o gancho — a frase de
atração que segura quem está rolando o feed nos primeiros 2 segundos.

Comparando as aberturas do A#1 (12 públicos), dá para ver que algumas já
tropeçam no gancho por acidente e outras não:

- `pessoacomum`: "Você usa a IA do jeito preguiçoso" — tem tensão, funciona
- `40mais`: "Sua experiência vale mais quando é multiplicada pela IA" — é uma
  afirmação boa, mas não é gancho: não cria pergunta na cabeça de ninguém
- `mulheres` (A#4): "Você já pensou em ter seu próprio sistema de IA
  trabalhando por você?" — pergunta, mas morna

Onde mexer: na skill `inemaclub-textos`, ou no `prompts/fase1-texto.md` como
requisito explícito de estrutura — hoje a seção ESTRUTURA descreve a fórmula
(identificação → promessa → mecânica → prova → CTA) e o gancho não aparece como
item obrigatório e separado.

**A decidir:** o gancho é a primeira frase da FALA (o avatar diz), ou é só
sobreposição de tela? Muda quem escreve e onde entra no vídeo.

## 2. CTA final mais impactante — e pré-renderizado como clipe

Hoje o CTA é texto no roteiro ("Saiba mais no inema.club" / "a trilha gratuita
te espera no inema.club"), falado pelo avatar e reforçado por sobreposição.

**Ideia: virar um clipe pronto**, colado no fim de todo reel em vez de gerado a
cada vez.

Vantagens:

- **Consistência de marca** — o fecho é sempre idêntico, em vez de variar por
  roteiro e por render
- **Mais impacto** — um clipe feito uma vez com capricho (animação, som,
  assinatura) vence um CTA improvisado 12 vezes
- **Mais barato** — sai do caminho do LLM e do render: é um `ffmpeg concat` no
  fim, determinístico. Conversa direto com `docs/ideias-custo-de-token.md` no
  repo do bot, item 3.2 (determinizar o que hoje é decisão de modelo)

A decidir antes:

- O avatar continua **falando** o CTA, ou o clipe assume sozinho? Se o avatar
  parar de falar, o roteiro encurta e a fala fica só no conteúdo
- **Um clipe só ou um por público?** O gatilho de cada público sugere fechos
  diferentes; um só é mais barato e mais consistente
- Onde ele mora e quem versiona (repo de domínio? `output/`?)
- Formato: 9:16, mesma resolução e fps do reel (1080x1920, 30 fps), com áudio —
  senão o concat re-encoda e perde qualidade

## 3. Relação entre os dois

Gancho na entrada e CTA no fim são as duas pontas da retenção. Vale tratá-los
juntos quando formos mexer: o modo "capa de impacto" da skill `reel-edita-inema`
já é focado em retenção, e é onde os dois encostam.

---

## 4. Duas perguntas que travam o roteiro (2026-07-31)

Saíram da crítica ao roteiro de `jovens`. O prompt já tem regra defensiva para
as duas — ele OMITE em vez de inventar — mas isso é remendo: o certo é a
resposta entrar no assunto.

**"Tiza" — o que é?** ✅ RESPONDIDO em 2026-07-31: **Nei Maldaner e Tiza são os
gestores da comunidade INEMA.** Viraram CONTEXTO FIXO no
`prompts/fase1-texto.md`, com exceção explícita à regra 12 — que, sem isso,
apagaria a Tiza do roteiro por ser nome sem papel declarado. No roteiro eles são
PROVA SOCIAL; não é preciso explicar o cargo, porque quem assiste é da
comunidade e já sabe.

**A data de início.** O roteiro saiu com "começa dia tal" — rascunho, e rascunho
derruba a credibilidade inteira. Regra atual: data, preço e número só entram se
vierem LITERALMENTE no assunto; senão a frase sai sem eles.

Sobra a DATA. Sem ela o roteiro perde a urgência real — e a fabricada ("garanta
sua vaga") está proibida no prompt justamente porque não há vaga limitada que a
sustente. A prova social já está resolvida.

---

## 5. Os quatro gatilhos, do texto ao vídeo (2026-07-31)

O gancho não podia morrer no roteiro: quem retém é o VÍDEO. Os quatro momentos
agora estão amarrados nos dois lugares onde são decididos:

| gatilho | onde | quem executa |
|---|---|---|
| ATENÇÃO (0–2s) | 1ª frase da FALA + headline na tela | fase 1 escreve, fase 3 monta |
| RETENÇÃO (miolo) | lacuna de curiosidade + imagem trocando por segmento | fase 1 abre, fase 3 sustenta |
| ENGAJAMENTO | convite a agir na tela (comentar / salvar / marcar) | fase 1 escolhe, fase 3 posiciona |
| CTA (fecho) | ordem imperativa, falada e na tela | fase 1 escreve, fase 3 fixa |

Implementado em `prompts/fase1-texto.md` (regra 11: as SOBREPOSIÇÕES viram o
roteiro VISUAL, nomeadas com os quatro) e no `entrega` da fase `reel` no
`flow.json`, que manda CRIAR o que faltar em vez de sair sem.

**Cuidado ao mexer:** o `flow.json` é CONGELADO na criação do fluxo. Os fluxos
que já existem seguem com a instrução antiga; só os novos pegam esta.

**Ainda aberto:** o CTA como clipe pronto (item 2 acima). Se ele virar clipe, o
quarto gatilho sai do caminho do LLM e do render — passa a ser concat de
ffmpeg, sempre idêntico.

---

## 6. Legenda mais perto da borda inferior (2026-07-31)

Hoje a legenda palavra-a-palavra fica **na altura do peito** — é o que a skill
`reel-edita-inema` faz por padrão ("palavra-chave âmbar na altura do peito").
Pedido: descer, para mais perto da **borda inferior**.

Onde mexer — e as duas opções não são equivalentes:

**a) No `entrega` da fase `reel` (`flow.json` deste repo).** Vale só para o
promoavatar, é versionado aqui, e não afeta mais ninguém. **Mas o `flow.json` é
CONGELADO na criação do fluxo**: os fluxos que já existem seguem com a instrução
antiga, e não dá para testar via `/refazer` — só criando fluxo novo.

**b) Na skill `reel-edita-inema` (`~/.claude/skills/`).** Pega todo reel, de
qualquer origem, inclusive os disparados direto no chat. Mais abrangente e mais
arriscado: muda o padrão de coisas que ninguém está olhando agora.

Inclinação: **(a)**, porque o pedido nasceu deste pipeline e a mudança fica
rastreável no repo do domínio.

A decidir: **quanto** mais perto? "Borda inferior" pode virar legenda colada no
rodapé, e aí ela briga com a barra de interface do Instagram/TikTok, que come os
últimos ~15% da tela em 9:16. Uma margem segura provavelmente é o alvo real —
não o extremo. Vale olhar um dos reels do A#8 e medir.
