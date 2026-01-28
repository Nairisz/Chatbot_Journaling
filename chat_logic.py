# chat_logic.py

from expressions import (
    analyze_expression, HIGH_RISK_WORDS, SAD_WORDS, STRESS_WORDS,
    FATIGUE_WORDS, JOY_WORDS, UNCERTAIN_WORDS
)
from high_risk import high_risk_support_message

def handle_idle_input(text, bot_say, session):
    if any(w in text for w in HIGH_RISK_WORDS):
        bot_say(high_risk_support_message("offer"))
        session.offer_journal = True
        session.high_risk = True

    elif any(w in text for w in SAD_WORDS):
        bot_say("I’m sorry you’re feeling this way. Would you like to write about it?")
        session.offer_journal = True

    elif any(w in text for w in STRESS_WORDS):
        bot_say("That sounds stressful. Do you want to reflect on it together?")
        session.offer_journal = True

    elif any(w in text for w in FATIGUE_WORDS):
        bot_say("You sound really tired. Want to talk about what drained you today?")
        session.offer_journal = True

    elif any(w in text for w in JOY_WORDS):
        bot_say("That sounds meaningful. Want to save it as a journal?")
        session.offer_journal = True

    elif any(w in text for w in UNCERTAIN_WORDS):
        bot_say("It’s okay to feel unsure. You can talk it out here.")

    else:
        bot_say("I'm listening. Tell me more.")
