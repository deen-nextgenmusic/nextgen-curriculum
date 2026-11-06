#!/usr/bin/env python3
"""Builds the NextGen DJ Curriculum handbook into one self-contained HTML page."""
import base64, html, re, sys, pathlib
import dg, illus

ROOT = pathlib.Path(__file__).parent
IMG = ROOT / "img"

def b64(name, mime):
    return f"data:{mime};base64," + base64.b64encode((IMG / name).read_bytes()).decode()

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"\b((?:WU|MR|HL)-[KSRG]\d\d)\b", lambda m: f'<a class="xref" href="#{m.group(1).lower()}">{m.group(1)}</a>', s)
    return s

# ------------------------------------------------------------------ parser
def parse(path):
    lines = path.read_text().splitlines()
    doc = {"meta": {}, "groups": []}
    group = None; topic = None
    i = 0
    def new_block(kind, **kw):
        d = {"k": kind}; d.update(kw); topic["blocks"].append(d); return d
    while i < len(lines):
        ln = lines[i].rstrip()
        if ln.startswith("@"):
            k, v = ln[1:].split(":", 1); doc["meta"][k.strip()] = v.strip(); i += 1; continue
        if ln.startswith("== "):
            group = {"name": ln[3:].strip(), "topics": []}; doc["groups"].append(group); i += 1; continue
        if ln.startswith("## "):
            parts = [p.strip() for p in ln[3:].split("|")]
            topic = {"code": parts[0], "title": parts[1], "flag": parts[2] if len(parts) > 2 else "", "blocks": []}
            group["topics"].append(topic); i += 1; continue
        if topic is None or not ln.strip():
            i += 1; continue
        if ln.startswith("> "):
            new_block("lead", t=ln[2:]); i += 1; continue
        m = re.match(r"^(dg|drums|pic|tip|game|warn|h|tutor|roots):\s*(.*)$", ln)
        if m:
            key, val = m.groups()
            new_block(key, t=val); i += 1; continue
        m = re.match(r"^(teach|check|listen|facts|timeline|table|steps|cards|people):\s*$", ln)
        if m:
            key = m.group(1); items = []; i += 1
            while i < len(lines) and lines[i].strip() and (lines[i].lstrip().startswith(("- ", "|"))):
                items.append(lines[i].strip()); i += 1
            new_block(key, items=items); continue
        if ln.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:]); i += 1
            new_block("ul", items=items); continue
        if re.match(r"^\d+\. ", ln):
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\. ", "", lines[i])); i += 1
            new_block("ol", items=items); continue
        new_block("p", t=ln.strip()); i += 1
    return doc

# ------------------------------------------------------------------ renderers
ICON_CHECK = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3 3 7-7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
PICS = {}

def fig(svgstr, cap, cls="dg"):
    c = f"<figcaption>{inline(cap)}</figcaption>" if cap else ""
    return f'<figure class="{cls}"><div class="dgscroll">{svgstr}</div>{c}</figure>'

