# high_risk.py

def high_risk_support_message(stage="offer"):
    if stage == "offer":
        return (
            "It sounds like you're really struggling right now. "
            "I'm really glad you reached out.\n\n"
            "Would you like to write about what’s been hurting you?"
        )

    elif stage == "accept":
        return (
            "Thank you for trusting me with something so heavy.\n\n"
            "If things feel overwhelming, you might consider reaching out:\n"
            "📞 Befrienders (Malaysia): 03-7627 2929\n"
            "🌐 https://www.befrienders.org.my\n\n"
            "I’m still here with you."
        )

    elif stage == "refuse":
        return (
            "That’s okay. You don’t have to write if you’re not ready.\n\n"
            "You deserve support:\n"
            "📞 Befrienders (Malaysia): 03-7627 2929\n"
            "🌐 https://www.befrienders.org.my\n\n"
            "I’m here if you want to talk."
        )
