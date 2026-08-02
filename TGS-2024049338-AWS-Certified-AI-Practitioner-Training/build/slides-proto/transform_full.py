#!/usr/bin/env python3
"""1:1 transform: every slide of the original AWS deck -> a house-styled component slide.

Keeps the full slide count and all content + screenshots, but re-renders each slide in the
CLSSGB house design (eyebrow + title + footer + palette; dividers as section(), screenshots as
picture(), short lists as tile_grid(), prose as content()).

Loads the component functions from build_slides.py WITHOUT running its BUILD section, then drives
them from the original deck's per-slide content.
"""
import os, re, json
from pptx import Presentation
from pptx.util import Emu

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "..", "v11-work.pptx")            # original deck (374 slides, full images)
OUT  = os.path.join(HERE, "..", "..", "courseware", "AWS-AIF-C01-FULL-v13.pptx")

# ---- load components (everything before the BUILD marker) into a namespace ----
_src = open(os.path.join(HERE, "build_slides.py"), encoding="utf-8").read()
_comp = _src.split("# ============================================================ BUILD")[0]
NS = {"__file__": os.path.join(HERE, "build_slides.py")}
exec(compile(_comp, "build_slides.py", "exec"), NS)
cover, section, content, tile_grid, picture, two_col, cards3, big_statement, flow_h = (
    NS["cover"], NS["section"], NS["content"], NS["tile_grid"], NS["picture"],
    NS["two_col"], NS["cards3"], NS["big_statement"], NS["flow_h"])
prs = NS["prs"]

# ---- screenshot map: slide number -> [image files], from the manifest ----
man = json.load(open(os.path.join(HERE, "screens_manifest.json"), encoding="utf-8"))
SCREENS = {}
for m in man:
    SCREENS.setdefault(m["slide"], []).append(m)   # keeps w/h to pick the biggest

DOMWT = {1:"20%",2:"24%",3:"28%",4:"14%",5:"14%"}
DOMNAME = {1:"Fundamentals of AI and ML",2:"Fundamentals of Generative AI",
           3:"Applications of Foundation Models",4:"Guidelines for Responsible AI",
           5:"Security, Compliance, and Governance for AI Solutions"}

def slide_data(s):
    """Return (title, body_lines, layout_name)."""
    lines = []
    for sh in s.shapes:
        if sh.has_text_frame:
            for para in sh.text_frame.paragraphs:
                t = para.text.strip()
                if t:
                    lines.append(t)
    # drop the "#"/page-number stub and Maarek attribution and copyright
    lines = [l for l in lines if l not in ("#","") and "Maarek" not in l
             and not l.startswith("©") and not re.fullmatch(r'[\W_]{0,3}#[\W_]{0,3}', l)]
    lines = [l for l in lines if l.strip()]
    title = lines[0] if lines else ""
    body = lines[1:]
    return title, body, s.slide_layout.name

def is_short_list(body):
    return 2 <= len(body) <= 6 and all(len(b) <= 70 for b in body)

def biggest_image(n):
    ims = SCREENS.get(n, [])
    if not ims: return None
    return max(ims, key=lambda m: m.get("w",0)*m.get("h",0))["file"]

def main():
    p = Presentation(SRC)
    sl = list(p.slides)
    cur_dom = None; cur_kicker = None
    stats = {"cover":0,"section":0,"picture":0,"tile":0,"content":0,"skip":0}

    for i, s in enumerate(sl, 1):
        title, body, layout = slide_data(s)
        low = title.lower()

        # 1) cover
        if i == 1:
            cover(); stats["cover"]+=1; continue

        # 2) dividers: Domain / Task / Topic
        mdom = re.match(r'domain\s*([1-5])', low)
        mtask = re.match(r'task\s*([1-5]\.\d)', low)
        mtopic = re.match(r'topic\s*(\d+)', low)
        if layout == "SECTION_HEADER" or mdom or mtask or mtopic:
            if mdom:
                d = int(mdom.group(1)); cur_dom = d
                name = body[0] if body else DOMNAME.get(d,"")
                if "fundamental of al" in name.lower(): name = DOMNAME[d]
                section(f"DOMAIN {d}", name or DOMNAME[d], DOMWT.get(d,""),
                        sub=f"Exam weighting {DOMWT.get(d,'')} · {DOMNAME.get(d,'')}")
                cur_kicker = f"DOMAIN {d}"
            elif mtask:
                t = mtask.group(1)
                section(f"TASK {t}", (body[0] if body else title), "")
                cur_kicker = f"TASK {t}"
            elif mtopic:
                section(f"TOPIC {mtopic.group(1)}", (body[0] if body else title), "")
                cur_kicker = f"TOPIC {mtopic.group(1)}"
            else:
                # generic section header slide
                section((title.upper() if len(title) < 30 else "SECTION"),
                        (body[0] if body else title), "")
                cur_kicker = None
            stats["section"]+=1; continue

        # 3) slide has a screenshot -> picture()
        img = biggest_image(i)
        if img:
            cap = None
            if body:
                # use the first short body line as caption, else no caption
                cap = body[0] if len(body[0]) <= 120 else None
            picture(title or "Reference", img, caption=cap, kicker=cur_kicker)
            stats["picture"]+=1; continue

        # 4) empty-ish slide -> skip (keeps count honest; rare)
        if not title and not body:
            stats["skip"]+=1; continue

        # 5) short distinct list -> tile_grid ; else -> content (bullets)
        if is_short_list(body):
            tile_grid(title or "Overview", body, kicker=cur_kicker,
                      cols=(2 if len(body) <= 4 else 3), size=15)
            stats["tile"]+=1
        else:
            items = body if body else [title]
            content(title or "", items, kicker=cur_kicker, size=(18 if len(items) > 6 else 20))
            stats["content"]+=1

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    prs.save(OUT)
    n = len(prs.slides._sldIdLst)
    print(f"saved {os.path.basename(OUT)}  ({n} slides)")
    print("  ", stats)

if __name__ == "__main__":
    main()
