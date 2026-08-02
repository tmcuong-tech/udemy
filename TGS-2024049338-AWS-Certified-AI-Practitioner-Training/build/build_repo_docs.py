#!/usr/bin/env python3
"""Generate the repo-root README.md and LEARNER GUIDE.md from the lab set.

Mirrors the layout of the SAA-C03 course repo
(tertiarycourses/TGS-2024048315---AWS-Certified-Solutions-Architect-Associate-Training):
a catalogue README plus a single aggregated LEARNER GUIDE.md built from every lab.md.
"""
import json, os, re, glob

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
LABS = os.path.join(REPO, "labs")

COURSE = "AWS Certified AI Practitioner Training"
CODE   = "TGS-2024049338"
EXAM   = "AIF-C01"
CERT   = "https://aws.amazon.com/certification/certified-ai-practitioner/"

DOMAINS = [
    (1, "Fundamentals of AI and ML", 20, range(1, 6)),
    (2, "Fundamentals of Generative AI", 24, range(6, 12)),
    (3, "Applications of Foundation Models", 28, range(12, 19)),
    (4, "Guidelines for Responsible AI", 14, range(19, 23)),
    (5, "Security, Compliance and Governance for AI Solutions", 14, range(23, 26)),
]

def lab_dirs():
    out = {}
    for d in sorted(os.listdir(LABS)):
        m = re.match(r'lab-(\d\d)-', d)
        if m and os.path.isdir(os.path.join(LABS, d)):
            out[int(m.group(1))] = d
    return out

DIRS = lab_dirs()

def meta(n):
    d = DIRS[n]
    j = json.load(open(os.path.join(LABS, d, "index.json"), encoding="utf-8"))
    lab = open(os.path.join(LABS, d, "lab.md"), encoding="utf-8").read()
    obj = re.findall(r'^- (.+)$', lab.split("**Learning objectives:**")[-1].split("---")[0], re.M) \
          if "**Learning objectives:**" in lab else []
    slides = re.search(r'\*\*Slide reference:\*\*\s*(.+)', lab)
    return dict(dir=d, title=j["title"], desc=j["description"], time=j["time"],
                difficulty=j.get("difficulty", ""), steps=j["details"]["steps"],
                objectives=obj, slides=slides.group(1).strip() if slides else "", body=lab)

M = {n: meta(n) for n in DIRS}

def short_title(t):
    return re.sub(r'^Lab \d+\s*[—-]\s*', '', t)

def practise(n):
    """Short 'what you practise' phrase from the first three objectives."""
    objs = [re.sub(r'\.$', '', o).strip().lower() for o in M[n]["objectives"][:3]]
    return ", ".join(objs) if objs else M[n]["desc"].lower().rstrip(".")

# --------------------------------------------------------------------- README
def build_readme():
    L = []
    L.append(f"# {CODE} — {COURSE}\n")
    L.append(f"> **Course:** WSQ — {COURSE}  ")
    L.append(f"> **Course Code:** {CODE}  ")
    L.append(f"> **Certification:** [AWS Certified AI Practitioner ({EXAM})]({CERT})\n")
    L.append(f"These are the official hands-on lab exercises for the WSQ {COURSE} course "
             f"delivered by [**Tertiary Infotech Academy Pte Ltd**](https://www.tertiarycourses.com.sg/).\n")
    L.append(f"A complete set of **{len(DIRS)} step-by-step labs** aligned to the five official "
             f"**{EXAM} exam domains**. Every lab runs in your own AWS account and includes a cleanup step.\n")
    L.append("---\n")
    L.append("## How to use\n")
    L.append("1. Create a free tier AWS account: https://aws.amazon.com/free/")
    L.append("2. Secure it before you start — enable MFA on root, create an IAM admin user, set a billing alarm.")
    L.append("3. Install and configure the AWS CLI (see [labs/tools.md](labs/tools.md)):")
    L.append("   ```bash\n   aws configure\n   aws sts get-caller-identity\n   ```")
    L.append("4. Set the working region:")
    L.append("   ```bash\n   export AWS_DEFAULT_REGION=us-east-1\n   export AWS_PAGER=\"\"\n"
             "   export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)\n   ```")
    L.append("5. Request Amazon Bedrock model access before Lab 06 — approval is not always instant.")
    L.append("6. Work through the labs in order — each domain builds on the previous one.\n")
    L.append("> ⚠️ **Always complete the cleanup step.** SageMaker notebook instances, Studio apps and "
             "inference endpoints, OpenSearch Serverless collections, Kendra indexes and Amazon Q Business "
             "applications bill continuously whether or not you use them. Deleting a Bedrock knowledge base "
             "does **not** reliably delete the vector store beneath it — check every Region you used.\n")
    L.append("---\n")
    L.append("## Lab catalogue\n")
    for num, name, wt, rng in DOMAINS:
        L.append(f"### Domain {num} — {name} ({wt}%)\n")
        L.append("| Lab | Topic | What you practise |")
        L.append("|-----|-------|-------------------|")
        for n in rng:
            if n not in M: continue
            L.append(f"| [{n:02d}](labs/{M[n]['dir']}/) | {short_title(M[n]['title'])} | {practise(n)} |")
        L.append("")
    L.append("---\n")
    L.append("## Courseware\n")
    L.append("| Artifact | File |")
    L.append("|---|---|")
    L.append(f"| Master trainer slides (374 slides) | [`courseware/`](courseware/) — `.pptx` + `.pdf` |")
    L.append(f"| Learner Guide | [`courseware/`](courseware/) — `.docx` + `.pdf` |")
    L.append(f"| Lesson Plan | [`courseware/`](courseware/) — `.docx` + `.pdf` |")
    L.append(f"| Full lab walkthrough | [LEARNER GUIDE.md](LEARNER%20GUIDE.md) |")
    L.append(f"| Lab index | [labs/README.md](labs/README.md) |\n")
    L.append("> Assessment instruments (WA-SAQ and Case Study) and their answer keys are **not** in this "
             "repository. They are trainer-only and live in the course Google Drive folder.\n")
    L.append("---\n")
    L.append("## Exam domain weighting\n")
    L.append("| Domain | Weight | Labs |")
    L.append("|---|---|---|")
    for num, name, wt, rng in DOMAINS:
        have = [f"{n:02d}" for n in rng if n in M]
        L.append(f"| {num} — {name} | {wt}% | {have[0]}–{have[-1]} |")
    L.append("")
    L.append("---\n")
    L.append("## Repository structure\n")
    L.append("```")
    L.append(f"{CODE}---{COURSE.replace(' ', '-')}/")
    L.append("├── LEARNER GUIDE.md      full walkthrough of every lab")
    L.append("├── README.md")
    L.append("├── build/                generators for the deck, guide, lesson plan and labs")
    L.append("├── courseware/           slides, Learner Guide, Lesson Plan (docx + pdf)")
    L.append("└── labs/                 25 hands-on labs, one folder each")
    L.append("    ├── README.md         lab index with WSQ mapping")
    L.append("    ├── tools.md          AWS CLI setup")
    L.append("    └── lab-NN-slug/")
    L.append("        ├── index.json    manifest: title, time, steps")
    L.append("        ├── intro.md      what you will do")
    L.append("        ├── lab.md        the full lab")
    L.append("        ├── finish.md     recap and key takeaways")
    L.append("        └── stepN/text.md one file per step")
    L.append("```\n")
    L.append("---\n")
    L.append("## License\n")
    L.append(f"This material is provided for **educational use** as part of the WSQ course **{CODE}**. "
             "© Tertiary Infotech Academy Pte Ltd. All rights reserved.\n")
    p = os.path.join(REPO, "README.md")
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(L))
    return p

