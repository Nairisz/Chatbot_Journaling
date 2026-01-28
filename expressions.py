# expressions.py

# ============================
# Lexicon
# ============================
JOY_WORDS = ["happy", "excited", "grateful", "thankful", "relieved", "proud", "content",
             "love"]

STRESS_WORDS = ["stress", "stressed", "pressure", "busy", "overwhelmed", "burnout"]

SAD_WORDS = ["sad", "down", "cry", "lonely", "empty", "lost", "hurt"]

FATIGUE_WORDS = ["tired", "exhausted", "sleepy", "drained", "haaaa", "sick", "fever",
                 "flu"]

UNCERTAIN_WORDS = ["not sure", "idk", "maybe", "confused", "meh", "okay i guess", 
                   "maybe nothing", "i guess"]

HIGH_RISK_WORDS = [
    "suicide", "kill myself", "give up", "worthless", 
    "hopeless", "end it all", "die", "off myself", "kms"
]

# ============================
# Expression tag
# ============================
def analyze_expression(text):
    text = text.lower()
    expressions = []

    if any(w in text for w in JOY_WORDS):
        expressions.append("Joy")

    if any(w in text for w in STRESS_WORDS):
        expressions.append("Stress")

    if any(w in text for w in SAD_WORDS):
        expressions.append("Sadness")

    if any(w in text for w in FATIGUE_WORDS):
        expressions.append("Fatigue")

    if any(w in text for w in UNCERTAIN_WORDS):
        expressions.append("Uncertain")

    if any(w in text for w in HIGH_RISK_WORDS):
        expressions.append("High Risk")

    if not expressions:
        expressions.append("General")

    return expressions or ["General"]