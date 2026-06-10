import re
import random
from datetime import datetime
RULES = [
    # Greetings
    {
        "patterns": [r"\b(hi|hello|hey|what'?s up)\b"],
        "responses": [
            "Hello! How can I help you today? 😊",
            "Hey there! What can I do for you?",
            "Hi! Nice to meet you. How can I assist?",
        ],
        "tag": "greeting",
    },

    # How are you
    {
        "patterns": [r"how are you", r"how('?re| are) (you|u) doing", r"how('?s| is) it going"],
        "responses": [
            "I'm doing great, thanks for asking! How about you?",
            "All systems running smoothly! What can I help you with?",
        ],
        "tag": "wellbeing",
    },

    # Name
    {
        "patterns": [r"what is your name", r"who are you"],
        "responses": [
            "I'm ChatBot — a simple chatbot built with rule-based logic!",
            "My name is ChatBot. Nice to meet you!",
        ],
        "tag": "identity",
    },

    # Time / Date
    {
        "patterns": [r"\btime\b", r"what time is it", r"current time"],
        "responses": ["__TIME__"],   # special token — replaced at runtime
        "tag": "time",
    },
    {
        "patterns": [r"\bdate\b", r"what is the date", r"what day is (it|today)"],
        "responses": ["__DATE__"],
        "tag": "date",
    },

    # Help
    {
        "patterns": [r"\bhelp\b", r"what can you do", r"what do you know"],
        "responses": [
            (
                "I can help you with:\n"
                "  • Greetings & small talk\n"
                "  • Telling you the current time & date\n"
                "  • Answering basic questions about me\n"
                "  • Jokes 😄\n"
                "  • Simple math calculations\n"
                "Just type naturally!"
            )
        ],
        "tag": "help",
    },

    # Jokes
    {
        "patterns": [r"\bjoke\b", r"tell me (a joke|something funny)", r"make me laugh"],
        "responses": [
            "Why do programmers prefer dark mode?\nBecause light attracts bugs! 🐛",
            "Why did the Python programmer wear glasses?\nBecause they couldn't C! 👓",
            "What do you call a sleeping dinosaur?\nA dino-snore! 🦕",
            "I told my computer I needed a break.\nNow it won't stop sending me Kit-Kat ads.",
        ],
        "tag": "joke",
    },

    # Math  (e.g., "what is 12 + 7?")
    {
        "patterns": [r"(what is|calculate|compute|solve)?\s*(-?\d+\.?\d*)\s*([+\-*/])\s*(-?\d+\.?\d*)"],
        "responses": ["__MATH__"],
        "tag": "math",
    },

    # Goodbye
    {
        "patterns": [r"\b(bye|goodbye|see you|later|take care|quit|exit)\b"],
        "responses": [
            "Goodbye! Have a wonderful day! 👋",
            "See you later! Take care!",
            "Bye! Come back anytime 😊",
        ],
        "tag": "farewell",
    },

    # Thanks
    {
        "patterns": [r"\b(thanks|thank you|thx)\b"],
        "responses": [
            "You're welcome! 😊",
            "Happy to help!",
            "Anytime! Let me know if you need anything else.",
        ],
        "tag": "thanks",
    },
]

# Default fallback responses when nothing matches
FALLBACK_RESPONSES = [
    "I'm not sure I understand. Could you rephrase that?",
    "Hmm, I don't have a rule for that yet. Try asking something else!",
    "That's beyond my current knowledge. I'm still learning! 🤖",
    "Could you elaborate a bit more? I want to make sure I help correctly.",
]


# ─────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────

def get_time_response() -> str:
    now = datetime.now()
    return f"The current time is {now.strftime('%I:%M %p')} "


def get_date_response() -> str:
    now = datetime.now()
    return f"Today is {now.strftime('%A, %B %d, %Y')} "


def evaluate_math(expression: str) -> str:
    """Safely evaluate a simple arithmetic expression."""
    try:
        # Extract numbers and operator
        match = re.search(r"(-?\d+\.?\d*)\s*([+\-*/])\s*(-?\d+\.?\d*)", expression)
        if match:
            a, op, b = float(match.group(1)), match.group(2), float(match.group(3))
            if op == "+" : result = a + b
            elif op == "-": result = a - b
            elif op == "*": result = a * b
            elif op == "/":
                if b == 0:
                    return "Division by zero is undefined! ⚠️"
                result = a / b
            # Return int if result is whole number
            return f"The answer is {int(result) if result == int(result) else round(result, 4)} "
    except Exception:
        pass
    return "I couldn't compute that. Please use a format like: 12 + 7"


# ─────────────────────────────────────────────
#  CORE MATCHING ENGINE
# ─────────────────────────────────────────────

def match_input(user_input: str) -> str:
    normalized = user_input.lower().strip()

    for rule in RULES:
        for pattern in rule["patterns"]:
            if re.search(pattern, normalized, re.IGNORECASE):
                response = random.choice(rule["responses"])

                # Handle runtime-computed responses
                if response == "__TIME__":
                    return get_time_response()
                if response == "__DATE__":
                    return get_date_response()
                if response == "__MATH__":
                    return evaluate_math(normalized)

                return response

    # Nothing matched
    return random.choice(FALLBACK_RESPONSES)


# ─────────────────────────────────────────────
#  CONVERSATION LOOP
# ─────────────────────────────────────────────

def run_chatbot():
    print("         🤖  ChatBot — Rule-Based Chatbot")
    print("     Type 'help' to see what I can do.")
    print("     Type 'quit' or 'bye' to exit.")
    print()

    conversation_history = []   # stores (user_msg, bot_reply) tuples

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nChatBot: Goodbye! 👋")
            break

        if not user_input:
            print("ChatBot: Please say something! I'm listening. 👂\n")
            continue

        response = match_input(user_input)
        conversation_history.append((user_input, response))

        print(f"ChatBot: {response}\n")

        # Exit condition
        if match_input(user_input) and any(
            re.search(p, user_input, re.IGNORECASE)
            for p in [r"\b(bye|goodbye|see you|later|quit|exit)\b"]
        ):
            break

    # Optional: show conversation summary
    if len(conversation_history) > 1:
        print("\n--- Conversation Summary ---")
        for i, (u, b) in enumerate(conversation_history, 1):
            print(f"  {i}. You: {u}")
            print(f"     Bot: {b}")
        print(f"\nTotal exchanges: {len(conversation_history)}")


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    run_chatbot()