# ---------------------------------------------------------- LEARNER GUIDE.md
def build_learner_guide():
    L = []
    L.append(f"# {COURSE} ({EXAM}) — Learner Guide\n")
    L.append(f"**Course Code:** {CODE}  ")
    L.append("**Conducted by:** Tertiary Infotech Academy Pte Ltd · UEN 201200696W\n")
    L.append(f"Step-by-step walkthrough of all {len(DIRS)} hands-on labs, aligned to the five official "
             f"[{EXAM} exam domains]({CERT}).\n")
    L.append("**Lab environment:** your own AWS account ([free tier](https://aws.amazon.com/free/)) — "
             "region `us-east-1` unless stated otherwise.\n")
    L.append("> ⚠️ Every lab ends with a cleanup step. Complete it. Resources that bill continuously are "
             "called out in each lab's Clean up section.\n")
    L.append("---\n")
    L.append("## Contents\n")
    for num, name, wt, rng in DOMAINS:
        L.append(f"**Domain {num} — {name} ({wt}%)**\n")
        for n in rng:
            if n not in M: continue
            anchor = re.sub(r'[^a-z0-9 -]', '', M[n]['title'].lower()).replace(' ', '-')
            L.append(f"- [{M[n]['title']}](#{anchor}) — {M[n]['time']} min")
        L.append("")
    L.append("---\n")
    L.append("## Full walkthroughs\n")
    L.append("The complete step-by-step text for every lab is split by exam domain so each file "
             "renders in full on GitHub (a single combined file would exceed GitHub's 512 KB "
             "blob-rendering limit and be truncated).\n")
    L.append("| Domain | Labs | Walkthrough |")
    L.append("|---|---|---|")
    for num, name, wt, rng in DOMAINS:
        have = [f"{n:02d}" for n in rng if n in M]
        L.append(f"| {num} — {name} ({wt}%) | {have[0]}–{have[-1]} | "
                 f"[guides/domain-{num}.md](guides/domain-{num}.md) |")
    L.append("")
    L.append("Each lab folder also holds the same content as `lab.md`, plus one file per step "
             "under `stepN/text.md`.\n")
    L.append("---\n")
    L.append("Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.")
    p = os.path.join(REPO, "LEARNER GUIDE.md")
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(L))

    # per-domain walkthrough files
    gdir = os.path.join(REPO, "guides"); os.makedirs(gdir, exist_ok=True)
    for num, name, wt, rng in DOMAINS:
        G = [f"# Domain {num} — {name} ({wt}%)\n",
             f"Part of the [{COURSE} ({EXAM}) Learner Guide](../LEARNER%20GUIDE.md) · "
             f"course code {CODE}\n", "---\n"]
        for n in rng:
            if n not in M: continue
            body = M[n]["body"]
            body = re.sub(r'^# ', '## ', body, count=1, flags=re.M)
            body = re.sub(r'^## Step ', '### Step ', body, flags=re.M)
            body = re.sub(r'^## (Verification|Discussion questions)', r'### \1', body, flags=re.M)
            body = re.sub(r'\nCopyright 2026.*?All rights reserved\.\s*$', '', body, flags=re.S)
            G.append(body.rstrip()); G.append("\n---\n")
        G.append("Copyright 2026, Tertiary Infotech Academy Pte Ltd. All rights reserved.")
        gp = os.path.join(gdir, f"domain-{num}.md")
        open(gp, "w", encoding="utf-8", newline="\n").write("\n".join(G))
    return p

if __name__ == "__main__":
    for f in (build_readme, build_learner_guide):
        p = f()
        print(f"wrote {os.path.basename(p):22} {os.path.getsize(p)/1024:8.1f} KB")
    print(f"\nlabs aggregated: {len(M)}")
