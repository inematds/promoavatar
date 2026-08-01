# PromoAvatar — Prompt Principal para 3 Versões por Assunto

## Objetivo

Receber um assunto, produto, curso, notícia, tendência ou ideia relacionada a tecnologia e inteligência artificial e gerar três abordagens diferentes de vídeo:

1. **Vídeo de Alcance** — chama atenção, amplia visualizações e compartilhamentos.
2. **Vídeo de Autoridade** — ensina, demonstra conhecimento e gera confiança.
3. **Vídeo Promocional** — conecta o problema à solução e conduz para uma oferta.

As três versões devem partir do mesmo assunto, mas não podem ser apenas pequenas variações do mesmo roteiro.

---

## Variáveis dinâmicas

- `{{publicos}}` — lista de públicos-alvo.
- `{{input}}` — assunto, notícia, produto, curso, ferramenta ou ideia principal.
- `{{ref}}` — referência para o commit.
- `{{pasta}}` — caminho absoluto onde salvar os arquivos.
- `{{saida}}` — pasta onde salvar o resumo final.
- `{{cta_principal}}` — destino principal, como INEMA.club ou INEMA.pro.
- `{{evidencias}}` — dados, testes, exemplos, fontes ou demonstrações disponíveis.
- `{{restricoes}}` — informações que não podem ser inventadas ou alteradas.

---

## Decisão inicial obrigatória

Antes de escrever os roteiros, analise o assunto e defina:

### 1. Tese central

Resuma o ponto principal do assunto em uma frase clara, específica e memorável.

A tese não pode ser genérica.

Exemplo fraco:

> A inteligência artificial está mudando tudo.

Exemplo forte:

> Quem aprende apenas ferramentas de IA corre o risco de ficar obsoleto junto com elas.

### 2. Motivo para assistir agora

Explique por que esse assunto é relevante neste momento.

Pode ser:

- uma mudança recente;
- um risco;
- uma oportunidade;
- um erro comum;
- uma descoberta;
- uma consequência prática;
- uma mudança no mercado;
- uma dúvida recorrente do público.

Não invente atualidade. Se não houver elemento temporal confirmado, use relevância prática, não urgência falsa.

### 3. Elemento demonstrável

Defina o que pode aparecer na tela para provar, ilustrar ou tornar o conteúdo mais concreto.

Exemplos:

- tela de uma ferramenta;
- resultado gerado;
- fluxo visual;
- comparação;
- antes e depois;
- gráfico;
- código;
- sistema funcionando;
- notícia;
- comentário;
- exemplo cotidiano.

### 4. Público principal

Mesmo que existam vários públicos em `{{publicos}}`, escolha o público mais adequado para cada versão.

As três versões podem falar com públicos diferentes quando isso melhorar o resultado.

---

## Estratégia das três versões

### Versão 1 — Alcance

Objetivo:

- interromper a rolagem;
- despertar curiosidade;
- provocar identificação;
- gerar compartilhamento ou comentário;
- alcançar pessoas que ainda não conhecem a marca.

Não transformar o vídeo em anúncio.

### Versão 2 — Autoridade

Objetivo:

- explicar algo concreto;
- mostrar domínio técnico ou estratégico;
- entregar uma ideia útil;
- apresentar prova, exemplo ou demonstração;
- aumentar confiança e percepção de autoridade.

A autoridade deve ser demonstrada, não apenas declarada.

### Versão 3 — Promocional

Objetivo:

- conectar uma dor ou oportunidade à solução;
- mostrar benefício;
- apresentar o produto, curso, comunidade ou formação;
- terminar com CTA direto;
- evitar exagero e pressão artificial.

---

## Regras gerais para as três versões

1. **Gancho nos 2 primeiros segundos**  
   A primeira frase precisa interromper a atenção. Não começar com saudação, contexto longo ou apresentação pessoal.

