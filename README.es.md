# promoavatar

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

Repo de **dominio** del flujo `/promoavatar` de inemaccbot: reels de promoción
para 12 públicos, con una pausa para aprobación humana.

> ## Descongelado en 2026-08-09
>
> Entre 2026-08-06 y 2026-08-09 este repo estuvo **congelado** ("intocable"), y todo el
> trabajo se destinaba a [`promoavatar3`](https://github.com/inematds/promoavatar3).
> El dueño lo autorizó: **los dos vuelven a evolucionar**.
>
> Eso **no** los convierte en uno solo. Siguen siendo sistemas separados: cada uno tiene su
> motor de reel (`scripts/`), sus layouts (`templates/`), sus objetivos y su prompt.
> Modificar este repo no afecta al otro, ni viceversa. La diferencia de propósito continúa: aquí es
> **un video por público** (12 públicos); allí son **tres** (alcance, autoridad,
> promocional).
>
> **Algo existe solo aquí:** la ruta `| navega` — el agente que controla el estudio,
> que es el plan de respaldo si cambia el DOM de HeyGen y se rompe el script de `| estudio`.
> promoavatar3 no tiene ese plan B.
>
> **Costo de la divergencia de esos tres días:** lo que este repo recibió durante la congelación
> fue solo lo mínimo para no quedar roto fuera de esta máquina: CTA versionado
> (`3e0da37`), rutas como variables de entorno (`4f10c84`) y el adaptador de
> imagen. Lo que **no** recibió fue todo lo nuevo que ganó promoavatar3 en ese
> período, y migrarlo caso por caso es decisión tuya, no algo automático.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/promoavatar/guia/es/**

El bot escribe los guiones y SE DETIENE. Tú grabas los avatares en HeyGen; cuando
termines, lo autorizas y el bot los descarga, arma los reels y los entrega en cada canal.

Aquí no hay **TypeScript**: la definición del pipeline (`flow.json`, prompts) es el
corazón del repo, y un flujo nuevo es una entrada en el registry del bot más un repo
como este. Pero hay código Python en `scripts/` (8 archivos): es el motor del reel,
que se ejecuta como una función activada por la fase `reel.montar`.

## Qué hay aquí

| archivo | qué es |
|---|---|
| `flow.json` | las fases, los 12 públicos, el canal y el activador de cada uno |
| `prompts/fase1-texto.md` | lo que recibe el agente para escribir los guiones |
| `templates/*.json` | los 4 layouts del reel 9:16 + el `mapa.json` formato→layout |
| `scripts/*.py` | los motores del reel (`preparar.py`, `montar-reel.py`) |
| `HELP.md` | la ayuda que aparece en el chat con `/promoavatar help` |
| `textos/A<N>/` | los guiones generados, un archivo por público |
| `docs/pipeline.md` | **la tabla de todo**: etapas, LLM/IA/worker, costo y tiempo |
| `docs/canais-e-destinos.md` | a quién va dirigido cada reel y dónde queda |
| `docs/` | las demás decisiones y lo que sigue pendiente |

## Para quién y dónde queda

Es la pregunta que más dudas genera, así que aquí va un resumen; el detalle está en
[`docs/canais-e-destinos.md`](docs/canais-e-destinos.md):

| pregunta | quién responde | dónde ajustar |
|---|---|---|
| **para quién** es el reel | este repo | `flow.json`, campo `canal` del público |
| **dónde queda** el canal en el disco | el bot | derivado: `~/projetos/yt-pub-<canal>/imports/videos` |

Ejemplo: `mulheres` tiene `"canal": "lives4"`, así que su reel se entrega en
`~/projetos/yt-pub-lives4/imports/videos`.

**Esta entrega es la última etapa del pipeline**: ocurre dentro de la fase
`reel`, no en una fase separada de "publicación". No existe una fase `publicar` en
`flow.json`: el destino lo indica el `canal` de cada público.

La ruta **no está escrita en ningún sitio**: siempre es
`~/projetos/yt-pub-<canal>/imports/videos`. Por eso:

- **cambiar el canal de un público** = editar `flow.json` (se aplica al próximo flujo);
- **crear un canal nuevo** = `mkdir -p ~/projetos/yt-pub-lives33/imports/videos`,
  sin tocar el bot.

## El ciclo, en una pantalla

```
/promoavatar <assunto> [--alvo=mulheres]
        │
        ▼
  1. texto     UN guion por público, guardado en textos/A<N>/<publico>.md
        │
        ⏸️  SE DETIENE — el chat te envía cada guion con el TÍTULO del video
        │      lo grabas en HeyGen con ese nombre exacto
        │      (AQUÍ es donde se cambia la portada: `capa: A#<N> <publico>` + la foto)
        │      /aprovar A#<N>
        ▼
  2.5 baixar   encuentra el video por el título y lo descarga (ventana de 90 min)
        │
        ⏸️  SE DETIENE — segundo punto de control: revisas los avatares descargados
        │      antes de gastar en la cola de renderizado
        ▼
  3. reel      arma el reel 9:16 y lo ENTREGA en el canal del público
        │
        ▼
  ✅ enlace del video final en el chat
```

## Las fases y los puntos de control

Son **4 fases lógicas y 2 puntos de control**. Estos puntos son el `"pausa_apos": true` de las
fases `texto` y `baixar` en `flow.json`: el pipeline se detiene allí y solo avanza
cuando lo autorizas.

| nº | fase | `id` en `flow.json` | cola | quién lo hace | ¿hay un punto de control después? |
|---|---|---|---|---|---|
| 1 | texto | `texto` | `texto` | agente (opus) | ✅ `/aprovar A#N` |
| 2 | avatar | *5 rutas, abajo* | — | **normalmente tú** | — |
| 2.5 | baixar | `baixar` | `io` | función `heygen.baixar` | ✅ tú revisas |
| 3 | reel | `reel` | `render` | función `reel.montar` | fin (entrega en el canal) |

`baixar` es una fase intermedia a propósito: no crea nada, solo trae al disco lo que ya
existe en el estudio.

Aprobar antes es mejor que volver a intentarlo después: el renderizado del avatar y la cola del reel
cuestan caro y no se pueden deshacer. Los dos puntos de control existen para eso: el primero
protege el gasto del avatar y el segundo protege el gasto del renderizado.

### La fase 2 tiene 5 rutas

Solo se ejecuta una por flujo. Las cuatro automáticas son fases con la clave `opcional` en
`flow.json`; la quinta es la ausencia de todas ellas.

| ruta | `id` / flag `opcional` | quién genera el avatar |
|---|---|---|
| **manual** *(predeterminada en promoavatar)* | *ninguna* | **tú**, sin el bot |
| estudio | `estudio` (`opcional: estudio`) | el bot abre el estudio, tú terminas |
| API | `gerar` (`opcional: api`) | el bot, mediante la API de HeyGen |
| créditos | `gerar-creditos` (`opcional: creditos`) | el bot, consumiendo créditos |
| navegador | `navega-avatar` (`opcional: navega`) | agente LLM que clona el `TEMPLATE-AVATAR` |

Dos de estos flags están documentados en el chat: **`| api`** (ver la sección
"OS AVATARES: SUA MÃO OU A API" de `HELP.md`) y **`| estudio`**. Los de
`creditos` y `navega` existen como fases en `flow.json`, pero **no están en
`HELP.md`**: el nombre del flag en el chat viene del campo `opcional`, así que confírmalo
antes de usarlo.

La ruta `navega-avatar` es la más costosa: **~17,8k tokens por público**, o ~214k en el
flujo de 12 (`docs/pipeline.md`).

**Lo que une las 5 rutas es el título.** En cualquiera de ellas, el video debe llamarse
`A<N>-<publico>-v1`. En la ruta manual, eso es 100% tu responsabilidad: es
el único contrato entre tú y el pipeline.

## Cambiar la imagen de portada por una propia

Las imágenes del reel se deciden en la fase de texto (sección `## IMAGENS`, regla
11b) y se generan con flux. Para poner una imagen **tuya** en su lugar, envía la **foto en el
chat con esta leyenda**; la leyenda de la imagen, no un mensaje aparte:

| leyenda | efecto |
|---|---|
| `capa: A#25 jovens` | IMAGEN 1 (la portada del feed) de ese público |
| `capa: A#25 *` | la misma imagen en **todos** los públicos del flujo |
| `capa: A#25 jovens 3` | cambia la IMAGEN 3, no la portada |
| `capa: A#25 jovens cover` | rellena **recortando** los lados |

El bot escribe la línea `arquivo: <caminho>` en la imagen correcta de
`textos/A<N>/<publico>.md`, y `preparar.py` usará tu foto en vez de
generar una.

**El modo predeterminado es `contain`:** la imagen cabe COMPLETA y el resto de la franja se rellena
con una copia borrosa de la misma. Una imagen que envíes **nunca se recorta sin que lo
pidas**: la imagen generada ya nace con el tamaño exacto, así que recortarla no quita nada; la
tuya ya viene compuesta, y si tiene texto o un rostro enmarcado, recortarla destruye el
trabajo. `cover` es para una imagen de fondo, sin texto.

### Cuándo enviarla: en el punto de control de la fase de texto

Es la única ventana en la que cambiar la portada es **gratis**: no se ha generado ningún avatar,
ninguna imagen pagada con flux, ningún renderizado. Una vez que se arma el reel, el comando
sigue escribiendo en el guion, pero el video solo cambia con `/refazer`; el bot te avisa
eso en la respuesta.

Si no adjuntas una foto, la rechaza en vez de guardar una línea vacía. Si ya tienes el
archivo en el disco, puedes escribir la ruta:

```
capa: A#25 jovens | arquivo=/caminho/da/imagem.png
```

## El título es el contrato

En el estudio, el video debe llamarse **exactamente**:

```
A<N>-<publico>-v1        ej.: A8-mulheres-v1
```

La descarga busca una coincidencia exacta de la cadena. Si el nombre es distinto, el video nunca
se encuentra y la fase vence en 90 minutos. El chat te envía el título listo junto con
cada guion, precisamente para que no tengas que escribirlo de memoria.

## Opciones de creación

| opción | predeterminado | qué hace |
|---|---|---|
| `--alvo=jovens` (repetible) o `\| alvos=a,b` | los 12 | solo esos públicos |
| `\| legenda=nao` | **CON subtítulos** | desactiva los subtítulos palabra por palabra del reel |
| `\| versao=N` | 1 | cambia el `-vN` del título del estudio |
| `\| de=<fase>` | — | empieza a mitad del proceso (ya hiciste el texto y/o el avatar) |
| `\| sombra` | — | muestra el plan, no lo pone en cola |

```
/promoavatar <assunto> --alvo=jovens | legenda=nao
```

**El valor predeterminado cambió (2026-08-07): los subtítulos están ACTIVADOS.** Una palabra a la vez, en mayúsculas, blancas, con la palabra clave en ámbar, en la base de la franja del avatar. El
diseño, las decisiones y dónde cambiar el color y el formato están en
`docs/legenda.md`.

> **Atención: implementación parcial.** El **motor** ya está listo y verificado en este
> repo (`scripts/legendas.py`, capa en `montar.py`, nodo en el template,
> `--sem-legenda` en `preparar.py`/`montar-reel.py`). Todavía falta el **flag del bot**:
> `| legenda=nao` solo tendrá efecto después del cambio en
> `inemaccbot/src/gateway/comandos-fluxo.ts` (`:282`, `:182-186`, `:336`) y del
> reinicio, que requiere que la cola esté vacía. Hasta entonces, quienes ejecuten desde la línea de comandos ya verán los subtítulos; desde el bot, todavía no.

### Subtítulos: qué viene de HeyGen y qué es nuestro

Esta opción controla **solo los subtítulos que dibuja nuestro editor**. No puede ver el
MP4 que viene de HeyGen: si el avatar llega con subtítulos **incrustados en los píxeles**,
permanecen durante todo el reel, incluso con la opción desactivada; el pipeline no tiene una etapa de
eliminación, máscara o inpainting.

**Los subtítulos del avatar se deciden en el estudio.** Lo que ofrece la API de HeyGen
(`video_status.get`):

| campo | qué es | ¿lo usamos? |
|---|---|---|
| `video_url` | MP4 **sin** subtítulos incrustados | sí, cuando no hay una versión subtitulada |
| `video_url_caption` | MP4 **con** subtítulos incrustados | **sí, cuando viene con un valor** |
| `caption_url` | subtítulos aparte (archivo), cuando existen | no |

La descarga del bot prefiere `video_url_caption` y usa `video_url` si no está disponible (`escolherUrl`, `inemaccbot/src/fila/tarefas/heygen.ts`). Es decir:
si grabaste con subtítulos en el estudio, el reel los incluye; si grabaste sin ellos, sale sin subtítulos.

**No se puede elegir nada al descargar.** La descarga es un `GET` a una URL
lista; no hay `?estilo=`, `?formato=`, `?idioma=`. Se probaron cinco endpoints de subtítulos
(`v1/video.caption`, `v2/video/caption`, `v1/video.subtitle`,
`v1/caption.list`, `v2/caption_styles`) y dieron **404**. El estilo, la fuente y la posición
de los subtítulos incrustados se deciden **en el estudio, antes de renderizar**; después
quedan en los píxeles y solo se pueden cambiar volviendo a grabar.

**Lo que se midió (2026-08-01, con la clave real de la cuenta):** los 25 videos completos
más recientes tenían `video_url_caption` nulo y `caption_url` vacío.

**Lo que se midió (2026-08-07, en `A35-tecnicos-v1`, `901cc529…`):** el video
**sí** tiene subtítulos cuando se descarga desde la interfaz, y aun así:

- `GET /v3/videos/{id}` responde **200** (la línea anterior decía 404: era el
  legado `v2/video/{id}`, que sigue respondiendo 404). La respuesta completa contiene `id`, `title`,
  `status`, `duration`, `created_at`, `completed_at`, `video_url`,
  `thumbnail_url`, `gif_url`, `video_page_url`. **No existe
  `captioned_video_url` ni `subtitle_url`**; los campos descritos en la documentación pública
  no aparecieron;
- `v1/video_status.get` para el mismo video: `caption_url` vacío, `video_url_caption`
  nulo.

Es decir: **los subtítulos activados en el estudio no llegan a la API**, ni como MP4 subtitulado
ni como archivo. El MP4 con subtítulos que descarga la interfaz es un render bajo demanda,
inaccesible por API. Esto descarta la hipótesis anterior de que `video_url_caption`
llegaría con un valor.

**Lo que sigue SIN medirse:** el comportamiento de un video creado mediante
`POST /v3/videos` **con `caption`**; ese es otro camino y bien podría devolver los campos de la documentación. Por ahora es irrelevante mientras la fase 2 sea humana: el bot
nunca llama al create.

**Consecuencia para el pipeline:** los subtítulos de un video ya renderizado solo se quitan del archivo local (ASR). Ver `docs/legenda.md`.

Consecuencias prácticas de grabar con subtítulos incrustados:

- quedan ubicados para el encuadre 16:9, no para la franja del medio del
  9:16: pueden quedar recortados o superponerse con la base;
- con la opción `legenda` activada, aparecen **dos** juegos de subtítulos. **Activar uno implica
  decidir desactivar el otro**: subtítulos en el estudio → reel sin `| legenda`; reel con
  `| legenda` → estudio sin subtítulos.

## Dónde cambiar cada cosa

La regla: **las decisiones sobre el público o la campaña van en este repo; la
identidad visual de la marca va en la skill.** La skill es global: modificarla cambia
TODOS los reels, incluidos los que se activan directamente desde el chat.

| quiero cambiar… | archivo | capa |
|---|---|---|
| el canal de un público | `flow.json` → `alvos.<publico>.canal` | dominio |
| el gancho de un público | `flow.json` → `alvos.<publico>.gatilho` | dominio |
| **cómo se escriben los guiones** | `prompts/fase1-texto.md` | dominio |
| **qué le pide este flujo al reel** | `prompts/reel-regras.md` + `templates/*.json` | dominio |
| **el clip CTA del final** | `cta/cta-9x16.mp4` — reemplaza el archivo | dominio |
| la ayuda del chat | `HELP.md` | dominio |
| **cómo se ARMA el reel** (colores, fuentes, posiciones, SFX, modos) | `~/.claude/skills/reel-edita-inema/SKILL.md` | skill (global) |
| lo que recibe el agente antes de llamar a la skill | `inemaccbot/prompts/reel.md` | bot |
| colas, tiempos de espera, modelo y esfuerzo | `inemaccbot/config/skills.json` | bot |

### El prompt del texto (`prompts/fase1-texto.md`)

Aquí viven, en este orden:

1. **CONTEXTO FIJO** — lo que el agente ya sabe (Nei y Tiza son los gestores de la
   comunidad), para que no mencione nombres sin función ni invente quiénes son.
2. **NO TOQUES LA MÁQUINA** — prohibición de instalar cualquier cosa. Un renderizado
   instaló un binario equivocado siguiendo una sugerencia del log y arruinó el siguiente renderizado.
3. **PASO CERO** — tesis central, elemento demostrable y elección explícita de
   un formato entre 11. Si no elige, el agente siempre recurre a dolor→solución→CTA,
   que es una fórmula de anuncio, y los anuncios no se comparten.
4. **TALLER DE GANCHOS** — cinco frases iniciales por público; cuatro se descartan
   POR ESCRITO. El criterio es la prueba de la brecha: después de la frase, ¿la
   persona necesita la siguiente para completar el sentido? Si la frase se sostiene sola, es
   una afirmación, no un gancho. Máximo 9 palabras.
5. **REGLAS DE ESCRITURA** — las 16 reglas: gancho en los 2 primeros segundos, dolor
   antes que solución, nombrar la profesión, beneficio antes que mecánica, frases
   cortas, promesa del tamaño adecuado, CTA imperativo, nada de marcadores de posición, nada
   de urgencia inventada, las SUPERPOSICIONES como guion VISUAL con los cuatro
   activadores (atención · retención · interacción · CTA), la brecha presente en lo que se DICE,
   valor completo antes de la marca, la última frase debe motivar a compartir y
   escribir para UNA persona concreta.
6. **El contrato de salida** — `{{pasta}}`, `RESULT:`/`ERRO:`.

Variables que inyecta el bot: `{{input}}` (el tema), `{{publicos}}` (los públicos
REALES del flujo), `{{pasta}}` (dónde guardar, ruta absoluta), `{{ref}}`, `{{saida}}`.

#### Tema de DEBATE: el prompt fija una postura

Un tema que llega como pregunta abierta ("¿esto es bueno o malo?", "¿qué opinas?") tenía
un resultado predecible: el agente explicaba ambos lados y terminaba con "lo importante es prepararse". Correcto, pero tibio: nadie comenta sobre algo que busca quedar bien con todos, y el video se mira y se olvida.

La causa no era falta de talento: las reglas 9 y 10 (no inventar datos, no inventar urgencia) hacían que el agente retrocediera hasta el punto medio, que es el único lugar donde tiene la certeza de no afirmar nada.

Entonces el prompt ahora le indica que **tome partido** en ese caso y que **escriba en el resumen
qué postura tomó y por qué**. Eso no flexibiliza las reglas 9 y 10: se permite opinar; inventar hechos, no.

**La postura que indiques prevalece sobre la suya.** Si escribes la tuya en el tema, la usa; el bloque solo existe cuando no la indicaste. Seguir indicando tu postura es lo mejor, junto con un hecho concreto (para que la línea PRUEBA no quede vacía) y la pregunta que quieres que respondan en los comentarios.

Como el resumen indica la postura elegida, puedes discrepar con ella **en el punto de control**, antes de generar cualquier avatar: `/refazer` cuesta un texto, no un renderizado.

### El estilo del reel: dos capas

Lo que ESTE pipeline le pide al reel está en `prompts/reel-regras.md` y en
`templates/*.json`: los cuatro activadores, el titular a partir del `{gatilho}` del
público y las franjas de cada layout.

La skill `reel-edita-inema` es la que sabe armarlo: composición apilada 9:16, colores,
fuentes, corte de silencios, subtítulos palabra por palabra, SFX. Modificarla cambia
toda la marca.

**Mejorar el reel, de lo más barato a lo más caro:** reemplazar el clip de `cta/`;
ajustar `prompts/reel-regras.md` o `templates/*.json`; y solo entonces modificar la skill.

## Lo que NO es de este repo (es de inemaccbot)

Este repo es **dominio**: *declara* el pipeline. Quien lo **ejecuta** es
`inemaccbot`. Buscar aquí algo que pertenece al otro repo es la pérdida de tiempo más común, así que aquí está la lista de lo que **no** está en este repo:

| qué | dónde está realmente |
|---|---|
| los comandos del chat (`/promoavatar`, `/status`, `/aprovar`, `/refazer`, `/cancelar`) y el parser de `\|` y `--` | el bot. Aquí solo existe `HELP.md`, que contiene el **texto** de la ayuda, no su código |
| el motor de fases: colas, intentos, tiempos de espera, la congelación al crear, el propio concepto de punto de control | `inemaccbot/config/skills.json`. `flow.json` solo lo declara; quien lo obedece es el bot |
| las tareas `heygen.gerar`, `heygen.estudio`, `heygen.baixar` — y `escolherUrl`, que decide entre el MP4 subtitulado y el limpio | `inemaccbot/src/fila/tarefas/heygen.ts` |
| el estado de los flujos y los avatares descargados (`state/artefatos/fluxos/A<N>/`) | el repo del bot |
| las carpetas de canal `~/projetos/yt-pub-<canal>/imports/videos` | regla derivada por el bot; aquí solo existe el **nombre** del canal |
| **cómo se ARMA el reel** (colores, fuentes, posiciones, corte de silencios, SFX) | la skill global `~/.claude/skills/reel-edita-inema/SKILL.md`; modificarla cambia TODOS los reels de la marca |
| el prompt que recibe el agente antes de llamar a la skill del reel | `inemaccbot/prompts/reel.md` |

**Regla práctica:** si el cambio afecta a *todos* los flujos, no corresponde a este repo. Si solo afecta a promoavatar, sí.

La excepción son los `scripts/*.py`: están aquí y son el motor del reel de este
dominio; se pueden ejecutar directamente (ver "Parámetros").

## Dónde defino el prompt y dónde defino los públicos

Son dos archivos distintos y es común confundirlos:

| quiero cambiar… | archivo |
|---|---|
| **cómo se escribe** (tono, reglas, ganchos, imágenes) | `prompts/fase1-texto.md` |
| **el dolor / el ángulo de un público** | `flow.json` → `alvos.<publico>.gatilho` |
| **a qué canal va** | `flow.json` → `alvos.<publico>.canal` |
| **el formato del archivo de salida** (FALA / SOBREPOSIÇÕES / IMAGENS / ESTRUTURA) | la skill `inemaclub-textos` |

`prompts/fase1-texto.md` indica usar la skill `inemaclub-textos` (línea 1), pero
**sobrescribe** su fórmula: "REGRAS DE ESCRITA (valem acima da fórmula
padrão da skill)". Es decir, la skill define la estructura; el prompt del flujo define las reglas.

Los 12 públicos son las claves de `alvos` en `flow.json`:

```
pessoacomum · jovens · profissionais · mulheres · empreendedores · tecnicos
40mais · 60mais · educadores · criadores · recolocacao · familia
```

Agregar un público = otra entrada con `canal` y `gatilho`. La clave se convierte en
el `<publico>` del título `A<N>-<publico>-v1`, así que **nada de tildes, espacios ni
guiones**.

## Cómo modificar: prompts, templates y públicos

Son las tres cosas que probablemente más querrás modificar. A todas se aplica la misma regla:
**todo queda congelado cuando nace el flujo**: los cambios se aplican a los PRÓXIMOS, y
ni siquiera `/refazer` los toma. Un flujo en curso no cambia de reglas a mitad del proceso.

### 1. Modificar el PROMPT (cómo se escriben los guiones)

Archivo: **`prompts/fase1-texto.md`**. Es el documento completo que la fase 1
entrega al agente. Estas son sus partes y lo que ocurre si modificas cada una:

| bloque | modifícalo para… | cuidado |
|---|---|---|
| CONTEXTO FIJO | cambiar a quién "ya conoce" el agente (hoy: Nei y Tiza como gestores) | un nombre sin función se vuelve decorativo; el bloque existe para evitarlo |
| PASO ZERO | cambiar la lista de los 11 formatos o qué cuenta como tesis/prueba | **los formatos son claves de `templates/mapa.json`**: si cambias el nombre aquí, cámbialo allá |
| TALLER DE GANCHOS | cambiar el criterio del gancho (hoy: prueba de la brecha, máximo 9 palabras) | es el bloque que más impacta el alcance |
| REGLAS DE ESCRITURA (las 16) | cambiar el tono, el CTA o lo que está prohibido | la 11b define el formato de la sección `## IMAGENS` que LEE el reel |
| contrato de salida | cambiar dónde se guarda y el `RESULT:`/`ERRO:` | si esto se rompe, se rompe toda la fase |

El bot inyecta cinco variables que **no deben desaparecer**: `{{input}}` (el
tema), `{{publicos}}` (los públicos reales del flujo), `{{pasta}}` (dónde guardar,
ruta absoluta), `{{ref}}` y `{{saida}}`.

Regla de convivencia con la skill: `inemaclub-textos` define la **estructura** del
archivo (FALA / SOBREPOSIÇÕES / IMAGENS / ESTRUTURA); este prompt define las
**reglas** y reemplaza las de la skill cuando hay desacuerdo. ¿Cambió la estructura del archivo?
Eso se hace en la skill y se aplica a todos, no solo a promoavatar.

Los otros dos prompts del repo siguen la misma lógica:
`prompts/fase-navega-avatar.md` (la ruta de navegador de la fase 2) y
`prompts/reel-regras.md` (lo que este flujo le pide al reel).

### 2. Modificar los TEMPLATES (el layout del reel)

Son dos archivos distintos y es común confundirlos:

**a) cambiar el aspecto de un layout** → edita `templates/<nombre>.json`.
El esquema siempre es el mismo:

```jsonc
{
  "nome": "empilhado-capa",
  "descricao": "…",                       // texto libre, ayuda a quien elige
  "canvas": { "largura": 1080, "altura": 1920 },
  "cores":  { "fundo": "#0E1116", "texto": "#FFFFFF", "acento": "#F5A623" },
  "faixas": {
    "topo": { "y": 0,    "altura": 704, "fonte": "imagens",
              "escurecer": 0.62,
              "headline": { "tamanho": 76, "peso": 900, "entrelinha": 1.04,
                            "margem_lateral": 48, "base_em": 56,
                            "maiusculas": true } },
    "meio": { "y": 704,  "altura": 608, "fonte": "avatar", "audio": true },
    "base": { "y": 1312, "altura": 608, "fonte": "texto", "painel": true,
              "hook": { "tamanho": 56, "peso": 800, "entrelinha": 1.16,
                        "margem_lateral": 56 } }
  },
  "transicao": { "flash": true, "duracao": 0.42,
                 "escala_entrada": 1.08, "pulso_max_s": 3.6 }
}
```

Tres reglas al modificar:

- **`y` + `altura` de las franjas deben sumar 1920.** No se apilan solas: `y` es la posición absoluta. Si falta una franja, queda negra.
- **`fonte` indica qué alimenta la franja**: `imagens` · `avatar` · `texto` (el `hook`)
  · `explicativo` (clip mudo en bucle). Cambiar `fonte` cambia el contrato con la
  fase de texto.
- **`escurecer`** es la capa oscura sobre la imagen para que el titular sea legible. Si
  lo bajas demasiado, el texto desaparece sobre las zonas claras de la foto.

Crear un layout nuevo = agregar otro `.json` a `templates/`, con `"nome"` igual al
nombre del archivo. Estará disponible de inmediato para `--template`; para incluirlo en
la selección automática, necesitas el paso (b).

**b) cambiar qué formato corresponde a cada layout** → edita `templates/mapa.json`.
Las claves son los formatos del PASO ZERO, **con y sin tilde** (`preparar.py`
busca el texto que escribió la fase de texto, así que las dos grafías existen a propósito):

```json
"mito versus realidade": "diptico",
"comparação": "diptico",
"comparacao": "diptico",
```

Un formato que no esté en el mapa **usa el predeterminado de la raíz de `flow.json`**:
no inventa un layout. Entonces, al crear un formato nuevo en el prompt, agrégalo aquí
en las dos grafías; de lo contrario, nunca usará el layout que querías.

**c) fijar el layout de un público**, ignorando el mapa → campo `template` dentro
del público en `flow.json` (ejemplo en la sección de parámetros). Tiene prioridad sobre el
mapa, pero no sobre `--template`.

### 3. Modificar los PÚBLICOS

Archivo: **`flow.json`**, clave `alvos`. Cada entrada tiene dos claves
obligatorias y una opcional:

```json
"empreendedores": {
  "canal": "lives24",
  "gatilho": "Transforme IA em redução de custos, vendas e novos negócios.",
  "template": "diptico"
}
```

| qué quiero | dónde |
|---|---|
| cambiar el **dolor/ángulo** de un público | `gatilho`: es lo que la regla 2 del prompt indica usar |
| cambiar **a dónde va** el reel | `canal`: se convierte en `~/projetos/yt-pub-<canal>/imports/videos` |
| fijar el **layout** de ese público | `template` (opcional) |
| **agregar** un público | otra entrada; la clave es el slug |
| **eliminar** un público | borra la entrada |
| ejecutar **solo algunos** sin modificar nada | `--alvo=jovens` o `\| alvos=a,b` al crear el flujo |

**La clave es un contrato, no una etiqueta.** Se convierte en:
el nombre del archivo `textos/A<N>/<publico>.md` · el título del video en el estudio
`A<N>-<publico>-v1` · el `--alvo` del reel · la `seed-key` de las imágenes. Por eso:
**minúsculas, sin tildes, espacios ni guiones** (por eso
`pessoa-comum` pasó a ser `pessoacomum`).

### 4. Modificar el DESTINO (dónde se entrega el reel)

El destino no es una ruta escrita en ningún sitio: se **deriva del `canal`
del público**, siempre con la misma regla:

```
<canal>  →  ~/projetos/yt-pub-<canal>/imports/videos
```

La separación es intencional: el dominio (este repo) solo indica el **nombre** del canal;
el bot se encarga de convertirlo en carpeta (`src/dominio/destinos.ts`), en un solo lugar. Si
`flow.json` guardara la ruta completa, sería una segunda copia de la lista de
canales, y las copias terminan divergiendo.

| quiero… | cómo |
|---|---|
| **cambiar el canal** de un público | edita `alvos.<publico>.canal` en `flow.json` |
| **crear un canal nuevo** | `mkdir -p ~/projetos/yt-pub-lives33/imports/videos`: eso es todo; el bot no necesita saberlo |
| **dos públicos en el mismo canal** | pon el mismo `canal` en ambos; nada lo impide |
| **cambiar la REGLA** (la carpeta base, `imports/videos`) | no es aquí: es `destinos.ts` del bot y afecta a TODOS los flujos |
| **entregar un reel suelto**, fuera del flujo | ejecuta manualmente `scripts/montar-reel.py --saida <caminho>` |

Mapa actual de los 12 (de `docs/canais-e-destinos.md`, reasignado el 2026-07-31):

```
empreendedores lives24  pessoacomum lives2   recolocacao lives3   mulheres  lives4
tecnicos       lives6   40mais      lives7   60mais      lives8   educadores lives9
criadores      lives11  jovens      lives22  profissionais lives23  familia  lives31
```

Como todo lo de aquí, **se aplica al PRÓXIMO flujo**: un flujo en curso no cambia de
destino a mitad del proceso.

## Los templates del reel

Están en `templates/` (indicado por `"templates_dir": "templates"` en
`flow.json`). Son 4 layouts, todos de 1080×1920, con fondo `#0E1116` y acento ámbar
`#F5A623`:

| template | parte superior | parte central | base | para qué sirve |
|---|---|---|---|---|
| **`empilhado-capa`** *(predeterminado de la raíz)* | imagen 704px + `headline` | avatar 608px (audio) | panel de texto 608px (`hook`) | portada de impacto: el formato original |
| **`empilhado-explicativo`** | imagen 704px + `headline` | avatar 608px (audio) | video explicativo 608px, en bucle y sin audio | cuando hay un video explicativo |
| **`diptico`** | imagen 960px + `headline` | avatar 960px | **no tiene** | mito×realidad y comparación: la imagen crea el contraste |
| **`imagem-plena`** | la imagen ocupa los 1920px | avatar recortado en la **parte superior derecha** | — | pregunta incómoda, predicción, consecuencia inesperada |

En `imagem-plena`, el avatar va arriba a la derecha por una regla de producción, no por
estética: **el pie de página está prohibido**; en producción, la interfaz de la red (subtítulos, @,
botones) cubre la esquina inferior y el avatar simplemente no se vería.

Cada franja declara un `fonte`: `imagens`, `avatar`, `texto` o `explicativo`. De
ahí viene el requisito de la regla 11b del prompt de texto: el `headline` va en la
franja superior y el `hook` va en el panel de la base. **Si un layout tiene base, pero
le falta `hook`, la base queda negra**: eso pasó en A#23 (`hook` en 0 de 8 imágenes).
Por eso el prompt indica que siempre se escriba `hook`, incluso en los layouts que no tienen base
(`diptico` e `imagem-plena`).

### Nadie elige el layout al renderizar

El layout depende de la línea `Formato escolhido:` que la fase de texto guarda en cada
`<publico>.md` (el PASO ZERO del prompt), es decir, de una decisión editorial que
**ya aprobaste en el punto de control**. `templates/mapa.json` hace la traducción:

```
"mito versus realidade" → diptico        "pergunta incômoda" → imagem-plena
"comparação"            → diptico        ...
```

**Prioridad** (resuelta por `preparar.py`):

```
--template explícito  ›  template del PÚBLICO en flow.json  ›  mapa.json  ›  template de la raíz
```

Un formato que no esté en el mapa usa el predeterminado; no inventa. En el A#19 real, la fase
de texto eligió **9 formatos distintos para 12 públicos**, así que esto produce
variación real sin que nadie decida nada en tiempo de renderizado.

## Parámetros

### En el chat (lo que documenta `HELP.md`)

| opción | efecto |
|---|---|
| `--alvo=jovens` (repetible) o `\| alvos=a,b` | solo esos públicos |
| `\| sombra` | muestra el plan, no lo pone en cola |
| `\| legenda` | subtítulos palabra por palabra (predeterminado: sin ellos) |
| `\| versao=N` | cambia el `-vN` del título |
| `\| de=baixar` | empieza a mitad del proceso (el texto y el avatar ya están listos) |
| `\| api` | el BOT genera el avatar (~US$ 1/min de la billetera prepaga) |
| `\| api \| sem-portao` | genera Y no se detiene para pedir aprobación |
| `/status A#N` · `/aprovar A#N` · `/refazer A#N <publico>` · `/cancelar A#N` | seguimiento |

### En los motores del reel (`scripts/`)

`montar-reel.py` — toda la fase 3:

| flag | |
|---|---|
| `--avatar` | **obligatorio**: el MP4 de HeyGen |
| `--ws` | **obligatorio**: workspace del reel |
| `--alvo` | público; se convierte en la `seed-key` de las imágenes (predeterminado `reel`) |
| `--textos` | el `<publico>.md`: de ahí sale la sección `## IMAGENS` |
| `--template` | reemplazo de layout (tiene prioridad sobre todo) |
| `--flow` / `--mapa` | de dónde resolver el template y el mapa |
| `--qualidade` | `high` (predeterminado) · `standard` · `draft` |
| `--cta` / `--sem-cta` | el clip de cierre (`cta/cta-9x16.mp4`) |
| `--pular-preparo` | reutiliza la preparación ya hecha en `--ws` |
| `--saida` | destino del MP4 |

`preparar.py` — solo la preparación (imágenes + transcripción). Tiene los mismos flags,
más `--explicativo`, `--sem-imagens`, `--sem-transcricao` y `--sem-montar`.

### Ejemplos

```bash
# reel predeterminado de un público: el layout se obtiene del mapa
python3 scripts/montar-reel.py \
  --avatar state/artefatos/fluxos/A34/A34-jovens-v1.mp4 \
  --ws /tmp/ws-A34-jovens --alvo jovens \
  --textos textos/A34/jovens.md --flow flow.json

# borrador económico, solo para revisar el encuadre
python3 scripts/montar-reel.py ... --qualidade draft --sem-cta

# forzar un layout, ignorando el mapa
python3 scripts/montar-reel.py ... --template imagem-plena

# cambiar el template/CTA sin volver a generar las imágenes
python3 scripts/montar-reel.py ... --pular-preparo --saida saida/A34-jovens.mp4

# con video explicativo en la franja de base
python3 scripts/preparar.py ... --alvo tecnicos \
  --explicativo saida/explicativo-tecnicos.mp4 --template empilhado-explicativo

# solo preparar ahora y armar después
python3 scripts/preparar.py ... --sem-montar
```

Fijar directamente el layout de un público en `flow.json` (tiene prioridad sobre el mapa,
pero no sobre `--template`):

```json
"empreendedores": {
  "canal": "lives24",
  "gatilho": "Transforme IA em redução de custos...",
  "template": "diptico"
}
```

## Atención: todo aquí se congela al crear el flujo

`flow.json`, los prompts y las opciones (`legenda`, `cta`) se **congelan cuando
nace el flujo**. Los cambios se aplican a los PRÓXIMOS: un flujo en curso no cambia
de reglas a mitad del proceso, por eso ni `/refazer` los toma.
