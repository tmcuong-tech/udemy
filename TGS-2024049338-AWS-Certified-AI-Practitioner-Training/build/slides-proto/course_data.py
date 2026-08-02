"""
Course metadata for the AWS Certified AI Practitioner (AIF-C01) PROTOTYPE deck.

Mirrors the structure the reference build_slides.py expects. This prototype
covers front matter + Domain 1 only, so the slide list drives content directly;
this module supplies the metadata attributes the script reads.
"""

# ------------------------------------------------------------------ metadata
TITLE        = "AWS Certified AI Practitioner (AIF-C01)"
SHORT_TITLE  = "AWS Certified AI Practitioner (AIF-C01)"
COURSE_CODE  = "TGS-2024049338"
VERSION      = "v13.0"
VERSION_DATE = "21 July 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr. Alfred Ang"
DAYS         = 2

# ------------------------------------------------------------------ day themes
DAY_THEMES = {
    1: "Fundamentals of AI/ML & Generative AI",
    2: "Applications, Responsible AI, Security & Assessment",
}

# ------------------------------------------------------------------ assessment
ASSESSMENT = {
    "written":   "Written Assessment — Short-Answer Questions (WA-SAQ): 11 open-ended questions, 1 hour.",
    "practical": "Practical Assessment (Case Study): 5 lab-based tasks (A1-A5), 1 hour.",
    "note":      "A grade of Competent (C) in both instruments is required.",
}