def render_block(b):
    k = b["k"]
    if k == "lead": return f'<p class="lead">{inline(b["t"])}</p>'
    if k == "p": return f"<p>{inline(b['t'])}</p>"
    if k == "h": return f"<h4>{inline(b['t'])}</h4>"
    if k == "ul": return "<ul>" + "".join(f"<li>{inline(x)}</li>" for x in b["items"]) + "</ul>"
    if k == "ol": return '<ol class="num">' + "".join(f"<li>{inline(x)}</li>" for x in b["items"]) + "</ol>"
    if k == "dg":
        spec, _, cap = b["t"].partition("|")
        return fig(dg.render(spec.strip()), cap.strip())
    if k == "drums":
        g, _, cap = b["t"].partition("|")
        return fig(dg.drums(g.strip()), cap.strip() or "A typical one-bar pattern. Real tracks vary.", "dg drums")
    if k == "pic":
        name, _, cap = b["t"].partition("|")
        return f'<figure class="photo"><img src="{PICS[name.strip()]}" alt="{html.escape(cap.strip())}" loading="lazy"><figcaption>{inline(cap.strip())}</figcaption></figure>'
    if k == "tip":
        return f'<aside class="note tip"><span class="nlab">Tutor tip</span><p>{inline(b["t"])}</p></aside>'
    if k == "warn":
        return f'<aside class="note warn"><span class="nlab">Watch out</span><p>{inline(b["t"])}</p></aside>'
    if k == "tutor":
        return f'<aside class="note tip"><span class="nlab">In the lesson</span><p>{inline(b["t"])}</p></aside>'
    if k == "game":
        name, _, txt = b["t"].partition("|")
        return f'<aside class="note game"><span class="nlab">Game</span><p><strong>{inline(name.strip())}.</strong> {inline(txt.strip())}</p></aside>'
    if k == "teach":
        return '<div class="box teach"><h5>Teach it</h5><ol>' + "".join(f"<li>{inline(x[2:])}</li>" for x in b["items"]) + "</ol></div>"
    if k == "check":
        return '<div class="box check"><h5>Students can</h5><ul>' + "".join(f"<li>{ICON_CHECK}<span>{inline(x[2:])}</span></li>" for x in b["items"]) + "</ul></div>"
    if k == "steps":
        return '<ol class="steps">' + "".join(f"<li><span>{inline(x[2:])}</span></li>" for x in b["items"]) + "</ol>"
    if k == "roots":
        parts = [p.strip() for p in b["t"].split(">")]
        before = [x.strip() for x in parts[0].split(",")]
        mid = parts[1:-1]
        after = [x.strip() for x in parts[-1].split(",")]
        chips = lambda xs: "".join(f'<span class="rc">{inline(x)}</span>' for x in xs)
        midh = '<span class="rarr" aria-hidden="true"></span>'.join(f'<span class="rg">{inline(x)}</span>' for x in mid)
        return ('<div class="roots" role="group" aria-label="Where the genre came from and what it led to">'
                f'<div class="rcol"><span class="rl">Grew out of</span><div class="rchips">{chips(before)}</div></div>'
                '<span class="rarr" aria-hidden="true"></span>'
                f'<div class="rmid">{midh}</div>'
                '<span class="rarr" aria-hidden="true"></span>'
                f'<div class="rcol"><span class="rl">Led to</span><div class="rchips">{chips(after)}</div></div></div>')
    if k == "people":
        out = []
        for x in b["items"]:
            n, _, r = x[2:].partition("=")
            n, r = n.strip(), r.strip()
            words = [w for w in re.sub(r"[^A-Za-z0-9 &]", "", n).split() if w not in ("and", "&", "The", "DJ", "MC")]
            ini = "".join(w[0] for w in words[:2]).upper() or n[:2].upper()
            out.append(f'<div class="person"><span class="pi" aria-hidden="true">{html.escape(ini)}</span><span class="pt"><strong>{inline(n)}</strong><span>{inline(r)}</span></span></div>')
        return '<div class="people">' + "".join(out) + "</div>"
    if k == "cards":
        out = []
        for x in b["items"]:
            ic, name, txt = [s.strip() for s in x[2:].split("|", 2)]
            out.append(f'<div class="icard"><div class="ill">{illus.icon(ic)}</div><div class="ic-t"><strong>{inline(name)}</strong><span>{inline(txt)}</span></div></div>')
        cols = 4 if len(out) in (4, 7, 8) else 3
        return f'<div class="icards" style="--cols:{cols}">' + "".join(out) + "</div>"
    if k == "facts":
        cells = []
        for x in b["items"]:
            kk, _, vv = x[2:].partition("=")
            cells.append(f'<div><dt>{inline(kk.strip())}</dt><dd>{inline(vv.strip())}</dd></div>')
        return '<dl class="facts">' + "".join(cells) + "</dl>"
    if k == "listen":
        out = []
        for x in b["items"]:
            a, _, t = x[2:].partition(" - ")
            out.append(f'<li><span class="la">{inline(a)}</span><span class="lt">{inline(t)}</span></li>')
        return '<div class="listen"><h5>Tunes that shaped it</h5><ul>' + "".join(out) + "</ul></div>"
    if k == "timeline":
        items = []
        for x in b["items"]:
            y, _, t = x[2:].partition("=")
            items.append((y.strip(), t.strip()))
        return fig(dg.timeline(items), "")
    if k == "table":
        rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in b["items"]]
        head = "".join(f"<th>{inline(c)}</th>" for c in rows[0])
        body = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
        return f'<div class="tablewrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'
    raise ValueError(k)

