"""NextGen DJ Curriculum - static SVG diagram library.
Every function returns an inline <svg> string themed through page CSS classes:
  st  = stroke ink     sm = stroke muted    sa = stroke accent   sb = stroke blue
  fa  = fill accent    fb = fill blue        fs = fill soft       fi = fill ink   fn = no fill
  tx  = text ink       tm = text muted        ts = small text      tk = mono label
"""
import math

def svg(w, h, body, label):
    return (f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}" '
            f'xmlns="http://www.w3.org/2000/svg">'
            '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0 0L10 5L0 10z" class="fi"/></marker></defs>'
            f'{body}</svg>')

def T(x, y, s, cls="tx", anchor="middle", size=None, weight=None):
    extra = ""
    if size: extra += f' font-size="{size}"'
    if weight: extra += f' font-weight="{weight}"'
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{extra}>{s}</text>'

def R(x, y, w, h, cls="fs st", rx=6):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>'

def L(x1, y1, x2, y2, cls="st", arrow=False, dash=False):
    a = ' marker-end="url(#ah)"' if arrow else ""
    d = ' stroke-dasharray="4 4"' if dash else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}"{a}{d}/>'

def C(x, y, r, cls="fa st"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" class="{cls}"/>'

def P(pts, cls="st fn", arrow=False):
    a = ' marker-end="url(#ah)"' if arrow else ""
    return f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" class="{cls}"{a}/>'

# ---------------------------------------------------------------- timing
def pulse():
    b = []
    bx, y = 30, 60
    for bar in range(4):
        x0 = bx + bar * 160
        b.append(R(x0, 30, 148, 60, "fs sm", 10))
        b.append(T(x0 + 74, 22, f"Bar {bar+1}", "tm", size=12))
        for beat in range(4):
            cx = x0 + 22 + beat * 35
            cls = "fa st" if beat == 0 else "fn st"
            b.append(C(cx, y, 11 if beat == 0 else 8, cls))
            b.append(T(cx, 112, str(beat + 1), "tx" if beat == 0 else "tm", size=13, weight=600 if beat == 0 else None))
    b.append(T(345, 140, "Count 1-2-3-4 and feel the big “1” at the start of every bar", "tm", size=12))
    return svg(680, 152, "".join(b), "Four bars of four beats with beat one highlighted")

def phrase():
    b = []
    # beat -> bar -> phrase hierarchy
    b.append(T(20, 24, "1 beat", "tx", "start", 13, 600))
    b.append(C(110, 20, 7, "fa st"))
    b.append(T(20, 64, "1 bar = 4 beats", "tx", "start", 13, 600))
    for i in range(4):
        b.append(C(150 + i * 22, 60, 7, "fa st" if i == 0 else "fn st"))
    b.append(T(20, 104, "1 phrase = 8 bars", "tx", "start", 13, 600))
    for i in range(8):
        b.append(R(150 + i * 58, 88, 52, 26, "fa st" if i == 0 else "fs st", 5))
        b.append(T(176 + i * 58, 106, str(i + 1), "tx", size=12))
    b.append(T(20, 160, "1 section = often 2 phrases", "tx", "start", 13, 600))
    for p in range(2):
        b.append(R(150 + p * 232, 136, 226, 36, "fs st", 6))
        b.append(T(263 + p * 232, 159, f"Phrase {p+1}  (8 bars, 32 beats)", "tm", size=12))
    return svg(620, 186, "".join(b), "A beat sits inside a bar, bars group into eight-bar phrases, phrases group into sections")

def sections(mix=True):
    segs = [("Intro", 16, 1.5), ("Build", 8, 3), ("Drop", 16, 5), ("Breakdown", 16, 2), ("Build", 8, 3.5), ("Drop", 16, 5), ("Outro", 16, 1.5)]
    total = sum(s[1] for s in segs)
    W, x0, x1 = 760, 20, 740
    sc = (x1 - x0) / total
    b = []
    x = x0
    pts = []
    for name, bars, e in segs:
        w = bars * sc
        cls = "fa st" if name == "Drop" else "fs st"
        b.append(R(x + 1, 110, w - 2, 40, cls, 6))
        b.append(T(x + w / 2, 135, name, "tx", size=12, weight=600))
        b.append(T(x + w / 2, 168, f"{bars} bars", "tm", size=11))
        y = 100 - e * 15
        pts += [(x + 2, y), (x + w - 2, y)]
        x += w
    b.append(P(pts, "sb fn"))
    b.append(T(x0, 18, "Energy", "tm", "start", 11))
    if mix:
        b.append(L(x0, 190, x0 + 16 * sc, 190, "sa", True))
        b.append(T(x0 + 8 * sc, 206, "mix in here", "tm", size=11))
        b.append(L(x1, 190, x1 - 16 * sc, 190, "sa", True))
        b.append(T(x1 - 8 * sc, 206, "mix out here", "tm", size=11))
    return svg(W, 214, "".join(b), "A typical club track laid out in sections with its energy line")

def intro_types():
    b = []
    rows = [("Beat intro", "drums from bar 1: easiest to beatmatch", "beat"),
            ("Beatless or FX intro", "no drums: start from where the beat lands", "fx"),
            ("Acapella intro", "voice only: align the vocal, or cue after it", "vox")]
    for i, (n, d, k) in enumerate(rows):
        y = 18 + i * 66
        b.append(T(16, y + 18, n, "tx", "start", 13, 600))
        b.append(T(16, y + 38, d, "tm", "start", 11))
        x0 = 330
        for j in range(48):
            x = x0 + j * 8.5
            if k == "beat":
                h = 26 if j % 4 == 0 else 10
            elif k == "fx":
                h = 4 + 14 * abs(math.sin(j / 5)) if j < 30 else (26 if j % 4 == 0 else 10)
            else:
                h = (6 + 12 * abs(math.sin(j * 1.7))) if j < 30 else (26 if j % 4 == 0 else 10)
            cls = "fb" if j < 30 and k != "beat" else "fa"
            b.append(f'<rect x="{x:.1f}" y="{y+26-h/2:.1f}" width="5" height="{h:.1f}" rx="2" class="{cls}"/>')
        if k != "beat":
            b.append(L(x0 + 30 * 8.5 - 2, y, x0 + 30 * 8.5 - 2, y + 52, "st", dash=True))
            b.append(T(x0 + 30 * 8.5 + 4, y + 2, "beat starts", "tm", "start", 10))
    return svg(750, 214, "".join(b), "Three types of intro drawn as simple waveforms")

def beatalign():
    b = []
    rows = [("In sync", 0, 0, "Same tempo, beats line up: sounds like one track"),
            ("Same tempo, out of line", 9, 0, "Nudge the jog wheel to pull it into line"),
            ("Different tempo", 0, 2.2, "Starts together, then drifts: fix the tempo")]
    for i, (n, off, drift, cap) in enumerate(rows):
        y = 20 + i * 78
        b.append(T(14, y + 4, n, "tx", "start", 13, 600))
        b.append(T(14, y + 22, cap, "tm", "start", 11))
        for t in range(2):
            ty = y + 36 + t * 18
            b.append(L(250, ty, 740, ty, "sm"))
            b.append(T(240, ty + 4, "A" if t == 0 else "B", "tm", "end", 11))
            for k in range(16):
                x = 260 + k * 30 + (off + drift * k if t == 1 else 0)
                if x > 742: continue
                b.append(L(x, ty - 7, x, ty + 7, "sa" if t == 1 else "st"))
    return svg(760, 250, "".join(b), "Two tracks shown as beat ticks: aligned, offset and drifting")

def tempo_middle():
    b = []
    xs = lambda bpm: 60 + (bpm - 130) * 15
    b.append(L(40, 120, 720, 120, "sm"))
    for bpm in range(130, 176, 5):
        b.append(L(xs(bpm), 115, xs(bpm), 125, "sm"))
        b.append(T(xs(bpm), 142, str(bpm), "tm", size=11))
    b.append(C(xs(140), 90, 12, "fs st")); b.append(T(xs(140), 66, "Track A 140", "tx", size=12, weight=600))
    b.append(C(xs(160), 90, 12, "fs st")); b.append(T(xs(160), 66, "Track B 160", "tx", size=12, weight=600))
    b.append(C(xs(150), 90, 12, "fa st")); b.append(T(xs(150), 30, "Meet at 150", "tx", size=13, weight=600))
    b.append(L(xs(140) + 14, 90, xs(150) - 16, 90, "st", True))
    b.append(L(xs(160) - 14, 90, xs(150) + 16, 90, "st", True))
    b.append(T(xs(145), 108, "A speeds up 7%", "tm", size=11))
    b.append(T(xs(155), 108, "B slows 6%", "tm", size=11))
    return svg(760, 160, "".join(b), "Two tracks at 140 and 160 BPM meeting at a middle tempo of 150")

def transition_track():
    b = []
    X = lambda t: 60 + t * 6.6
    Y = lambda bpm: 170 - (bpm - 130) * 3.4
    for bpm in (140, 150, 160, 170):
        b.append(L(55, Y(bpm), 730, Y(bpm), "sm", dash=True)); b.append(T(48, Y(bpm) + 4, str(bpm), "tm", "end", 11))
    pts = [(X(0), Y(140)), (X(40), Y(140)), (X(60), Y(170)), (X(100), Y(170))]
    b.append(P(pts, "sa fn"))
    b.append(R(X(0), 186, X(20) - X(0), 20, "fs st", 4)); b.append(T((X(0) + X(20)) / 2, 200, "mix in at 140", "tm", size=11))
    b.append(R(X(40), 186, X(60) - X(40), 20, "fb", 4)); b.append(T((X(40) + X(60)) / 2, 200, "let it change alone", "tx", size=11))
    b.append(R(X(80), 186, X(100) - X(80), 20, "fs st", 4)); b.append(T((X(80) + X(100)) / 2, 200, "mix out at 170", "tm", size=11))
    b.append(T(X(50) + 8, Y(155), "tempo ramp", "tx", "start", 12, 600))
    return svg(760, 214, "".join(b), "A transition track ramps from 140 to 170 BPM; mix in before the ramp and out after it")

# ---------------------------------------------------------------- mix control
def eqspectrum():
    b = []
    x0, x1 = 40, 720
    fx = lambda f: x0 + (math.log10(f) - math.log10(20)) / 3 * (x1 - x0)
    bands = [("LOW", 20, 250, "kick drum, sub bass, bassline"), ("MID", 250, 4000, "vocals, synths, snare, keys"), ("HIGH", 4000, 20000, "hi-hats, cymbals, air")]
    for i, (n, a, z, d) in enumerate(bands):
        cls = "fa" if i == 0 else ("fs" if i == 1 else "fb")
        b.append(f'<rect x="{fx(a):.1f}" y="40" width="{fx(z)-fx(a)-3:.1f}" height="70" rx="8" class="{cls}"/>')
        b.append(T((fx(a) + fx(z)) / 2, 70, n, "tx", size=14, weight=700))
        b.append(T((fx(a) + fx(z)) / 2, 92, d, "tx" if i != 2 else "tx", size=11))
    for f, s in [(20, "20 Hz"), (100, "100"), (250, "250"), (1000, "1 kHz"), (4000, "4k"), (10000, "10k"), (20000, "20 kHz")]:
        b.append(L(fx(f), 116, fx(f), 124, "sm")); b.append(T(fx(f), 140, s, "tm", size=11))
    b.append(T(380, 24, "Low pitch ← frequency → high pitch", "tm", size=12))
    return svg(760, 150, "".join(b), "The three EQ bands across the range of hearing and what lives in each")

def bassswap():
    b = []
    X = lambda bar: 70 + bar * 40
    b.append(T(14, 52, "Track A", "tx", "start", 12, 600)); b.append(T(14, 52 + 70, "Track B", "tx", "start", 12, 600))
    b.append(T(14, 68, "low EQ", "tm", "start", 11)); b.append(T(14, 138, "low EQ", "tm", "start", 11))
    b.append(P([(X(0), 40), (X(8), 40), (X(8), 80), (X(16), 80)], "st fn"))
    b.append(P([(X(0), 150), (X(8), 150), (X(8), 110), (X(16), 110)], "sa fn"))
    b.append(L(X(8), 24, X(8), 168, "sb", dash=True))
    b.append(T(X(8), 18, "swap on the phrase", "tx", size=12, weight=600))
    for bar in range(0, 17, 4):
        b.append(T(X(bar), 186, f"bar {bar+1}" if bar < 16 else "", "tm", size=10))
    b.append(T(X(4), 34, "full", "tm", size=10)); b.append(T(X(12), 74, "cut", "tm", size=10))
    b.append(T(X(4), 164, "cut", "tm", size=10)); b.append(T(X(12), 104, "full", "tm", size=10))
    return svg(740, 194, "".join(b), "A bass swap: one track's low EQ comes down exactly as the other's goes up, on a phrase")

def meter():
    b = []
    segs = 14
    for m, (lab, lit, note) in enumerate([("Too quiet", 5, "energy drops"), ("Just right", 10, "peaks touch amber"), ("Clipping", 14, "distortion")]):
        x = 60 + m * 230
        for s in range(segs):
            y = 200 - s * 13
            col = "fgood" if s < 9 else ("fwarn" if s < 12 else "fbad")
            on = s < lit
            b.append(f'<rect x="{x}" y="{y}" width="40" height="10" rx="2" class="{col if on else "fs"}"/>')
        b.append(T(x + 20, 230, lab, "tx", size=13, weight=600))
        b.append(T(x + 20, 248, note, "tm", size=11))
    b.append(L(108, 200 - 9 * 13 + 11, 120, 200 - 9 * 13 + 11, "st"))
    return svg(620, 258, "".join(b), "Three channel meters: too quiet, correct with occasional amber, and clipping into red")

def filtercurves():
    b = []
    def curve(x0, kind, title):
        out = [T(x0 + 150, 20, title, "tx", size=13, weight=600)]
        pts = []
        for i in range(0, 301, 6):
            f = i / 300
            if kind == "hp":
                g = 1 / (1 + math.exp(-(f - 0.45) * 18))
            else:
                g = 1 / (1 + math.exp((f - 0.55) * 18))
            pts.append((x0 + i, 140 - g * 95))
        poly = pts + [(x0 + 300, 140), (x0, 140)]
        out.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in poly)}" class="fa" opacity="0.6"/>')
        out.append(P(pts, "st fn"))
        out.append(L(x0, 140, x0 + 300, 140, "sm"))
        out.append(T(x0, 158, "low", "tm", "start", 11)); out.append(T(x0 + 300, 158, "high", "tm", "end", 11))
        cx = x0 + (135 if kind == "hp" else 165)
        out.append(L(cx, 40, cx, 140, "sb", dash=True)); out.append(T(cx, 176, "cut-off", "tm", size=11))
        out.append(T(x0 + (230 if kind == "hp" else 70), 80, "passes", "tx", size=12))
        out.append(T(x0 + (60 if kind == "hp" else 245), 128, "removed", "tm", size=11))
        return "".join(out)
    b.append(curve(30, "hp", "High-pass filter (turn right)"))
    b.append(curve(400, "lp", "Low-pass filter (turn left)"))
    return svg(730, 184, "".join(b), "High-pass and low-pass filter shapes with their cut-off points")

