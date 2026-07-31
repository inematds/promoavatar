# Melhorias criativas do roteiro e do reel

Anotação para revisar depois. **Nada aqui está implementado.**

## 1. Falta a frase de gatilho na ENTRADA

Os roteiros da fase 1 abrem indo direto ao assunto. Falta o gancho — a frase de
atração que segura quem está rolando o feed nos primeiros 2 segundos.

Comparando as aberturas do A#1 (12 públicos), dá para ver que algumas já
tropeçam no gancho por acidente e outras não:

- `pessoa-comum`: "Você usa a IA do jeito preguiçoso" — tem tensão, funciona
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