def render_topic(t, stage_key):
    tid = t["code"].lower()
    flag = ""
    if t["flag"] == "new": flag = '<span class="flag">New</span>'
    blocks = t["blocks"]
    main = []
    for b in blocks:
        if b["k"] in ("teach", "check"): continue
        if b["k"] == "facts" and tid in DISC:
            tempo = next((x[2:].split("=",1)[1].strip() for x in b["items"] if x[2:].startswith("Tempo")), "")
            tempo = tempo.split(",")[0].replace(" BPM", "").replace("Around ", "") + " BPM"
            main.append(f'<div class="genrehead"><div class="disc">{illus.disc(DISC[tid], tempo, "")}</div>{render_block(b)}</div>')
        else:
            main.append(render_block(b))
    side = [render_block(b) for b in blocks if b["k"] in ("teach", "check")]
    code = f'<span class="code">{t["code"]}</span>' if not t["code"].startswith("x-") else ""
    ticon = f'<span class="ticon">{illus.icon(ICONS[tid])}</span>' if tid in ICONS else ""
    return (f'<article class="topic" id="{tid}" data-title="{html.escape(t["title"].lower())}">'
            f'<header class="th">{ticon}{code}<h3>{inline(t["title"])}</h3>{flag}</header>'
            f'<div class="tb">{"".join(main)}</div>'
            + (f'<div class="boxes">{"".join(side)}</div>' if side else "") + "</article>")

DISC = {"wu-k12":"House","wu-k13":"Hip hop","wu-k14":"Grime","wu-k15":"Afrobeats","mr-k08":"Disco","mr-k09":"Techno","mr-k10":"Tech house","mr-k11":"R&B","mr-k12":"Amapiano","mr-k13":"Trap & drill","hl-k07":"Trance","hl-k08":"Drum & bass","hl-k09":"Dubstep","hl-k10":"Breakbeat","hl-k11":"UK garage","hl-k12":"Afro house","hl-k13":"Jersey club"}
_I = """x-safety ear,x-kit controller,x-games crowd,x-shape metronome,x-levelup vinyl,
wu-k01 clap,wu-k02 metronome,wu-k03 headphones,wu-k04 key,wu-k05 cdj,wu-k06 vinyl,wu-k07 kick,wu-k08 usb,wu-k09 controller,wu-k10 mixer,wu-k11 vinyl,
wu-k16 cdj,wu-k17 crowd,wu-k18 laptop,wu-k19 headphones,wu-k20 laptop,wu-s01 cdj,wu-s02 metronome,wu-s03 cdj,wu-s04 mixer,wu-s05 turntable,wu-s06 turntable,
wu-s07 turntable,wu-s08 turntable,wu-s09 turntable,wu-s10 turntable,wu-r01 laptop,wu-r02 laptop,wu-g01 mic,wu-g02 mic,
mr-k01 clap,mr-k02 crash,mr-k03 drummachine,mr-k04 mixer,mr-k05 controller,mr-k06 speaker,mr-k07 vinyl,mr-k14 kick,mr-k15 key,mr-k16 crowd,mr-k17 laptop,
mr-s01 fx,mr-s02 loop,mr-s03 turntable,mr-s04 turntable,mr-s05 loop,mr-s06 metronome,mr-s07 mixer,mr-s08 turntable,mr-s09 turntable,mr-s10 turntable,mr-s11 turntable,
mr-s12 sampler,mr-s13 turntable,mr-s14 cdj,mr-r01 laptop,mr-r02 laptop,mr-r03 laptop,mr-r04 sampler,mr-r05 laptop,mr-r06 key,
hl-k01 synth,hl-k02 clap,hl-k03 fx,hl-k04 mixer,hl-k05 speaker,hl-k06 vinyl,hl-k14 metronome,hl-k15 mic,hl-k16 crowd,hl-k17 vinyl,
hl-s01 fx,hl-s02 loop,hl-s03 mic,hl-s04 metronome,hl-s05 turntable,hl-s06 turntable,hl-s07 sampler,hl-r01 laptop,hl-r02 mixer,hl-r03 headphones"""
ICONS = dict(x.strip().split() for x in _I.replace("\n", "").split(",") if x.strip())

STAGE_N = {"warmup": 1, "mainroom": 2, "headliner": 3}

def meter(n):
    return '<span class="meter" aria-hidden="true">' + "".join(f'<i class="{"on" if i < n else ""}"></i>' for i in range(3)) + "</span>"