def xfcurve():
    b = []
    def panel(x0, kind, title):
        out = [T(x0 + 130, 18, title, "tx", size=13, weight=600)]
        a, c = [], []
        for i in range(0, 261, 5):
            f = i / 260
            if kind == "smooth":
                ga, gc = math.cos(f * math.pi / 2), math.sin(f * math.pi / 2)
            else:
                ga = 1 if f < 0.95 else max(0, (1 - f) / 0.05)
                gc = 1 if f > 0.05 else f / 0.05
            a.append((x0 + i, 130 - ga * 95)); c.append((x0 + i, 130 - gc * 95))
        out.append(P(a, "st fn")); out.append(P(c, "sa fn"))
        out.append(L(x0, 130, x0 + 260, 130, "sm"))
        out.append(T(x0, 150, "fader left", "tm", "start", 11)); out.append(T(x0 + 260, 150, "fader right", "tm", "end", 11))
        return "".join(out)
    b.append(panel(30, "smooth", "Smooth curve: for blending"))
    b.append(panel(380, "sharp", "Sharp curve: for scratching"))
    b.append(L(40, 172, 60, 172, "st")); b.append(T(66, 176, "deck A", "tm", "start", 11))
    b.append(L(130, 172, 150, 172, "sa")); b.append(T(156, 176, "deck B", "tm", "start", 11))
    return svg(680, 184, "".join(b), "Crossfader curves: a smooth crossover versus a sharp cut")

