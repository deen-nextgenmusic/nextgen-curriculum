"""On-brand line illustrations (white and mint on navy) for NextGen DJ Curriculum.
All drawings are generic, original artwork on a 120x120 grid."""

W = 'class="iw"'      # white line
A = 'class="ia"'      # mint line
FM = 'class="fm"'     # mint fill
FW = 'class="fw"'     # white fill
FN = 'class="fn2"'    # navy fill

def wrap(body, label):
    return f'<svg viewBox="0 0 120 120" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'

D = {}

D["kick"] = ('<circle cx="60" cy="58" r="40" class="iw"/><circle cx="60" cy="58" r="30" class="ia"/>'
             '<circle cx="60" cy="58" r="9" class="fm"/>'
             + "".join(f'<line x1="{60+40*__import__("math").cos(a*0.785):.1f}" y1="{58+40*__import__("math").sin(a*0.785):.1f}" x2="{60+45*__import__("math").cos(a*0.785):.1f}" y2="{58+45*__import__("math").sin(a*0.785):.1f}" class="iw"/>' for a in range(8))
             + '<line x1="30" y1="96" x2="22" y2="110" class="iw"/><line x1="90" y1="96" x2="98" y2="110" class="iw"/>', "Kick drum")
D["snare"] = ('<ellipse cx="60" cy="48" rx="40" ry="12" class="iw"/><path d="M20 48v26c0 7 18 12 40 12s40-5 40-12V48" class="iw"/>'
              '<path d="M28 58v20M44 61v22M60 62v24M76 61v22M92 58v20" class="ia"/>'
              '<line x1="34" y1="14" x2="66" y2="44" class="iw"/><line x1="88" y1="12" x2="58" y2="42" class="iw"/>'
              '<circle cx="66" cy="44" r="3" class="fm"/><circle cx="58" cy="42" r="3" class="fm"/>', "Snare drum")
D["hihat"] = ('<ellipse cx="60" cy="34" rx="40" ry="6" class="ia"/><ellipse cx="60" cy="42" rx="40" ry="6" class="iw"/>'
              '<line x1="60" y1="20" x2="60" y2="100" class="iw"/><path d="M60 100l-24 12M60 100l24 12M60 100v12" class="iw"/>'
              '<rect x="50" y="104" width="20" height="6" rx="2" class="fm"/>'
              '<path d="M18 22c4-4 8-4 12 0M90 22c4-4 8-4 12 0" class="ia"/>', "Hi-hat")
D["toms"] = ('<ellipse cx="40" cy="46" rx="24" ry="8" class="iw"/><path d="M16 46v24c0 5 11 8 24 8s24-3 24-8V46" class="iw"/>'
             '<ellipse cx="82" cy="54" rx="22" ry="7" class="ia"/><path d="M60 54v24c0 4 10 7 22 7s22-3 22-7V54" class="ia"/>'
             '<path d="M40 78v24M82 85v20" class="iw"/>', "Tom drums")
D["crash"] = ('<path d="M14 54c20-16 72-16 92 0c-20 8-72 8-92 0z" class="iw"/><circle cx="60" cy="48" r="5" class="fm"/>'
              '<line x1="60" y1="50" x2="60" y2="104" class="iw"/><path d="M60 104l-20 10M60 104l20 10" class="iw"/>'
              '<path d="M22 34c6-8 14-12 22-12M98 34c-6-8-14-12-22-12" class="ia"/><path d="M30 24c4-6 10-9 16-9M90 24c-4-6-10-9-16-9" class="ia"/>', "Crash cymbal")
D["ride"] = ('<path d="M8 58c24-20 80-20 104 0c-24 9-80 9-104 0z" class="iw"/><path d="M50 46c0-8 20-8 20 0" class="ia"/>'
             '<line x1="60" y1="56" x2="60" y2="106" class="iw"/><path d="M60 106l-20 8M60 106l20 8" class="iw"/>'
             '<line x1="86" y1="18" x2="66" y2="42" class="iw"/><circle cx="66" cy="42" r="3" class="fm"/>', "Ride cymbal")
