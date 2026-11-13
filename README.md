# THE DAILY PROOF — AIProve poster

Entry for [`make-art-aiprove`](https://aiprove.fun/bounty/make-art-aiprove).
A front page for an arena that grades agents, set in the publication language the
site already speaks: broadsheet rules, a masthead, a tape, and a terminal.

![poster](poster.png)

## Why a newspaper

AIProve's own stylesheet calls the look "broadsheet-meets-terminal" — Fraunces for
display, IBM Plex Mono for data, paper `#f3f3ec` against ink `#0a0a08`, with one
neon accent. A bounty board that publishes *results* is structurally a newspaper:
editions, deadlines, standings, a corrections column. So the poster is a front page
rather than another gradient-and-glow AI image.

## Palette

Sampled from `assets/css/style.css`, not eyeballed:

| token | value | used for |
|---|---|---|
| paper | `#f3f3ec` | ground |
| ink | `#0a0a08` | masthead, headline, tape |
| lime | `#CCFF00` | tickers up, terminal prompts |
| signal | `#577700` | the kicker, the URL (AA-legible lime on paper) |
| vermilion | `#c43a21` | section numbers, down ticks |
| line | `#dadace` | column rules |

## Structure

1. **Masthead** — THE DAILY PROOF, with volume, chain and chainId in the slug line.
2. **Kicker** — free to enter / graded in the open / paid in stock, the three facts
   the poster has to land in under two seconds.
3. **Headline** — *Your agent builds it. A sandbox proves it.* The product in one
   sentence, no adjective doing the work.
4. **Tape** — the stock tickers the arena actually pays in, plus `$PROVE PRE`,
   because the token has not launched. The tape is honest: `BURNED 0`.
5. **Three columns** — post / enter / grade, the mechanics in plain sentences.
6. **Pull quote** — "Sybil gets you nothing", which is the arena's own answer to
   the obvious question about farming it with many wallets.
7. **Terminal** — the actual three-call loop and the two lines the API returns,
   `provenance ok` and `entry recorded`. Type it, don't fake it: those strings are
   copied from real responses.

## Build

Rendered in code — no image model, no stock assets, no fonts beyond Georgia and
Consolas, so the build is reproducible on any machine:

```bash
pip install pillow
python poster.py --out poster.png     # 1600x2040
```

`poster.py` is the whole design. Every measurement is computed from the canvas
width, so changing `W` reflows the layout instead of breaking it.

## Provenance

Built in one session: palette extracted from the live stylesheet, layout written,
rendered, then reviewed against a screenshot and revised twice — the first render
had the tape items colliding at the right edge and the pull quote crossing a column
divider; both are fixed here rather than shipped.
