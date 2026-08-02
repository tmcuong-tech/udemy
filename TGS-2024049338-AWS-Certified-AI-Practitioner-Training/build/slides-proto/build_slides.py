#!/usr/bin/env python3
"""Generate the AZ-104 course slide deck (all-white Tertiary house style).

Design helpers are the same set used by the tertiary-course-slides skill that
produced the n8n reference deck (cover, section, content, two_col, cards3,
big_statement, step_slide, test_slide, brk). Content is driven entirely by
course_data.py + data_domainN.py so the deck stays 100% aligned with the LP,
LG and labs.
"""
import os, sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import course_data as C

REPO = os.path.dirname(os.path.dirname(HERE))
ASSETS = os.path.join(HERE, "assets")

# ---------------- palette (matches reference) ----------------
BLUE=RGBColor(0x1F,0x6F,0xEB); TEAL=RGBColor(0x10,0xB9,0x81); AMBER=RGBColor(0xF5,0x9E,0x0B)
INK=RGBColor(0x16,0x1B,0x26); GREY=RGBColor(0x5B,0x63,0x72); LIGHT=RGBColor(0xF5,0xF8,0xFC)
WHITE=RGBColor(0xFF,0xFF,0xFF); LINE=RGBColor(0xE2,0xE8,0xF0); VIOLET=RGBColor(0x7C,0x3A,0xED)

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
SW,SH=prs.slide_width,prs.slide_height
BLANK=prs.slide_layouts[6]

def slide(): return prs.slides.add_slide(BLANK)
def rect(s,x,y,w,h,color,line=None):
    sp=s.shapes.add_shape(1,x,y,w,h); sp.fill.solid(); sp.fill.fore_color.rgb=color
    if line is None: sp.line.fill.background()
    else: sp.line.color.rgb=line; sp.line.width=Pt(1)
    sp.shadow.inherit=False; return sp
def oval(s,x,y,w,h,color):
    sp=s.shapes.add_shape(9,x,y,w,h); sp.fill.solid(); sp.fill.fore_color.rgb=color
    sp.line.fill.background(); sp.shadow.inherit=False; return sp
def txt(s,x,y,w,h,runs,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,space=4):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True; tf.vertical_anchor=anchor
    for i,line in enumerate(runs):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=align; p.space_after=Pt(space)
        for t,sz,col,bold in line:
            r=p.add_run(); r.text=t; r.font.size=Pt(sz); r.font.bold=bold
            r.font.color.rgb=col; r.font.name="Arial"
    return tb
def bullets(s,x,y,w,h,items,size=18,color=INK,gap=10,mcolor=BLUE):
    tb=s.shapes.add_textbox(x,y,w,h); tf=tb.text_frame; tf.word_wrap=True
    for i,it in enumerate(items):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph(); p.space_after=Pt(gap)
        lvl=it[1] if isinstance(it,tuple) else 0
        text=it[0] if isinstance(it,tuple) else it
        r=p.add_run(); r.text=("•  " if lvl==0 else "–  ")+text
        r.font.size=Pt(size if lvl==0 else size-2); r.font.color.rgb=color if lvl==0 else GREY
        r.font.name="Arial"; r.font.bold=(lvl==0 and isinstance(it,tuple) and len(it)>2 and it[2])
    return tb

PAGE={"n":0}
def footer(s):
    PAGE["n"]+=1
    txt(s,Inches(0.4),Inches(7.05),Inches(7.5),Inches(0.35),
        [[(f"{C.SHORT_TITLE}  ·  {C.COURSE_CODE}",9,GREY,False)]])
    txt(s,Inches(5.0),Inches(7.05),Inches(3.3),Inches(0.35),
        [[("© 2026 Tertiary Infotech Academy Pte Ltd",9,GREY,False)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(12.4),Inches(7.05),Inches(0.6),Inches(0.35),
        [[(str(PAGE["n"]),9,GREY,False)]],align=PP_ALIGN.RIGHT)
def head(s,title,kicker=None,kcolor=BLUE):
    rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),Inches(1.55),kcolor)
    if kicker: txt(s,Inches(0.85),Inches(0.5),Inches(11.6),Inches(0.4),[[(kicker,14,kcolor,True)]])
    # scale the title font by length so a 2-line title never overflows into the rule below
    tl=len(title or "")
    tsize = 29 if tl<=42 else (24 if tl<=72 else (20 if tl<=110 else 17))
    txt(s,Inches(0.85),Inches(0.83),Inches(11.9),Inches(0.82),[[(title,tsize,INK,True)]])
    rect(s,Inches(0.85),Inches(1.72),Inches(11.63),Inches(0.02),LINE)
    return s