D["shaker"] = ('<rect x="38" y="30" width="44" height="64" rx="22" class="iw" transform="rotate(-20 60 62)"/>'
               '<g transform="rotate(-20 60 62)"><circle cx="54" cy="52" r="3" class="fm"/><circle cx="66" cy="60" r="3" class="fm"/><circle cx="56" cy="70" r="3" class="fm"/><circle cx="66" cy="78" r="3" class="fm"/></g>'
               '<path d="M18 40c-4 8-4 16 0 24M26 46c-2 5-2 10 0 14M102 60c4 8 4 16 0 24M94 66c2 5 2 10 0 14" class="ia"/>', "Shaker")
D["cowbell"] = ('<path d="M44 30h32l12 60H32z" class="iw"/><rect x="52" y="20" width="16" height="10" rx="2" class="iw"/>'
                '<path d="M40 74h40" class="ia"/><line x1="98" y1="22" x2="72" y2="58" class="iw"/><circle cx="72" cy="58" r="4" class="fm"/>', "Cowbell")
D["bass"] = ('<rect x="24" y="16" width="72" height="92" rx="10" class="iw"/><circle cx="60" cy="72" r="24" class="iw"/><circle cx="60" cy="72" r="10" class="fm"/>'
             '<circle cx="60" cy="34" r="8" class="ia"/><path d="M6 72c4-10 8-10 12 0s8 10 12 0M90 72c4-10 8-10 12 0s8 10 12 0" class="ia"/>', "Bass speaker")
D["keys"] = ('<rect x="10" y="38" width="100" height="50" rx="6" class="iw"/>'
             + "".join(f'<line x1="{10+i*12.5:.1f}" y1="38" x2="{10+i*12.5:.1f}" y2="88" class="iw"/>' for i in range(1, 8))
             + "".join(f'<rect x="{18+i*12.5:.1f}" y="38" width="8" height="28" rx="1" class="fw"/>' for i in (0, 1, 3, 4, 5))
             + '<path d="M30 22l8-8 8 8M52 16v14M72 18c6 0 10 4 10 8" class="ia"/>', "Keyboard")
D["mic"] = ('<rect x="44" y="12" width="32" height="50" rx="16" class="iw"/><path d="M48 26h24M48 36h24M48 46h24" class="ia"/>'
            '<path d="M34 50c0 16 12 26 26 26s26-10 26-26" class="iw"/><line x1="60" y1="76" x2="60" y2="100" class="iw"/><line x1="42" y1="102" x2="78" y2="102" class="iw"/>', "Microphone")
D["headphones"] = ('<path d="M22 70V58a38 38 0 0 1 76 0v12" class="iw"/><rect x="14" y="64" width="20" height="36" rx="8" class="fm"/>'
                   '<rect x="86" y="64" width="20" height="36" rx="8" class="fm"/><path d="M28 64v36M92 64v36" class="iw"/>', "Headphones")
D["turntable"] = ('<rect x="8" y="22" width="104" height="80" rx="8" class="iw"/><circle cx="50" cy="62" r="32" class="iw"/><circle cx="50" cy="62" r="12" class="fm"/>'
                  '<circle cx="50" cy="62" r="22" class="ia"/><path d="M98 32v40l-22 14" class="iw"/><circle cx="98" cy="32" r="5" class="fw"/>'
                  '<rect x="92" y="84" width="12" height="10" rx="2" class="ia"/>', "Turntable")
D["vinyl"] = ('<circle cx="60" cy="60" r="48" class="iw"/><circle cx="60" cy="60" r="40" class="ia"/><circle cx="60" cy="60" r="32" class="iw"/>'
              '<circle cx="60" cy="60" r="16" class="fm"/><circle cx="60" cy="60" r="3" class="fn2"/>', "Vinyl record")