# ---------------------------------------------------------------- signal flow
def flow(items, label, sub=None, w=760):
    n = len(items)
    gap = 26
    bw = (w - 40 - gap * (n - 1)) / n
    b = []
    for i, it in enumerate(items):
        name, note = it if isinstance(it, tuple) else (it, "")
        x = 20 + i * (bw + gap)
        cls = "fa st" if i in (sub or []) else "fs st"
        b.append(R(x, 30, bw, 60, cls, 10))
        b.append(T(x + bw / 2, 56, name, "tx", size=13, weight=600))
        if note: b.append(T(x + bw / 2, 76, note, "tm", size=11))
        if i < n - 1:
            b.append(L(x + bw + 3, 60, x + bw + gap - 3, 60, "st", True))
    return svg(w, 110, "".join(b), label)

def signal1():
    return flow([("Storage", "USB, laptop"), ("Player", "deck or software"), ("Mixer", "blends the decks"), ("Output", "speakers, recorder")],
                "Signal flow from storage to player to mixer to speakers", [2])

def signal2():
    items = [("Input", "line or phono"), ("Trim", "gain"), ("EQ", "hi mid low"), ("Fader", "channel"), ("X-fader", "if assigned"), ("Master", "level")]
    b = []
    w = 780
    bw, gap = 104, 22
    for i, (n, d) in enumerate(items):
        x = 14 + i * (bw + gap)
        b.append(R(x, 30, bw, 56, "fa st" if n in ("Trim", "EQ") else "fs st", 10))
        b.append(T(x + bw / 2, 54, n, "tx", size=13, weight=600)); b.append(T(x + bw / 2, 73, d, "tm", size=11))
        if i < len(items) - 1: b.append(L(x + bw + 3, 58, x + bw + gap - 3, 58, "st", True))
    # cue tap after EQ
    xe = 14 + 2 * (bw + gap) + bw / 2
    b.append(L(xe, 88, xe, 128, "sb", True)); b.append(R(xe - 62, 132, 124, 36, "fb", 8)); b.append(T(xe, 155, "CUE to headphones", "tx", size=11, weight=600))
    xm = 14 + 5 * (bw + gap) + bw / 2
    outs = ["Master out", "Booth out", "Rec out"]
    for j, o in enumerate(outs):
        ox = xm - 190 + j * 120
        b.append(L(xm, 88, ox + 50, 130, "st", True))
        b.append(R(ox, 132, 100, 36, "fs st", 8)); b.append(T(ox + 50, 155, o, "tx", size=11))
    return svg(w, 180, "".join(b), "Inside a mixer channel: input, trim, EQ, fader, crossfader, master, with the cue tapped before the fader")