2. **Frases curtas e faladas**  
   Escrever para locução. Evitar frases longas, linguagem acadêmica ou texto com aparência de artigo.

3. **Uma ideia principal por vídeo**  
   Não tentar explicar todo o assunto em um único roteiro.

4. **Nomear conceitos importantes**  
   Não usar expressões vagas quando existir um termo específico.

5. **Mostrar antes de afirmar**  
   Sempre que possível, indicar uma prova visual, exemplo ou demonstração.

6. **Promessa realista**  
   Não prometer resultado que o produto, curso ou conteúdo não consegue sustentar.

7. **Sem urgência inventada**  
   Não usar escassez, prazo, vagas ou pressão sem informação explícita no `{{input}}`.

8. **Sem datas e preços inventados**  
   Só usar datas, números, preços ou condições presentes no material recebido.

9. **Diferenciar sem atacar gratuitamente**  
   Pode criticar ideias, práticas e erros. Não atacar pessoas, grupos ou concorrentes sem necessidade.

10. **Evitar repetição entre versões**  
    As três versões não podem ter o mesmo gancho, a mesma estrutura e o mesmo fechamento.

11. **Independência de plataforma**  
    Os roteiros devem funcionar em formato vertical para Instagram Reels, YouTube Shorts, TikTok, Facebook Reels e plataformas semelhantes.

12. **Sem referência exclusiva a uma plataforma**  
    Não dizer “aqui no TikTok”, “neste Reels” ou “no Shorts”, salvo se isso vier em `{{input}}`.

---

## Estrutura visual obrigatória

Cada roteiro deve conter:

### FALA

Texto completo da locução.

### SOBREPOSIÇÕES

- **ATENÇÃO (0–2s):** headline curta.
- **RETENÇÃO:** frase ou lacuna de curiosidade.
- **PROVA:** dado, exemplo ou elemento que aparece na tela.
- **ENGAJAMENTO:** pergunta ou estímulo natural.
- **CTA:** chamada final, quando necessária.

### ROTEIRO VISUAL

Indicar:

- o que aparece no primeiro segundo;
- cortes ou mudanças visuais;
- prova visual;
- tela, objeto, interface ou imagem usada;
- cena final.

### ESTRUTURA

Descrever a lógica do roteiro:

- gancho;
- desenvolvimento;
- prova;
- conclusão;
- CTA.

---

## Duração

- Alcance: entre 25 e 40 segundos.
- Autoridade: entre 35 e 60 segundos.
- Promocional: entre 30 e 45 segundos.

Não preencher tempo com frases desnecessárias.

---

## Saída esperada

Criar uma pasta para cada público ou assunto, conforme a organização definida pelo sistema.

Salvar:

- `01-alcance.md`
- `02-autoridade.md`
- `03-promocional.md`
- `resumo-estrategico.md`

O arquivo `resumo-estrategico.md` deve conter:

- assunto;
- tese central;
- motivo para assistir;
- público de cada versão;
- objetivo de cada vídeo;
- diferenças entre as versões;
- recomendação de ordem de publicação.

---

## Ordem recomendada de publicação

Como padrão:

1. Alcance
2. Autoridade
3. Promocional

A ordem pode mudar quando o assunto exigir, mas a alteração deve ser explicada no resumo.

---

## Operação técnica

- Salvar os arquivos em `{{pasta}}`.
- Salvar o resumo final em `{{saida}}`.
- Realizar commit Git sem push.
- Usar a referência `{{ref}}`.
- Usar o autor configurado como `inematds`.
- Não instalar, atualizar ou remover pacotes.
- Não gerar vídeo nesta fase.
- Não alterar arquivos fora das pastas definidas.

---

## Instrução final

Analise `{{input}}`, defina a estratégia e chame os três prompts especializados:

- `01-prompt-alcance.md`
- `02-prompt-autoridade.md`
- `03-prompt-promocional.md`

Cada prompt deve receber a mesma tese central, mas construir uma abordagem editorial diferente.