D["controller"] = ('<rect x="6" y="28" width="108" height="64" rx="8" class="iw"/><circle cx="30" cy="58" r="16" class="iw"/><circle cx="90" cy="58" r="16" class="iw"/>'
                   '<circle cx="30" cy="58" r="5" class="fm"/><circle cx="90" cy="58" r="5" class="fm"/><path d="M54 40v24M66 40v24" class="iw"/>'
                   '<rect x="50" y="48" width="8" height="5" class="fm"/><rect x="62" y="44" width="8" height="5" class="fm"/><path d="M50 80h20" class="ia"/>', "DJ controller")
D["speaker"] = ('<rect x="28" y="8" width="64" height="104" rx="8" class="iw"/><circle cx="60" cy="76" r="22" class="iw"/><circle cx="60" cy="76" r="8" class="fm"/>'
                '<circle cx="60" cy="32" r="10" class="ia"/>', "Speaker")
D["usb"] = ('<rect x="42" y="38" width="36" height="64" rx="6" class="iw"/><rect x="48" y="18" width="24" height="20" rx="2" class="iw"/>'
            '<rect x="53" y="24" width="5" height="5" class="fm"/><rect x="62" y="24" width="5" height="5" class="fm"/><path d="M52 70h16" class="ia"/>', "USB stick")
D["laptop"] = ('<rect x="22" y="26" width="76" height="50" rx="4" class="iw"/><path d="M10 86h100l-6 10H16z" class="iw"/>'
               '<path d="M30 60l8-14 8 20 8-24 8 18 8-8 8 8 8-4" class="ia"/>', "Laptop")
D["drummachine"] = ('<rect x="6" y="30" width="108" height="62" rx="6" class="iw"/><rect x="14" y="38" width="28" height="14" rx="2" class="ia"/>'
                    + "".join(f'<circle cx="{54+i*14}" cy="45" r="5" class="iw"/>' for i in range(4))
                    + "".join(f'<rect x="{12+i*12.5:.1f}" y="70" width="8" height="12" rx="2" class="{"fm" if i % 4 == 0 else "fw"}"/>' for i in range(8)), "Drum machine")
D["synth"] = ('<rect x="6" y="20" width="108" height="34" rx="6" class="iw"/>'
              + "".join(f'<circle cx="{20+i*16}" cy="37" r="6" class="{"ia" if i % 2 else "iw"}"/>' for i in range(6))
              + '<rect x="6" y="58" width="108" height="40" rx="4" class="iw"/>'
              + "".join(f'<line x1="{6+i*13.5:.1f}" y1="58" x2="{6+i*13.5:.1f}" y2="98" class="iw"/>' for i in range(1, 8))
              + "".join(f'<rect x="{14+i*13.5:.1f}" y="58" width="8" height="22" class="fw"/>' for i in (0, 1, 3, 4, 5)), "Synthesiser")
D["sampler"] = ('<rect x="14" y="10" width="92" height="100" rx="8" class="iw"/><rect x="24" y="20" width="72" height="18" rx="2" class="ia"/>'
                + "".join(f'<rect x="{26+(i%4)*18}" y="{46+(i//4)*15}" width="14" height="11" rx="2" class="{"fm" if i in (0, 5, 10, 15, 6) else "fw"}"/>' for i in range(16)), "Sampler pads")
D["mixer"] = ('<rect x="20" y="10" width="80" height="100" rx="8" class="iw"/>'
              + "".join(f'<circle cx="{38+c*22}" cy="{24+r*14}" r="5" class="{"ia" if r == 0 else "iw"}"/>' for c in range(3) for r in range(3))
              + "".join(f'<line x1="{38+c*22}" y1="70" x2="{38+c*22}" y2="96" class="iw"/><rect x="{32+c*22}" y="{76+c*5}" width="12" height="6" rx="1" class="fm"/>' for c in range(3)), "Mixer")
D["crowd"] = ("".join(f'<circle cx="{14+i*23}" cy="{70-(i%2)*6}" r="9" class="iw"/><path d="M{2+i*23} {104}c0-14 6-22 12-22s12 8 12 22" class="iw"/>' for i in range(5))
              + '<path d="M20 52l-6-22M60 46l2-26M100 52l6-22" class="ia"/><circle cx="14" cy="28" r="3" class="fm"/><circle cx="62" cy="18" r="3" class="fm"/><circle cx="106" cy="28" r="3" class="fm"/>', "Crowd")