def signal3():
    b = []
    row = [("Trim", 0), ("EQ", 0), ("Colour FX", 1), ("Channel fader", 0), ("Beat FX", 2), ("Master", 0)]
    bw, gap = 104, 22
    for i, (n, k) in enumerate(row):
        x = 14 + i * (bw + gap)
        cls = "fa st" if k == 1 else ("fb st" if k == 2 else "fs st")
        b.append(R(x, 40, bw, 50, cls, 10)); b.append(T(x + bw / 2, 70, n, "tx", size=12, weight=600))
        if i < len(row) - 1: b.append(L(x + bw + 3, 65, x + bw + gap - 3, 65, "st", True))
    b.append(T(14 + 2 * (bw + gap) + bw / 2, 28, "pre-fader", "tm", size=11))
    b.append(T(14 + 4 * (bw + gap) + bw / 2, 28, "post-fader", "tm", size=11))
    # send/return
    xs_ = 14 + 3 * (bw + gap) + bw + 11
    b.append(L(xs_, 65, xs_, 128, "sb", True)); b.append(R(xs_ + 20, 118, 170, 40, "fs st", 8))
    b.append(T(xs_ + 105, 143, "external FX unit", "tx", size=11))
    b.append(T(xs_ - 6, 112, "send", "tm", "end", 11))
    b.append(L(xs_ + 190, 138, xs_ + 220, 138, "sb")); b.append(L(xs_ + 220, 138, xs_ + 220, 96, "sb", True))
    b.append(T(xs_ + 226, 124, "return", "tm", "start", 11))
    return svg(780, 168, "".join(b), "Where effects sit: colour FX before the channel fader, beat FX after it, and a send-return loop to an external unit")

def headphones():
    b = []
    b.append(R(20, 30, 120, 44, "fs st", 8)); b.append(T(80, 57, "Deck 1", "tx", size=12, weight=600))
    b.append(R(20, 100, 120, 44, "fs st", 8)); b.append(T(80, 127, "Deck 2", "tx", size=12, weight=600))
    b.append(R(220, 50, 150, 74, "fa st", 10)); b.append(T(295, 82, "Mixer", "tx", size=13, weight=600)); b.append(T(295, 102, "CUE buttons choose", "tm", size=11))
    b.append(L(142, 52, 218, 72, "st", True)); b.append(L(142, 122, 218, 102, "st", True))
    b.append(R(470, 20, 170, 44, "fs st", 8)); b.append(T(555, 47, "Speakers: crowd hears", "tx", size=11))
    b.append(R(470, 110, 170, 44, "fb", 8)); b.append(T(555, 137, "Headphones: only you", "tx", size=11, weight=600))
    b.append(L(372, 70, 468, 44, "st", True)); b.append(T(420, 46, "master", "tm", size=11))
    b.append(L(372, 104, 468, 130, "sb", True)); b.append(T(420, 132, "cue", "tm", size=11))
    b.append(T(330, 176, "Headphone MIX knob: left = cue only, right = master only, middle = both", "tm", size=11))
    return svg(660, 188, "".join(b), "The cue buttons send a deck to the headphones while the master goes to the speakers")

def controller():
    b = []
    W, H = 800, 400
    b.append(R(60, 50, 680, 280, "fs st", 22))
    def lab(x1, y1, x2, y2, text, anchor):
        b.append(L(x1, y1, x2, y2, "sm"))
        b.append(C(x1, y1, 3, "fi"))
        b.append(T(x2 + (4 if anchor == "start" else -4), y2 + 4, text, "tx", anchor, 12, 600))
    # decks
    for side, x0 in (("L", 80), ("R", 540)):
        cx = x0 + 100
        b.append(C(cx, 170, 82, "fn st")); b.append(C(cx, 170, 30, "fs st")); b.append(C(cx, 170, 3, "fi"))
        tx = x0 + 196 if side == "L" else x0 - 14
        b.append(R(tx, 90, 14, 140, "fn st", 6)); b.append(R(tx - 3, 150, 20, 12, "fa st", 3))
        b.append(C(x0 + 22, 296, 14, "fa st")); b.append(C(x0 + 58, 296, 14, "fn st"))
        for k in range(4):
            b.append(R(x0 + 90 + k * 28, 284, 22, 22, "fb", 4))
    # mixer
    mx = 320
    b.append(R(mx, 66, 160, 250, "fn st", 12))
    b.append(C(mx + 80, 90, 11, "fn st"))
    rows = [(118, "TRIM"), (146, "HI"), (172, "MID"), (198, "LOW"), (226, "FILTER")]
    for y, name in rows:
        for cx in (mx + 34, mx + 126):
            b.append(C(cx, y, 9, "fa st" if name == "TRIM" else ("fb st" if name == "FILTER" else "fn st")))
        b.append(T(mx + 80, y + 4, name, "tm", size=9, weight=600))
    for cx in (mx + 34, mx + 126):
        b.append(R(cx - 13, 244, 26, 12, "fb", 3))
        b.append(R(cx - 5, 262, 10, 34, "fn st", 4)); b.append(R(cx - 10, 272, 20, 8, "fi", 2))
    b.append(T(mx + 80, 254, "CUE", "tm", size=9, weight=600))
    b.append(T(mx + 80, 284, "FADERS", "tm", size=9, weight=600))
    b.append(R(mx + 45, 302, 70, 8, "fn st", 4)); b.append(R(mx + 74, 298, 12, 16, "fi", 2))
    # labels: left side
    lab(155, 120, 120, 26, "Jog wheel", "end")
    lab(283, 105, 250, 26, "Tempo slider", "end")
    lab(102, 308, 70, 370, "Play", "end")
    lab(138, 308, 150, 370, "Cue", "start")
    lab(240, 306, 250, 370, "Pads: hot cues, loops", "start")
    lab(mx + 80, 79, mx + 140, 26, "Browse and load", "start")
    lab(mx + 34, 118, mx + 25, 26, "Trim", "end")
    lab(mx + 80, 310, mx + 80, 370, "Crossfader", "start")
    lab(mx + 126, 279, 520, 370, "Channel EQ, filter, cue and fader", "start")
    return svg(W, H, "".join(b), "A generic two-deck DJ controller with its main controls labelled")

