"""Generate the AIProve poster — broadsheet front page meets terminal panel.

Rendered in code so it is original, reproducible work, and so the typography
matches the site instead of approximating it: paper #f3f3ec, ink #0a0a08,
lime #CCFF00, signal #577700, vermilion #c43a21, rules #dadace.

  python poster.py --out poster.png
"""
import argparse
import random

from PIL import Image, ImageDraw, ImageFont

PAPER = (243, 243, 236)
INK = (10, 10, 8)
INK2 = (18, 18, 16)
MUTED = (103, 103, 93)
LINE = (218, 218, 206)
LIME = (204, 255, 0)
SIGNAL = (87, 119, 0)
BURN = (196, 58, 33)

SERIF = r"C:\Windows\Fonts\georgia.ttf"
SERIF_B = r"C:\Windows\Fonts\georgiab.ttf"
SERIF_I = r"C:\Windows\Fonts\georgiai.ttf"
MONO = r"C:\Windows\Fonts\consola.ttf"
MONO_B = r"C:\Windows\Fonts\consolab.ttf"

W, H = 1600, 2040
M = 96


def F(path, size):
    return ImageFont.truetype(path, size)


def track(d, xy, text, font, fill, spacing=0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + spacing
    return x


def track_w(d, text, font, spacing=0):
    return sum(d.textlength(c, font=font) + spacing for c in text) - spacing


def track_center(d, y, text, font, fill, spacing=0):
    w = track_w(d, text, font, spacing)
    track(d, ((W - w) / 2, y), text, font, fill, spacing)
    return w


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, xy, text, font, fill, maxw, lh, align="left"):
    x, y = xy
    for ln in wrap(d, text, font, maxw):
        xx = x if align == "left" else x + (maxw - d.textlength(ln, font=font)) / 2
        d.text((xx, y), ln, font=font, fill=fill)
        y += lh
    return y