def _logo(name):
    p=os.path.join(ASSETS,name)
    return p if os.path.exists(p) else None

# ---------------- slide templates ----------------
def cover():
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    rect(s,0,0,SW,Inches(0.22),BLUE); rect(s,0,Inches(7.28),SW,Inches(0.22),TEAL)
    org=_logo("tertiary-infotech-logo.png")
    if org: s.shapes.add_picture(org,Inches(0.85),Inches(0.7),height=Inches(1.05))
    # course badge (top-right) — AWS blue "AIF-C01"
    rect(s,Inches(11.0),Inches(0.72),Inches(1.55),Inches(1.0),BLUE)
    txt(s,Inches(11.0),Inches(0.82),Inches(1.55),Inches(0.5),[[("AIF-C01",20,WHITE,True)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(11.0),Inches(1.28),Inches(1.55),Inches(0.4),[[("AI PRACTITIONER",8,WHITE,True)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(0.9),Inches(2.3),Inches(12),Inches(0.6),[[("COURSE SLIDES  ·  WSQ",16,BLUE,True)]])
    txt(s,Inches(0.9),Inches(2.85),Inches(12.0),Inches(1.9),[[(C.TITLE,40,INK,True)]])
    rect(s,Inches(0.92),Inches(4.75),Inches(2.4),Inches(0.06),TEAL)
    txt(s,Inches(0.9),Inches(5.05),Inches(12),Inches(1.4),
        [[(f"WSQ Course Code: {C.COURSE_CODE}",16,GREY,False)],
         [("Conducted by Tertiary Infotech Academy Pte Ltd  ·  UEN 201200696W",14,GREY,False)]],space=6)
    txt(s,Inches(0.9),Inches(6.5),Inches(12),Inches(0.4),[[(f"Version {C.VERSION}  ·  {C.VERSION_DATE}",12,GREY,False)]])
    txt(s,Inches(0.9),Inches(6.85),Inches(12),Inches(0.34),[[("© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.  ·  www.tertiarycourses.com.sg",10,GREY,False)]])

def section(kicker,title,n,sub=""):
    s=slide(); rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),SH,BLUE)
    rect(s,Inches(0.85),Inches(2.5),Inches(0.14),Inches(2.0),TEAL)
    txt(s,Inches(1.25),Inches(2.55),Inches(11),Inches(0.6),[[(kicker,18,BLUE,True)]])
    txt(s,Inches(1.25),Inches(3.0),Inches(11.4),Inches(1.6),[[(title,40,INK,True)]])
    if sub: txt(s,Inches(1.27),Inches(4.55),Inches(11),Inches(0.8),[[(sub,16,GREY,False)]])
    txt(s,Inches(10.0),Inches(0.7),Inches(2.8),Inches(1.6),[[(n,72,RGBColor(0xE2,0xE8,0xF0),True)]],align=PP_ALIGN.RIGHT)
    footer(s)
def content(title,items,kicker=None,size=20):
    s=head(slide(),title,kicker); bullets(s,Inches(0.85),Inches(1.95),Inches(11.6),Inches(4.9),items,size=size); footer(s); return s
def picture(title,image_file,caption=None,kicker=None):
    """House-styled screenshot slide: eyebrow+title header, image fitted in the body, optional caption."""
    s=head(slide(),title,kicker)
    path=os.path.join(ASSETS,"screens",image_file)
    if not os.path.exists(path):
        txt(s,Inches(0.85),Inches(3.0),Inches(11.6),Inches(0.6),[[("[screenshot: "+image_file+"]",14,GREY,False)]])
        footer(s); return s
    from PIL import Image
    try:
        iw,ih=Image.open(path).size
    except Exception:
        iw,ih=16,9
    # fit within the body box (max 11.4 x 4.55 in), centred, leaving room for a caption
    bx,by,bw,bh=Inches(0.95),Inches(2.0),Inches(11.4),Inches(4.5 if caption else 4.9)
    ar=iw/ih; box_ar=bw/bh
    if ar>box_ar: w=bw; h=int(bw/ar)
    else: h=bh; w=int(bh*ar)
    x=int(bx+(bw-w)/2); y=int(by+(bh-h)/2); pad=int(0.03*914400)
    rect(s,x-pad,y-pad,w+2*pad,h+2*pad,LINE)  # thin frame
    s.shapes.add_picture(path,x,y,width=w,height=h)
    if caption:
        txt(s,Inches(0.95),Inches(6.55),Inches(11.4),Inches(0.4),[[(caption,12,GREY,False)]],align=PP_ALIGN.CENTER)
    footer(s); return s
def two_col(title,left,right,kicker=None,lhead="",rhead=""):
    s=head(slide(),title,kicker)
    rect(s,Inches(0.85),Inches(1.95),Inches(5.7),Inches(4.7),LIGHT); rect(s,Inches(6.95),Inches(1.95),Inches(5.55),Inches(4.7),LIGHT)
    if lhead: txt(s,Inches(1.1),Inches(2.15),Inches(5.2),Inches(0.4),[[(lhead,16,BLUE,True)]])
    if rhead: txt(s,Inches(7.2),Inches(2.15),Inches(5.0),Inches(0.4),[[(rhead,16,TEAL,True)]])
    bullets(s,Inches(1.1),Inches(2.7),Inches(5.2),Inches(3.8),left,size=16)
    bullets(s,Inches(7.2),Inches(2.7),Inches(5.05),Inches(3.8),right,size=16,mcolor=TEAL); footer(s); return s
def cards3(title,cards,kicker):
    s=head(slide(),title,kicker); xs=[Inches(0.85),Inches(5.0),Inches(9.15)]
    for i,c in enumerate(cards[:3]):
        x=xs[i]; col=c[0]
        rect(s,x,Inches(1.95),Inches(3.65),Inches(4.7),LIGHT); rect(s,x,Inches(1.95),Inches(3.65),Inches(0.12),col)
        txt(s,x+Inches(0.25),Inches(2.2),Inches(3.2),Inches(0.6),[[(c[1],19,col,True)]])
        bullets(s,x+Inches(0.25),Inches(2.95),Inches(3.2),Inches(3.4),c[2],size=14,mcolor=col,gap=9)
    footer(s); return s
def big_statement(line1,line2,kicker,color=BLUE):
    s=slide(); rect(s,0,0,SW,SH,WHITE); rect(s,0,0,Inches(0.28),SH,color)
    txt(s,Inches(1.1),Inches(2.2),Inches(11),Inches(0.5),[[(kicker,16,color,True)]])
    txt(s,Inches(1.1),Inches(2.8),Inches(11.3),Inches(2.4),[[(line1,38,INK,True)]])
    if line2: txt(s,Inches(1.12),Inches(4.9),Inches(11),Inches(1.2),[[(line2,20,GREY,False)]])
    footer(s); return s
import math
PALETTE=[BLUE,TEAL,VIOLET,AMBER]
def tile_grid(title,items,kicker=None,cols=2,size=15,icons=None,accent=BLUE):
    """Grid of light panels, each with a coloured icon/number badge + text.
    items: list of strings (or (title,caption) tuples). Much richer than a bullet list."""
    s=head(slide(),title,kicker,kcolor=accent)
    n=len(items); rows=math.ceil(n/cols)
    X0=Inches(0.85); Y0=Inches(1.95); TOTW=Inches(11.63); AREAH=Inches(4.78)
    gx=Inches(0.3); gy=Inches(0.26)
    cw=int((TOTW-gx*(cols-1))/cols); ch=int((AREAH-gy*(rows-1))/rows)
    bd=Inches(0.6)
    for i,it in enumerate(items):
        r=i//cols; c=i%cols
        x=int(X0+(cw+gx)*c); y=int(Y0+(ch+gy)*r); col=PALETTE[i%len(PALETTE)]
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,Inches(0.1),ch,col)
        oval(s,x+Inches(0.28),int(y+ch/2-bd/2),bd,bd,col)
        ic=icons[i] if icons else str(i+1)
        txt(s,x+Inches(0.28),int(y+ch/2-bd/2),bd,bd,[[(ic,19,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        tx=x+Inches(1.08); tw=cw-Inches(1.32)
        if isinstance(it,tuple):
            txt(s,tx,int(y+Inches(0.14)),tw,int(ch-Inches(0.2)),
                [[(it[0],size+2,INK,True)],[(it[1],size-2,GREY,False)]],anchor=MSO_ANCHOR.MIDDLE,space=3)
        else:
            txt(s,tx,int(y+Inches(0.1)),tw,int(ch-Inches(0.16)),[[(it,size,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def flow_h(title,steps,kicker=None,color=BLUE):
    """Horizontal numbered flow: coloured chips connected by chevrons."""
    s=head(slide(),title,kicker,kcolor=color)
    n=len(steps); X0=Inches(0.85); TOTW=Inches(11.63); gap=Inches(0.34)
    cw=int((TOTW-gap*(n-1))/n); y=Inches(2.55); ch=Inches(3.15); bd=Inches(0.82)
    for i,st in enumerate(steps):
        x=int(X0+(cw+gap)*i)
        rect(s,x,y,cw,ch,LIGHT); rect(s,x,y,cw,Inches(0.1),color)
        oval(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,color)
        txt(s,int(x+cw/2-bd/2),int(y+Inches(0.42)),bd,bd,[[(str(i+1),30,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
        txt(s,x+Inches(0.16),int(y+Inches(1.55)),cw-Inches(0.32),int(ch-Inches(1.7)),[[(st,14,INK,False)]],align=PP_ALIGN.CENTER)
        if i<n-1:
            txt(s,int(x+cw-Inches(0.04)),int(y+ch/2-Inches(0.3)),int(gap+Inches(0.08)),Inches(0.6),
                [[("▶",15,color,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def trainer_slide(kicker,name,role,rows,initials,accent=BLUE):
    """Profile-card layout: avatar badge + name/role panel on the left, labelled
    info tiles on the right. rows: list of (LABEL, value); blank value → fill-in line."""
    s=head(slide(),"About the Trainer",kicker,kcolor=accent)
    lx=Inches(0.85); lw=Inches(3.65)
    rect(s,lx,Inches(1.95),lw,Inches(4.7),LIGHT); rect(s,lx,Inches(1.95),lw,Inches(0.12),accent)
    bd=Inches(1.7); ax=int(lx+(lw-bd)/2)
    oval(s,ax,Inches(2.5),bd,bd,accent)
    txt(s,ax,Inches(2.5),bd,bd,[[(initials,44,WHITE,True)]],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    txt(s,lx+Inches(0.15),Inches(4.55),lw-Inches(0.3),Inches(0.6),[[(name,21,INK,True)]],align=PP_ALIGN.CENTER)
    txt(s,lx+Inches(0.15),Inches(5.2),lw-Inches(0.3),Inches(1.2),[[(role,13,GREY,False)]],align=PP_ALIGN.CENTER)
    rx=Inches(4.9); rw=Inches(7.6); ry=Inches(1.95); rh=Inches(4.7)
    n=len(rows); gy=Inches(0.2); th=int((rh-gy*(n-1))/n)
    for i,(label,val) in enumerate(rows):
        y=int(ry+(th+gy)*i); col=PALETTE[i%len(PALETTE)]
        rect(s,rx,y,rw,th,LIGHT); rect(s,rx,y,Inches(0.1),th,col)
        vruns=[(val,14,INK,False)] if val else [("____________________________________________",13,LINE,False)]
        txt(s,rx+Inches(0.32),y,rw-Inches(0.6),th,
            [[(label.upper(),11,col,True)],vruns],anchor=MSO_ANCHOR.MIDDLE,space=3)
    footer(s); return s
def activity_overview(tag,title,desc,build,services,kicker):
    s=head(slide(),title,kicker,kcolor=TEAL)
    rect(s,Inches(0.85),Inches(1.85),Inches(1.7),Inches(0.5),TEAL)
    txt(s,Inches(0.85),Inches(1.9),Inches(1.7),Inches(0.4),[[(tag,16,WHITE,True)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(0.85),Inches(2.55),Inches(11.7),Inches(1.6),[[(desc,21,INK,False)]])
    rect(s,Inches(0.85),Inches(4.3),Inches(11.7),Inches(2.0),LIGHT)
    txt(s,Inches(1.1),Inches(4.5),Inches(11),Inches(0.4),[[("You'll build",14,BLUE,True)]])
    txt(s,Inches(1.1),Inches(4.9),Inches(11),Inches(0.6),[[(build,18,INK,True)]])
    txt(s,Inches(1.1),Inches(5.6),Inches(11.2),Inches(0.6),[[("Azure services:  ",13,GREY,True),(services,13,GREY,False)]]); footer(s); return s
def step_slide(kicker,act_title,n,total,text,cmd=""):
    s=head(slide(),act_title,kicker,TEAL)
    oval(s,Inches(0.85),Inches(2.5),Inches(1.4),Inches(1.4),TEAL)
    txt(s,Inches(0.85),Inches(2.74),Inches(1.4),Inches(0.9),[[(str(n),38,WHITE,True)]],align=PP_ALIGN.CENTER)
    txt(s,Inches(0.95),Inches(1.95),Inches(11),Inches(0.4),[[(f"STEP {n} OF {total}",13,GREY,True)]])
    txt(s,Inches(2.55),Inches(2.4),Inches(10.1),Inches(1.3),[[(text,23,INK,False)]],anchor=MSO_ANCHOR.MIDDLE)
    if cmd:
        rect(s,Inches(2.55),Inches(4.15),Inches(10.1),Inches(0.95),RGBColor(0x0B,0x12,0x20))
        txt(s,Inches(2.8),Inches(4.28),Inches(9.7),Inches(0.7),[[("$ "+cmd,13,RGBColor(0x9C,0xDC,0xFE),False)]],anchor=MSO_ANCHOR.MIDDLE)
    footer(s); return s
def test_slide(act_title,text,kicker):
    s=head(slide(),act_title,kicker,TEAL)
    rect(s,Inches(0.85),Inches(2.3),Inches(11.7),Inches(2.6),RGBColor(0xE8,0xF7,0xEE))
    txt(s,Inches(1.2),Inches(2.6),Inches(11),Inches(0.5),[[("✅  Test it",20,RGBColor(0x12,0x7A,0x3E),True)]])
    txt(s,Inches(1.2),Inches(3.3),Inches(11),Inches(1.4),[[(text,18,INK,False)]]); footer(s); return s
def brk(kind,dur,color=AMBER):
    s=slide(); rect(s,0,0,SW,SH,WHITE)
    rect(s,0,0,SW,Inches(0.22),color); rect(s,0,Inches(7.28),SW,Inches(0.22),color)
    rect(s,Inches(5.4),Inches(2.35),Inches(2.53),Inches(0.1),color)
    txt(s,0,Inches(2.75),SW,Inches(1.2),[[(kind,48,INK,True)]],align=PP_ALIGN.CENTER)
    txt(s,0,Inches(4.05),SW,Inches(0.8),[[(dur,22,color,True)]],align=PP_ALIGN.CENTER); PAGE["n"]+=1

# ============================================================ BUILD
# 1
cover()

# 2 — ADMIN
section("COURSE ADMINISTRATION","Welcome & Housekeeping","")
# 3
content("Digital Attendance (Mandatory)",[
 "It is mandatory to take the AM, PM and Assessment digital attendance for WSQ-funded courses.",
 "The trainer/administrator displays the digital attendance QR code from the SSG portal.",
 "Scan the QR code with your mobile phone camera and submit your attendance.",
 "A minimum of 75% attendance is required to be eligible for assessment and funding."],kicker="TRAQOM · SSG DIGITAL ATTENDANCE")
# 4
trainer_slide("YOUR TRAINER · GENERAL","Your Trainer","General Trainer template —\nto be completed by the trainer",
 [("Name",""),("Title / Designation",""),("Qualifications",""),
  ("Areas of expertise",""),("Training & industry experience",""),("Contact","")],
 initials="?",accent=GREY)
# 5
trainer_slide("YOUR TRAINER",C.TRAINER,"Principal Trainer\nTertiary Infotech Academy Pte. Ltd.",
 [("Role","Principal Trainer, Tertiary Infotech Academy"),
  ("Certification","AWS certified — AI/ML and cloud."),
  ("Delivers","WSQ courses on AWS AI, cloud & automation."),
  ("Founder","Founder and lead instructor at Tertiary Infotech.")],
 initials="AA",accent=BLUE)
# 6
content("Let's Know Each Other",[
 "Your name and organisation / role.",
 "Your experience with AWS or other clouds and any AI/ML background.",
 "What you want to build with AWS AI services after this course."],kicker="ICE-BREAKER")
# 7
tile_grid("Ground Rules",[
 "Set your mobile phone to silent mode.","Participate actively — no question is too small.",
 "Mutual respect: agree to disagree.","One conversation at a time.",
 "Be punctual; return from breaks on time.","75% attendance is required."],
 kicker="HOUSEKEEPING",cols=2,size=15)
# 8
content("LMS / TMS",[
 "Access your course materials, attendance and assessment on the LMS/TMS portal.",
 "Portal: https://lms-tms.tertiaryinfotech.com",
 "Download the slides and Learner Guide for reference during the open-book assessment."],kicker="COURSE PORTAL")
# 9
two_col("Lesson Plan — 2 Days, 7 hours/day",[
 (f"Day 1 — {C.DAY_THEMES[1]}",0),
 ("Domain 1: Fundamentals of AI and ML (Labs 1–5)",1),
 ("Domain 2: Fundamentals of Generative AI (Labs 6–11)",1)],
 [(f"Day 2 — {C.DAY_THEMES[2]}",0),
 ("Domain 3: Applications of Foundation Models (Labs 12–18)",1),
 ("Domain 4: Responsible AI (Labs 19–22)",1),
 ("Domain 5: Security & Governance (Labs 23–25)",1),
 ("Final Assessment (WA + CS)",1)],
 kicker="SCHEDULE",lhead="Day 1",rhead="Day 2 & assessment")
# 10
tile_grid("Learning Outcomes",[
 ("Implement AI apps","Amazon Q Business and AWS AI models."),
 ("Deploy AI workflows","Bedrock workflows and ML techniques."),
 ("Identify & report issues","AI application and data issues."),
 ("Data interoperability","Maintain during AI development."),
 ("Data cleaning","Optimise AWS foundation models.")],
 kicker="WHAT YOU'LL ACHIEVE",cols=2,size=15)
# 11
content("Briefing for Assessment",[
 "Place phones and other materials under the table or on the floor.",
 "No photos or recording of assessment scripts.","No discussion during the assessment.",
 "Use a black/blue pen for hard-copy assessments.","No liquid paper / correction tape.",
 "Scripts are collected when time is up."])
# 12
content("Assessment",[
 C.ASSESSMENT["written"], C.ASSESSMENT["practical"],
 "Format: Open Book.",
 C.ASSESSMENT["note"]],kicker="FINAL ASSESSMENT")
# 13
flow_h("Assessment Flow",[
 "TRAQOM survey — scan the QR code on the LMS",
 "Assessment digital attendance — scan the SSG QR",
 "Sit WA (SAQ) then Case Study — open book",
 "Submit your answers on the LMS",
 "Sign the Assessment Summary Record"],kicker="ON ASSESSMENT DAY")

# ---------------- DOMAIN 1 ----------------
# 14
section("DOMAIN 1","Fundamentals of AI and ML","20%",sub="Exam weighting 20% · Tasks 1.1–1.3 · Labs 1–5")
# 15
tile_grid("AI, ML and Deep Learning",[
 ("Artificial Intelligence","Machines performing tasks that need human intelligence."),
 ("Machine Learning","Systems that learn patterns from data instead of explicit rules."),
 ("Deep Learning","Neural networks with many layers; powers vision and language."),
 ("Generative AI","Foundation models that generate new text, images, code.")],
 kicker="TASK 1.1 · TERMINOLOGY",cols=2,size=15)
# 16
cards3("Types of Machine Learning",[
 (BLUE,"Supervised",["Labelled data","Classification & regression","e.g. fraud detection"]),
 (TEAL,"Unsupervised",["Unlabelled data","Clustering","e.g. segmentation"]),
 (VIOLET,"Reinforcement",["Reward signal","Agent learns by trial","e.g. robotics"])],
 kicker="TASK 1.1 · LEARNING TYPES")
# 17
two_col("Inferencing & Data Types",[
 ("Inferencing",0),
 ("Batch — many predictions offline",1),
 ("Real-time — low-latency, one at a time",1)],
 [("Data types",0),
 ("Labelled vs unlabelled",1),
 ("Structured / tabular, time-series",1),
 ("Unstructured — text, image, audio",1)],
 kicker="TASK 1.1",lhead="Inference",rhead="Data")
# 18
tile_grid("Practical AI Use Cases",[
 ("Computer vision","Image classification, object detection."),
 ("NLP","Sentiment, entities, translation."),
 ("Speech","Transcription and text-to-speech."),
 ("Recommendation","Personalised suggestions."),
 ("Fraud detection","Anomaly detection on transactions."),
 ("Forecasting","Demand and time-series prediction.")],
 kicker="TASK 1.2 · USE CASES",cols=3,size=13)
# 19
tile_grid("AWS Managed AI Services",[
 ("Amazon SageMaker","Build, train, deploy ML models."),
 ("Amazon Comprehend","NLP — sentiment, entities."),
 ("Amazon Transcribe","Speech to text."),
 ("Amazon Translate","Language translation."),
 ("Amazon Polly","Text to speech."),
 ("Amazon Rekognition","Image & video analysis.")],
 kicker="TASK 1.2 · AWS AI SERVICES",cols=3,size=13)
# 20
big_statement("Use AI where patterns beat rules.","When you need a specific guaranteed outcome, a deterministic rule may be better than a prediction.","WHEN (NOT) TO USE AI",color=BLUE)
# 21
flow_h("The ML Development Lifecycle",[
 "Data collection & EDA","Pre-processing & feature engineering","Model training & tuning",
 "Evaluation","Deployment","Monitoring"],kicker="TASK 1.3 · ML PIPELINE")
# 22
tile_grid("Amazon SageMaker for the ML Lifecycle",[
 ("Data Wrangler","Prepare and engineer features."),
 ("Feature Store","Store and share features."),
 ("Training & tuning","Managed training, hyperparameter tuning."),
 ("Model Monitor","Detect drift in production."),
 ("Endpoints","Real-time and batch inference."),
 ("MLOps / Pipelines","Repeatable, automated workflows.")],
 kicker="TASK 1.3 · SAGEMAKER",cols=3,size=13)
# 23
content("Domain 1 — Key Takeaways",[
 "AI ⊃ ML ⊃ Deep Learning; Generative AI builds on foundation models.",
 "Three learning types: supervised, unsupervised, reinforcement.",
 "Inference can be batch or real-time; data is labelled/unlabelled, structured/unstructured.",
 "AWS managed AI services (SageMaker, Comprehend, Transcribe, Translate, Polly, Rekognition) solve common tasks.",
 "The ML lifecycle runs data → features → train → evaluate → deploy → monitor, orchestrated by Amazon SageMaker."],kicker="RECAP")

# ---- Domains 2-5: authored in separate modules, exec'd in this namespace ----
for _mod in ("dom2_slides.py","dom3_slides.py","dom4_slides.py","dom5_slides.py"):
    _p=os.path.join(HERE,_mod)
    if os.path.exists(_p):
        exec(compile(open(_p,encoding="utf-8").read(), _mod, "exec"))

# ---- Closing ----
section("WRAP-UP","Course Summary & Next Steps","")
tile_grid("What You Covered",[
 ("Domain 1","Fundamentals of AI and ML (20%)"),
 ("Domain 2","Fundamentals of Generative AI (24%)"),
 ("Domain 3","Applications of Foundation Models (28%)"),
 ("Domain 4","Guidelines for Responsible AI (14%)"),
 ("Domain 5","Security, Compliance & Governance (14%)")],kicker="THE FIVE EXAM DOMAINS",cols=2,size=15)
big_statement("You're ready to practise.","Complete the 25 hands-on labs, attempt the practice exams, then book your AIF-C01 exam.","NEXT STEPS",color=TEAL)
section("THANK YOU","See you in class","")

OUT=os.path.join(HERE,"..","..","courseware","AWS-AIF-C01-FULL-v13.pptx")
os.makedirs(os.path.dirname(OUT),exist_ok=True)
prs.save(OUT)
print(f"Saved {os.path.abspath(OUT)}  ({len(prs.slides.__iter__.__self__._sldIdLst)} slides)")