# ---------------------------------------------------------------- transitions
def blend(mix_in, together, mix_out, title=None, swap=True):
    total = mix_in + together + mix_out + 1
    X = lambda p: 70 + p * (640 / total)
    b = []
    for p in range(total + 1):
        b.append(L(X(p), 30, X(p), 150, "sm", dash=True))
    for p in range(total):
        b.append(T((X(p) + X(p + 1)) / 2, 168, f"phrase {p+1}", "tm", size=10))
    top, bot = 44, 138
    a = [(X(0), top), (X(1 + mix_in + together), top), (X(total), bot)]
    if mix_out == 0:
        a = [(X(0), top), (X(1 + mix_in), top), (X(1 + mix_in), bot), (X(total), bot)]
    bpts = [(X(0), bot), (X(1), bot), (X(1 + mix_in), top), (X(total), top)]
    b.append(P(a, "st fn")); b.append(P(bpts, "sa fn"))
    b.append(T(64, top + 4, "full", "tm", "end", 11)); b.append(T(64, bot + 4, "off", "tm", "end", 11))
    if swap:
        sx = X(1 + mix_in) if mix_out == 0 else X(1 + mix_in + (together // 2 if together else 0))
        b.append(C(sx, 18, 9, "fb")); b.append(T(sx, 22, "EQ", "tinv", size=8, weight=700))
        b.append(T(sx + 14, 22, "bass swap", "tm", "start", 10))
    b.append(L(560, 186, 580, 186, "st")); b.append(T(586, 190, "outgoing", "tm", "start", 10))
    b.append(L(640, 186, 660, 186, "sa")); b.append(T(666, 190, "incoming", "tm", "start", 10))
    return svg(740, 196, "".join(b), title or "Fader levels of the outgoing and incoming tracks across phrases")

def cutdiag(kind="straight"):
    X = lambda p: 70 + p * 160
    b = []
    for p in range(5): b.append(L(X(p), 30, X(p), 150, "sm", dash=True))
    top, bot = 44, 138
    if kind == "straight":
        b.append(P([(X(0), top), (X(2), top), (X(2), bot), (X(4), bot)], "st fn"))
        b.append(P([(X(0), bot), (X(2), bot), (X(2), top), (X(4), top)], "sa fn"))
        b.append(T(X(2), 22, "cut on beat 1 of the phrase", "tx", size=12, weight=600))
    elif kind == "beatcut":
        b.append(P([(X(0), top), (X(2), top), (X(2), bot), (X(4), bot)], "st fn"))
        pts = [(X(0), bot), (X(1), bot)]
        for k in range(4):
            x = X(1) + k * 40
            pts += [(x, bot), (x, 90), (x + 14, 90), (x + 14, bot)]
        pts += [(X(2), bot), (X(2), top), (X(4), top)]
        b.append(P(pts, "sa fn"))
        b.append(T(X(1.5), 22, "tease: flick in on the beat", "tx", size=12, weight=600))
    elif kind == "dropin":
        b.append(P([(X(0), top), (X(2), top), (X(2), bot), (X(4), bot)], "st fn"))
        b.append(P([(X(0), bot), (X(2), bot), (X(2), top), (X(4), top)], "sa fn"))
        b.append(C(X(2), top, 7, "fa st"))
        b.append(T(X(2), 22, "press play and switch at the same moment", "tx", size=12, weight=600))
    elif kind == "quickfade":
        b.append(P([(X(0), top), (X(2), top), (X(2.35), bot), (X(4), bot)], "st fn"))
        b.append(P([(X(0), bot), (X(2), bot), (X(2), top), (X(4), top)], "sa fn"))
        b.append(T(X(2.2), 22, "drop in, then pull the old fader down fast", "tx", size=12, weight=600))
    for p in range(4): b.append(T((X(p) + X(p + 1)) / 2, 168, f"phrase {p+1}", "tm", size=10))
    b.append(L(560, 186, 580, 186, "st")); b.append(T(586, 190, "outgoing", "tm", "start", 10))
    b.append(L(640, 186, 660, 186, "sa")); b.append(T(666, 190, "incoming", "tm", "start", 10))
    b.append(T(64, top + 4, "full", "tm", "end", 11)); b.append(T(64, bot + 4, "off", "tm", "end", 11))
    return svg(740, 196, "".join(b), "Fader movement for a cut-style transition")

# ---------------------------------------------------------------- scratching
SCR = {
    # list of (beat, position 0-1) points over 4 beats, fader open spans in beats
    "baby": ([(0, 0), (.5, 1), (1, 0), (1.5, 1), (2, 0), (2.5, 1), (3, 0), (3.5, 1), (4, 0)], [(0, 4)]),
    "dropcut": ([(0, 0), (1, 1), (1.6, 1), (2, 0), (3, 1), (3.6, 1), (4, 0)], [(0, 1), (2, 3)]),
    "forwardcut": ([(0, 0), (.4, 1), (1, 0), (1.4, 1), (2, 0), (2.4, 1), (3, 0), (3.4, 1), (4, 0)], [(0, .4), (1, 1.4), (2, 2.4), (3, 3.4)]),
    "dropscratch": ([(0, 0), (1, .7), (1.5, 0), (2, .7), (2.5, 0), (3, .7), (3.5, 0), (4, .7)], [(0, 4)]),
    "chirp": ([(0, 0), (.5, 1), (1, 0), (1.5, 1), (2, 0), (2.5, 1), (3, 0), (3.5, 1), (4, 0)], [(0, .35), (.65, 1.35), (1.65, 2.35), (2.65, 3.35), (3.65, 4)]),
    "stab": ([(0, 0), (.25, 1), (1, 0), (1.25, 1), (2, 0), (2.25, 1), (3, 0), (3.25, 1), (4, 0)], [(0, .25), (1, 1.25), (2, 2.25), (3, 3.25)]),
    "tear": ([(0, 0), (.25, .5), (.45, .5), (.7, 1), (1, .5), (1.2, .5), (1.5, 0), (2, 0), (2.25, .5), (2.45, .5), (2.7, 1), (3, .5), (3.2, .5), (3.5, 0), (4, 0)], [(0, 4)]),
    "scribble": ([(i / 8, (0.12 if i % 2 else 0)) for i in range(33)], [(0, 4)]),
    "transform": ([(0, 0), (2, 1), (4, 0)], [(0.2, .45), (.7, .95), (1.2, 1.45), (1.7, 1.95), (2.2, 2.45), (2.7, 2.95), (3.2, 3.45), (3.7, 3.95)]),
    "flare": ([(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)], [(0, .3), (.4, .6), (.7, 1.3), (1.4, 1.6), (1.7, 2.3), (2.4, 2.6), (2.7, 3.3), (3.4, 3.6), (3.7, 4)]),
}

def scratch(kind):
    pts, opens = SCR[kind]
    X = lambda beat: 70 + beat * 160
    Y = lambda pos: 120 - pos * 80
    b = []
    for k in range(5):
        b.append(L(X(k), 30, X(k), 128, "sm", dash=True))
        if k < 4: b.append(T(X(k) + 80, 22, f"beat {k+1}", "tm", size=10))
    b.append(L(X(0), 128, X(4), 128, "sm"))
    b.append(T(60, Y(1) + 4, "end", "tm", "end", 10)); b.append(T(60, Y(0) + 4, "start", "tm", "end", 10))
    b.append(T(14, 76, "sound", "tm", "start", 10))
    b.append(P([(X(a), Y(p)) for a, p in pts], "st fn thick"))
    b.append(T(60, 154, "fader", "tm", "end", 10))
    b.append(R(X(0), 142, X(4) - X(0), 18, "fs", 4))
    for a, z in opens:
        b.append(R(X(a), 142, X(z) - X(a), 18, "fa", 4))
    b.append(R(X(0) + 380, 170, 14, 10, "fa", 2)); b.append(T(X(0) + 400, 179, "fader open (you hear it)", "tm", "start", 10))
    return svg(740, 188, "".join(b), f"Scratch notation for the {kind} scratch: hand movement above, crossfader below")

# ---------------------------------------------------------------- harmony
KEYS_A = ["Ab m", "Eb m", "Bb m", "F m", "C m", "G m", "D m", "A m", "E m", "B m", "F# m", "Db m"]
KEYS_B = ["B", "F#", "Db", "Ab", "Eb", "Bb", "F", "C", "G", "D", "A", "E"]

def camelot(sel=8):
    cx, cy = 200, 200
    b = []
    good = {(sel, "A"), (sel % 12 + 1, "A"), ((sel - 2) % 12 + 1, "A"), (sel, "B")}
    for i in range(12):
        n = i + 1
        a0 = math.radians(-90 + i * 30 - 15); a1 = math.radians(-90 + i * 30 + 15)
        for ring, (r0, r1), keys in (("B", (130, 190), KEYS_B), ("A", (70, 128), KEYS_A)):
            p = [(cx + r1 * math.cos(a0), cy + r1 * math.sin(a0)), (cx + r1 * math.cos(a1), cy + r1 * math.sin(a1)),
                 (cx + r0 * math.cos(a1), cy + r0 * math.sin(a1)), (cx + r0 * math.cos(a0), cy + r0 * math.sin(a0))]
            cls = "fa st" if (n, ring) == (sel, "A") else ("fb st" if (n, ring) in good else "fs st")
            b.append(f'<path d="M{p[0][0]:.1f},{p[0][1]:.1f} A{r1},{r1} 0 0 1 {p[1][0]:.1f},{p[1][1]:.1f} L{p[2][0]:.1f},{p[2][1]:.1f} A{r0},{r0} 0 0 0 {p[3][0]:.1f},{p[3][1]:.1f} Z" class="{cls}"/>')
            am = math.radians(-90 + i * 30); rm = (r0 + r1) / 2
            tx, ty = cx + rm * math.cos(am), cy + rm * math.sin(am)
            b.append(T(f"{tx:.1f}", f"{ty-1:.1f}", f"{n}{ring}", "tx", size=12, weight=700))
            b.append(T(f"{tx:.1f}", f"{ty+12:.1f}", keys[i], "tm", size=9))
    b.append(T(cx, cy - 4, "inner: minor", "tm", size=10)); b.append(T(cx, cy + 10, "outer: major", "tm", size=10))
    # legend
    b.append(R(430, 140, 16, 16, "fa st", 3)); b.append(T(452, 153, f"Playing now: {sel}A ({KEYS_A[sel-1]})", "tx", "start", 13, 600))
    b.append(R(430, 172, 16, 16, "fb st", 3)); b.append(T(452, 185, "Safe next keys: one step round, or straight across", "tx", "start", 12))
    b.append(T(452, 216, f"{(sel-2)%12+1}A, {sel%12+1}A, {sel}B", "tm", "start", 12))
    return svg(760, 400, "".join(b), "The Camelot wheel with a playing key and its compatible neighbours highlighted")

# ---------------------------------------------------------------- structure
def energy(shape="build"):
    shapes = {
        "build": [1, 1.5, 2, 2.5, 3, 3, 3.5, 4, 4, 4.5, 5, 5],
        "coaster": [2, 3, 4, 5, 3, 2, 3, 4, 5, 4, 3, 5],
        "story": [2, 2.5, 3, 4, 4.5, 3, 2, 3.5, 4.5, 5, 4, 2.5],
    }
    v = shapes[shape]
    X = lambda i: 60 + i * 58
    Y = lambda e: 170 - e * 28
    b = []
    for e in range(1, 6):
        b.append(L(55, Y(e), 700, Y(e), "sm", dash=True)); b.append(T(46, Y(e) + 4, str(e), "tm", "end", 11))
    pts = [(X(i), Y(e)) for i, e in enumerate(v)]
    b.append(P(pts, "sa fn thick"))
    for x, y in pts: b.append(C(x, y, 5, "fa st"))
    b.append(T(30, 24, "energy 1-5", "tm", "start", 11))
    for i in range(12): b.append(T(X(i), 192, f"T{i+1}", "tm", size=10))
    return svg(720, 200, "".join(b), f"Energy level of each track across a set ({shape} shape)")

def loopdiag():
    b = []
    for row, (title, start, length, ok) in enumerate([("Good loop: starts on beat 1, a full phrase", 0, 8, True), ("Bad loop: starts mid-bar and cuts the phrase short", 2.5, 3, False)]):
        y = 26 + row * 92
        b.append(T(20, y, title, "tx", "start", 13, 600))
        for bar in range(8):
            b.append(R(20 + bar * 88, y + 14, 84, 30, "fs st", 5)); b.append(T(62 + bar * 88, y + 34, f"bar {bar+1}", "tm", size=11))
        x0 = 20 + start * 88; x1 = x0 + length * 88 - 4
        b.append(f'<path d="M{x0},{y+52} v12 H{x1} v-12" class="{"sa" if ok else "sbad"} fn thick"/>')
        b.append(L(x1, y + 64, x0 + 6, y + 64, "sa" if ok else "sbad", True))
        b.append(T((x0 + x1) / 2, y + 80, "loop" if ok else "glitch at the join", "tx" if ok else "tm", size=11))
    return svg(740, 210, "".join(b), "A loop that fits the phrase versus a loop that starts off the bar")

def slip():
    b = []
    X = lambda beat: 60 + beat * 40
    b.append(T(14, 40, "you hear", "tm", "start", 11)); b.append(T(14, 100, "track runs", "tm", "start", 11))
    b.append(L(X(0), 96, X(16), 96, "st", True))
    for k in range(17): b.append(L(X(k), 90, X(k), 102, "sm"))
    segs = [(0, 4, "fs st", "normal"), (4, 5, "fa st", "loop"), (5, 6, "fa st", "loop"), (6, 7, "fa st", "loop"), (7, 8, "fa st", "loop"), (8, 16, "fs st", "normal")]
    for a, z, c, n in segs:
        b.append(R(X(a) + 1, 24, X(z) - X(a) - 2, 28, c, 5)); b.append(T((X(a) + X(z)) / 2, 43, n, "tx", size=11))
    b.append(L(X(8), 56, X(8), 86, "sb", True)); b.append(T(X(8) + 6, 72, "let go: jumps to where the track would be", "tm", "start", 11))
    return svg(740, 116, "".join(b), "Slip mode: a beat-repeat loop plays while the track keeps running underneath")

def tappause(kind="tap"):
    b = []
    X = lambda s: 70 + s * 40
    rows = []
    if kind == "tap":
        rows = [("Original", [1] * 16), ("Tap paused", [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1])]
    else:
        rows = [("Deck A", [1 if i % 2 == 0 else 0 for i in range(16)]), ("Deck B, half a beat later", [0 if i % 2 == 0 else 1 for i in range(16)]),
                ("You hear", [2] * 16)]
    for r, (name, cells) in enumerate(rows):
        y = 20 + r * 44
        b.append(T(60, y + 22, name, "tx", "end", 11, 600))
        for s, v in enumerate(cells):
            cls = "fs" if v == 0 else ("fa" if v == 1 else ("fb" if s % 2 else "fa"))
            b.append(R(X(s) + 2, y + 6, 34, 26, cls, 4))
    return svg(740, 20 + len(rows) * 44 + 10, "".join(b), "Beat grid showing which slices of the track are heard")

def quantise():
    b = []
    X = lambda beat: 60 + beat * 80
    for k in range(9):
        b.append(L(X(k), 30, X(k), 130, "sm"))
        b.append(T(X(k), 146, str(k % 4 + 1), "tm", size=10))
    for k in range(8):
        h = 80 if k % 2 == 0 else 50
        b.append(f'<path d="M{X(k)},{80-h/2} L{X(k)+4},{80} L{X(k)},{80+h/2} L{X(k)+30},80 Z" class="fa"/>')
    # press point and snap
    px = X(2) + 28
    b.append(C(px, 38, 7, "fbadf")); b.append(T(px, 22, "you press here", "tm", size=11))
    b.append(L(px - 8, 38, X(2) + 8, 38, "sb", True)); b.append(T(X(2) - 4, 22, "snaps to beat", "tx", "end", 11, 600))
    b.append(T(X(6), 22, "spikes = transients (drum hits)", "tm", size=11))
    return svg(720, 156, "".join(b), "Quantise snaps a late button press back onto the nearest beat line")

def beatgrid():
    b = []
    for row, off in enumerate([14, 0]):
        y = 30 + row * 90
        b.append(T(20, y - 8, "Grid drifting off the kicks" if off else "Grid on the kicks", "tx", "start", 12, 600))
        for k in range(10):
            x = 40 + k * 68
            b.append(f'<path d="M{x},{y+10} L{x+3},{y+35} L{x},{y+60} L{x+24},{y+35} Z" class="fa"/>')
            gx = x + off + k * 1.5 if off else x
            b.append(L(gx, y + 4, gx, y + 66, "sbad" if off else "sb"))
    return svg(740, 200, "".join(b), "A beat grid misaligned with the drum hits compared with one sitting on them")

def hotcues():
    b = []
    import random
    random.seed(4)
    x0, x1 = 30, 720
    for i in range(0, 690, 4):
        f = i / 690
        e = 0.3 if f < .14 else (0.7 if f < .2 else (1 if f < .4 else (0.35 if f < .55 else (1 if f < .82 else 0.3))))
        h = (20 + random.random() * 30) * e + 4
        b.append(f'<rect x="{x0+i}" y="{80-h}" width="3" height="{2*h:.1f}" class="fb" opacity="0.8"/>')
    marks = [(0, "A", "first beat"), (.14, "B", "build"), (.2, "C", "drop"), (.4, "D", "breakdown"), (.82, "E", "outro")]
    for f, k, d in marks:
        x = x0 + f * 690
        b.append(L(x, 20, x, 140, "st"))
        b.append(R(x - 10, 6, 20, 18, "fa st", 4)); b.append(T(x, 19, k, "tx", size=11, weight=700))
        b.append(T(x + 4, 156, d, "tm", "start", 11))
    return svg(750, 166, "".join(b), "A track overview with hot cues A to E marking its sections")

def acapella():
    b = []
    X = lambda beat: 60 + beat * 40
    b.append(T(14, 46, "Vocal", "tx", "start", 12, 600)); b.append(T(14, 106, "Beat", "tx", "start", 12, 600))
    for bar in range(4):
        b.append(R(X(bar * 4) + 1, 84, 158, 34, "fs st", 5)); b.append(T(X(bar * 4) + 80, 106, f"bar {bar+1}", "tm", size=11))
    b.append(R(X(-1.5), 30, X(10) - X(-1.5), 26, "fa st", 5)); b.append(T(X(4), 48, "“Hey...  la la la la...”", "tx", size=11))
    b.append(L(X(0), 20, X(0), 126, "sb", dash=True)); b.append(T(X(0) + 4, 140, "bar 1, beat 1", "tm", "start", 11))
    b.append(T(X(-1.5), 22, "pickup", "tm", "start", 11))
    return svg(740, 150, "".join(b), "An acapella whose pickup starts just before beat one of the instrumental")

def stems():
    b = []
    lanes = [("Vocals", "fa", True), ("Melody", "fb", False), ("Bass", "fs", True), ("Drums", "fa", True)]
    import random
    random.seed(9)
    for i, (n, c, on) in enumerate(lanes):
        y = 14 + i * 40
        b.append(T(16, y + 22, n, "tx", "start", 12, 600))
        b.append(R(90, y + 6, 30, 22, "fa st" if on else "fs st", 5)); b.append(T(105, y + 21, "on" if on else "off", "tx" if on else "tm", size=10))
        for k in range(0, 560, 6):
            h = 4 + random.random() * 12
            b.append(f'<rect x="{140+k}" y="{y+17-h/2:.1f}" width="4" height="{h:.1f}" rx="1" class="{c if on else "fs"}"/>')
    return svg(720, 180, "".join(b), "A track split into four stems that can be switched on and off")

def folders():
    b = []
    items = [(0, "My Library"), (1, "Warm-Up sets"), (2, "House 122-126"), (2, "Hip hop 90s"), (1, "Main Room sets"), (2, "Peak time (energy 4-5)"),
             (2, "Warm up (energy 1-2)"), (1, "Showcase 2026"), (2, "Set order")]
    for i, (lvl, n) in enumerate(items):
        x = 24 + lvl * 34; y = 24 + i * 26
        if lvl:
            b.append(P([(x - 20, y - 18), (x - 20, y - 4), (x - 6, y - 4)], "sm fn"))
        b.append(R(x, y - 13, 18, 14, "fa" if lvl < 2 else "fb", 3))
        b.append(T(x + 26, y - 1, n, "tx" if lvl < 2 else "tm", "start", 12, 600 if lvl < 2 else None))
    return svg(360, 254, "".join(b), "A tidy rekordbox library: folders by purpose, playlists inside")

def drums(genre):
    P_ = {
        "house": {"Kick": "x---x---x---x---", "Clap": "----x-------x---", "Hat": "--x---x---x---x-"},
        "hiphop": {"Kick": "x-----x-x-------", "Snare": "----x-------x---", "Hat": "x-x-x-x-x-x-x-x-"},
        "grime": {"Kick": "x------x--x-----", "Snare": "--------x-------", "Hat": "x-x-x-x-x-x-x-x-"},
        "techno": {"Kick": "x---x---x---x---", "Hat": "--x---x---x---x-", "Clap": "------------x---"},
        "disco": {"Kick": "x---x---x---x---", "Snare": "----x-------x---", "Hat": "xxxxxxxxxxxxxxxx"},
        "techhouse": {"Kick": "x---x---x---x---", "Clap": "----x-------x---", "Perc": "-x-x--x--x-x--x-"},
        "rnb": {"Kick": "x-------x-x-----", "Snare": "----x-------x---", "Hat": "x-x-x-x-x-x-x-x-"},
        "trance": {"Kick": "x---x---x---x---", "Bass": "--x---x---x---x-", "Hat": "--x---x---x---x-"},
        "dnb": {"Kick": "x---------x-----", "Snare": "----x-------x---", "Hat": "x-x-x-x-x-x-x-x-"},
        "dubstep": {"Kick": "x---------------", "Snare": "--------x-------", "Hat": "x-x-x-x-x-x-x-x-"},
        "breaks": {"Kick": "x-----x---x-----", "Snare": "----x-------x---", "Hat": "x-xxx-x-x-xxx-x-"},
        "garage": {"Kick": "x---------x-----", "Snare": "----x-------x---", "Hat": "--x-x-x--x-x-x-x"},
        "afrobeats": {"Kick": "x--x--x-x--x--x-", "Snare": "----x-------x---", "Shaker": "xxxxxxxxxxxxxxxx"},
        "amapiano": {"Kick": "x---x---x---x---", "Log drum": "x--x---x--x-x---", "Shaker": "x-xxx-xxx-xxx-xx"},
        "drill": {"Kick": "x-----x---x-----", "Snare": "--------x-------", "Hat": "x--x-x--x-x--x-x"},
    }[genre]
    b = []
    for r, (lane, pat) in enumerate(P_.items()):
        y = 10 + r * 30
        b.append(T(76, y + 18, lane, "tx", "end", 11, 600))
        for s, ch in enumerate(pat):
            x = 84 + s * 22 + (s // 4) * 6
            b.append(R(x, y + 2, 18, 22, ("fa" if ch == "x" else "fs") + (" sm" if s % 4 == 0 else ""), 3))
    for beat in range(4):
        b.append(T(84 + beat * 94 + 40, 10 + len(P_) * 30 + 14, str(beat + 1), "tm", size=11))
    return svg(470, 10 + len(P_) * 30 + 22, "".join(b), f"Typical one-bar drum pattern for {genre}")

def timeline(items):
    n = len(items)
    W = 760
    b = [L(30, 60, W - 30, 60, "sm")]
    for i, (yr, txt) in enumerate(items):
        x = 92 + i * (W - 184) / max(1, n - 1)
        b.append(C(x, 60, 7, "fa st"))
        b.append(T(x, 40, yr, "tx", size=13, weight=700))
        words = txt.split()
        line, lines = "", []
        for w_ in words:
            if len(line) + len(w_) > 18: lines.append(line); line = w_
            else: line = (line + " " + w_).strip()
        lines.append(line)
        for j, ln in enumerate(lines[:3]):
            b.append(T(x, 86 + j * 15, ln, "tm", size=11))
    return svg(W, 136, "".join(b), "Timeline of key moments")

def setshape_genre():
    b = []
    blocks = [("Hip hop", "90 BPM", 0, 1), ("Afrobeats", "105", 1, 2), ("House", "124", 2, 3), ("UK garage", "132", 3, 4), ("Drum & bass", "174", 4, 5)]
    for i, (g, bpm, a, z) in enumerate(blocks):
        x = 20 + a * 140
        y = 150 - (i + 1) * 24
        b.append(R(x, y, 132, 150 - y, "fa st" if i == 4 else "fs st", 8))
        b.append(T(x + 66, y + 22, g, "tx", size=12, weight=600)); b.append(T(x + 66, y + 40, bpm, "tm", size=11))
    b.append(T(20, 172, "60-minute set: about 12 minutes per block, tempo climbing as the night builds", "tm", "start", 11))
    return svg(720, 182, "".join(b), "A set grouped into genre blocks that climb in tempo")

REG = {
    "pulse": pulse, "phrase": phrase, "sections": sections, "introtypes": intro_types, "beatalign": beatalign,
    "tempomiddle": tempo_middle, "transitiontrack": transition_track, "eq": eqspectrum, "bassswap": bassswap,
    "meter": meter, "filters": filtercurves, "xfcurve": xfcurve, "signal1": signal1, "signal2": signal2,
    "signal3": signal3, "headphones": headphones, "controller": controller, "camelot": camelot,
    "loop": loopdiag, "slip": slip, "quantise": quantise, "beatgrid": beatgrid, "hotcues": hotcues,
    "acapella": acapella, "stems": stems, "folders": folders, "setgenre": setshape_genre,
}

def render(spec):
    """spec like 'blend 1 0 0' or 'scratch baby' or 'energy coaster'"""
    parts = spec.split()
    k, args = parts[0], parts[1:]
    if k == "blend": return blend(*[int(a) for a in args])
    if k == "cut": return cutdiag(args[0] if args else "straight")
    if k == "scratch": return scratch(args[0])
    if k == "energy": return energy(args[0] if args else "build")
    if k == "drums": return drums(args[0])
    if k == "tap": return tappause("tap")
    if k == "doubling": return tappause("double")
    if k == "camelot": return camelot(int(args[0]) if args else 8)
    return REG[k]()