D["ear"] = ('<path d="M74 40c0-16-12-26-26-26S22 26 22 42c0 12 8 16 8 26s-4 14-4 22c0 10 8 16 16 16 10 0 14-8 14-16" class="iw"/>'
            '<path d="M44 44c0-6 4-10 9-10s9 4 9 10c0 6-6 8-6 14" class="iw"/><rect x="72" y="52" width="26" height="14" rx="7" class="fm"/>'
            '<path d="M100 34l10-6M100 84l10 6" class="ia"/>', "Ear with earplug")
D["metronome"] = ('<path d="M44 14h32l20 94H24z" class="iw"/><line x1="60" y1="96" x2="82" y2="34" class="ia"/><circle cx="76" cy="50" r="5" class="fm"/><path d="M34 84h52" class="iw"/>', "Metronome")
D["clap"] = ('<path d="M40 100c-10-10-14-24-14-40 0-6 6-6 8 0l4 12V28c0-6 8-6 8 0v30-36c0-6 8-6 8 0v36-30c0-6 8-6 8 0v40" class="iw"/>'
             '<path d="M84 34l10-10M90 48l14-4M80 22l2-14" class="ia"/>', "Clapping hand")
D["cdj"] = ('<rect x="14" y="8" width="92" height="104" rx="8" class="iw"/><rect x="26" y="16" width="68" height="20" rx="2" class="ia"/>'
            '<circle cx="60" cy="70" r="26" class="iw"/><circle cx="60" cy="70" r="8" class="fm"/><circle cx="24" cy="100" r="5" class="fm"/><circle cx="38" cy="100" r="5" class="iw"/>', "Media player")
D["fx"] = ('<circle cx="40" cy="56" r="20" class="iw"/><line x1="40" y1="56" x2="52" y2="42" class="ia"/><path d="M68 56c6-12 12-12 18 0s12 12 18 0" class="ia"/>'
           '<path d="M66 82c8-6 14-6 22 0s14 6 22 0" class="iw"/><rect x="24" y="86" width="32" height="12" rx="4" class="fm"/>', "Effects")
D["loop"] = ('<path d="M30 60a30 30 0 1 1 30 30" class="iw"/><path d="M60 90l-10-8M60 90l-8 10" class="iw"/><circle cx="60" cy="60" r="12" class="fm"/><path d="M60 22v8M98 60h-8" class="ia"/>', "Loop")
D["key"] = ('<circle cx="60" cy="60" r="44" class="iw"/>' + "".join(f'<circle cx="{60+34*__import__("math").cos(a*0.5236-1.5708):.1f}" cy="{60+34*__import__("math").sin(a*0.5236-1.5708):.1f}" r="5" class="{"fm" if a in (11, 0, 1) else "fw"}"/>' for a in range(12)) + '<circle cx="60" cy="60" r="16" class="ia"/>', "Key wheel")

def icon(name):
    body, label = D[name]
    return wrap(body, label)

def disc(name, bpm, era):
    import html
    n = html.escape(name)
    grooves = "".join(f'<circle cx="80" cy="80" r="{r}" class="dg-groove"/>' for r in range(36, 74, 5))
    return (f'<svg viewBox="0 0 160 160" role="img" aria-label="{n} record" xmlns="http://www.w3.org/2000/svg">'
            f'<circle cx="80" cy="80" r="76" class="dg-disc"/>{grooves}'
            f'<circle cx="80" cy="80" r="32" class="fm"/><circle cx="80" cy="80" r="3" class="fn2"/>'
            f'<text x="80" y="72" text-anchor="middle" class="dg-lab">{n}</text>'
            f'<text x="80" y="98" text-anchor="middle" class="dg-sub">{html.escape(bpm)}</text>'
            f'<path d="M24 52a64 64 0 0 1 28-30" class="dg-shine"/></svg>')