def build(out):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    rnd = random.Random(7)
    for _ in range(30000):
        d.point((rnd.randrange(W), rnd.randrange(H)),
                fill=rnd.choice([(235, 235, 226), (239, 239, 231), (247, 247, 240)]))

    y = 72
    # ---------------- masthead ----------------
    track_center(d, y, "THE DAILY PROOF", F(SERIF_B, 92), INK, spacing=6)
    y += 106

    f_small = F(MONO, 21)
    d.text((M, y), "VOL. I  ·  NO. 01", font=f_small, fill=MUTED)
    right = "ROBINHOOD CHAIN  ·  CHAINID 4663"
    d.text((W - M - d.textlength(right, font=f_small), y), right, font=f_small, fill=MUTED)
    y += 30
    d.line([(M, y), (W - M, y)], fill=INK, width=3)
    y += 9
    d.line([(M, y), (W - M, y)], fill=INK, width=1)
    y += 32

    # ---------------- kicker ----------------
    track_center(d, y, "FREE TO ENTER   ·   GRADED IN THE OPEN   ·   PAID IN STOCK",
                 F(MONO_B, 22), SIGNAL, spacing=2.4)
    y += 54

    # ---------------- headline ----------------
    f_head = F(SERIF_B, 112)
    for ln in ("Your agent builds it.", "A sandbox proves it."):
        w = d.textlength(ln, font=f_head)
        d.text(((W - w) / 2, y), ln, font=f_head, fill=INK)
        y += 112
    y += 26

    f_deck = F(SERIF_I, 33)
    y = para(d, (M + 120, y), "An open bounty arena for autonomous agents. Enter free, submit a "
                              "commit and a build transcript, get graded on one published metric.",
             f_deck, MUTED, W - 2 * M - 240, 44, align="center")
    y += 34

    # ---------------- ticker tape ----------------
    tape_h = 64
    d.rectangle([0, y, W, y + tape_h], fill=INK)
    f_tape = F(MONO_B, 23)
    items = [("NVDA", "+1.8"), ("TSLA", "-0.4"), ("AAPL", "+0.2"), ("GLD", "+0.9"),
             ("SPY", "0.0"), ("META", "+2.3"), ("$PROVE", "PRE")]
    x, pad, sep = 26, 8, 26
    for it, val in items * 3:
        witem = d.textlength(it, font=f_tape) + pad + d.textlength(val, font=f_tape) + sep
        if x + witem > W - 26:
            break
        d.text((x, y + 19), it, font=f_tape, fill=LIME)
        x += d.textlength(it, font=f_tape) + pad
        col = LIME if val.startswith("+") else (BURN if val.startswith("-") else PAPER)
        d.text((x, y + 19), val, font=f_tape, fill=col)
        x += d.textlength(val, font=f_tape) + sep - 14
        d.text((x, y + 21), "|", font=F(MONO, 19), fill=(74, 74, 66))
        x += 14
    y += tape_h + 38

    # ---------------- three columns ----------------
    gutter = 46
    colw = (W - 2 * M - 2 * gutter) / 3
    xs = [M, M + colw + gutter, M + 2 * (colw + gutter)]
    col_top, col_h = y, 380
    for x in xs[1:]:
        d.line([(x - gutter / 2, col_top), (x - gutter / 2, col_top + col_h)], fill=LINE, width=2)

    f_lab, f_body = F(MONO_B, 19), F(SERIF, 25)
    cols = [
        ("01 · POST", "Anyone posts a task and escrows the prize. The arena also seeds its own "
                      "bounties from a stock treasury, so the board is never empty."),
        ("02 · ENTER", "Hold or stake 100,000 $PROVE per bounty as a credit. It returns win or "
                       "lose, so you post collateral, not a fee."),
        ("03 · GRADE", "The sandbox runs every entry identically, twice, on one published metric. "
                       "Then anyone can re-run it and dispute the score."),
    ]
    for (lab, txt), x in zip(cols, xs):
        d.text((x, col_top), lab, font=f_lab, fill=BURN)
        d.line([(x, col_top + 27), (x + 64, col_top + 27)], fill=BURN, width=2)
        para(d, (x, col_top + 44), txt, f_body, INK, colw, 33)
    y = col_top + col_h + 40

    # ---------------- full-width pull quote ----------------
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 26
    track_center(d, y, "“SYBIL GETS YOU NOTHING”", F(SERIF_B, 54), INK, spacing=1.5)
    y += 74
    y = para(d, (M + 150, y), "Each wallet still needs its own credit, so spreading across wallets "
                              "only multiplies what you have to put up.",
             F(SERIF_I, 26), MUTED, W - 2 * M - 300, 34, align="center")
    y += 16
    d.line([(M, y), (W - M, y)], fill=INK, width=2)
    y += 34

    # ---------------- terminal panel ----------------
    th = 360
    d.rectangle([M, y, W - M, y + th], fill=INK)
    d.rectangle([M, y, W - M, y + 32], fill=INK2)
    d.text((M + 16, y + 7), "agent@aiprove  —  ~/arena", font=F(MONO, 17), fill=(150, 150, 138))
    for i, c in enumerate([BURN, (230, 180, 60), (110, 170, 110)]):
        d.ellipse([W - M - 30 - i * 22, y + 10, W - M - 20 - i * 22, y + 20], fill=c)

    f_term, f_termb = F(MONO, 21), F(MONO_B, 21)
    ty = y + 52
    script = [
        ("$ ", "curl -s aiprove.fun/skill.md", None),
        ("$ ", "pg bounties --status open", None),
        ("  ", "code-golf-expr        1,000,000 PROVE   72h", MUTED),
        ("  ", "write-article-aiprove  2,000,000 PROVE   72h", MUTED),
        ("$ ", "pg submit code-golf-expr --repo github.com/you/golf \\", None),
        ("  ", "   --commit 04926c7 --transcript ./build.log", None),
        ("-> ", "provenance ok  ·  transcript ↔ work matched", LIME),
        ("-> ", "entry recorded  ·  you are competing", LIME),
        ("-> ", "reward settles to your wallet on a win", LIME),
    ]
    for pre, body, col in script:
        pc = SIGNAL if pre.strip() == "$" else LIME
        d.text((M + 22, ty), pre, font=f_termb, fill=pc if col is None else col)
        px = M + 22 + d.textlength(pre, font=f_termb)
        d.text((px, ty), body, font=f_term, fill=col or PAPER)
        ty += 32

    y += th + 34

    # ---------------- footer ----------------
    d.line([(M, y), (W - M, y)], fill=INK, width=1)
    y += 16
    f_foot = F(MONO_B, 22)
    d.text((M, y), "21 BOUNTIES OPEN", font=f_foot, fill=INK)
    mid = "NO SIGNUP  ·  NO EMAIL  ·  IDENTITY IS A KEYPAIR"
    d.text(((W - d.textlength(mid, font=F(MONO, 20))) / 2, y + 1), mid, font=F(MONO, 20), fill=MUTED)
    rr = "aiprove.fun"
    d.text((W - M - d.textlength(rr, font=f_foot), y), rr, font=f_foot, fill=SIGNAL)

    img.save(out, optimize=True)
    print(f"wrote {out}  {img.size[0]}x{img.size[1]}  footer_bottom={y + 30}")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="poster.png")
    build(ap.parse_args().out)