def render_stage(doc, key):
    m = doc["meta"]
    n = STAGE_N.get(key)
    count = sum(len(g["topics"]) for g in doc["groups"])
    if n:
        opener = (f'<header class="opener" id="{key}">'
                  f'<div class="op-img" style="background-image:url({PICS[m["pic"]]})"></div>'
                  f'<div class="op-in"><div class="op-top">{meter(n)}<span class="eyebrow">Stage {n} of 3 · {count} topics</span></div>'
                  f'<h2>{m["title_html"]}</h2><p class="op-lead">{inline(m["lead"])}</p>'
                  f'<div class="op-check"><span class="eyebrow">Level-up check</span><p>{inline(m["check"])}</p></div></div></header>')
    else:
        opener = f'<header class="chap" id="{key}"><span class="eyebrow">{inline(m.get("eyebrow",""))}</span><h2>{inline(m["title"])}</h2>' + (f'<p class="op-lead">{inline(m["lead"])}</p>' if m.get("lead") else "") + "</header>"
    body = []
    for g in doc["groups"]:
        gid = f'{key}-{re.sub(r"[^a-z0-9]+", "-", g["name"].lower()).strip("-")}'
        if g["name"] != "-":
            body.append(f'<div class="group" id="{gid}"><span class="eyebrow">{inline(m.get("short", ""))}</span><h3 class="gh">{inline(g["name"])}</h3></div>')
        body.extend(render_topic(t, key) for t in g["topics"])
    return f'<section class="stage s-{key}">{opener}<div class="stage-body">{"".join(body)}</div></section>'

def nav_for(doc, key):
    m = doc["meta"]
    n = STAGE_N.get(key)
    head = (meter(n) if n else "") + f'<span>{inline(m.get("navtitle", m["title"]))}</span>'
    items = []
    for g in doc["groups"]:
        if g["name"] != "-":
            items.append(f'<li class="ng">{inline(g["name"])}</li>')
        for t in g["topics"]:
            code = "" if t["code"].startswith("x-") else f'<span class="nc">{t["code"]}</span>'
            items.append(f'<li class="nt" data-q="{html.escape((t["code"]+" "+t["title"]).lower())}"><a href="#{t["code"].lower()}">{code}{inline(t["title"])}</a></li>')
    first = f'<li class="nt"><a href="#{key}"><span class="nc"></span>Go to {inline(m.get("navtitle", m["title"]))}</a></li>'
    opened = " open" if key == "start" else ""
    return f'<details class="nsec"{opened}><summary>{head}<span class="chev" aria-hidden="true"></span></summary><ul>{first}{"".join(items)}</ul></details>'

def index_table(docs):
    rows = []
    for key, d in docs:
        if key not in STAGE_N: continue
        for g in d["groups"]:
            for t in g["topics"]:
                rows.append(f'<tr><td class="mono"><a href="#{t["code"].lower()}">{t["code"]}</a></td><td>{inline(t["title"])}</td><td>{inline(g["name"])}</td><td>{inline(d["meta"]["navtitle"])}</td></tr>')
    return ('<section class="stage s-index"><header class="chap" id="topic-index"><span class="eyebrow">Reference</span><h2>Topic index</h2>'
            f'<p class="op-lead">Every topic in the curriculum, with its code. Use the code in lesson notes so any tutor can pick up where you left off.</p></header>'
            '<div class="stage-body"><div class="tablewrap"><table class="idx"><thead><tr><th>Code</th><th>Topic</th><th>Area</th><th>Stage</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div></div></section>")

def main(files, out):
    for n, f in [("hero", "hero.jpg"), ("hands", "hands.jpg"), ("jog", "jog.jpg"), ("lesson", "lesson.jpg"), ("crowd", "crowd.jpg"), ("stall", "stall.jpg"), ("team", "team.jpg")]:
        PICS[n] = b64(f, "image/jpeg")
    PICS["logo"] = b64("logo.png", "image/png")
    docs = [(pathlib.Path(f).stem.split("_", 1)[1], parse(ROOT / "content" / f)) for f in files]
    for key, d in docs:
        if "title_html" in d["meta"]:
            d["meta"]["title_html"] = d["meta"]["title_html"]
    stages_html = "".join(render_stage(d, k) for k, d in docs)
    nav_html = "".join(nav_for(d, k) for k, d in docs)
    stage_meta = {k: d["meta"] for k, d in docs}
    total = sum(sum(len(g["topics"]) for g in d["groups"]) for k, d in docs if k in STAGE_N)
    tpl = (ROOT / "template.html").read_text()
    page = (tpl.replace("{{NAV}}", nav_html)
               .replace("{{STAGES}}", stages_html + index_table(docs))
               .replace("{{LOGO}}", PICS["logo"]).replace("{{HERO}}", PICS["hero"])
               .replace("{{TOTAL}}", str(total)))
    (ROOT / out).write_text(page)
    print("wrote", out, len(page) // 1024, "KB,", total, "stage topics")

if __name__ == "__main__":
    main(sys.argv[1:-1], sys.argv[-1])
