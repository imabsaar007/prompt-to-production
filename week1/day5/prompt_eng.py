import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# --------------------------------------------------
# 1. RTCF + FEW-SHOT SYSTEM PROMPT
# --------------------------------------------------

SYSTEM_PROMPT = """
ROLE:
You are a helpful food-delivery chatbot assistant.

TASK:
Help users with restaurant discovery, food recommendations,
cuisine preferences, budgets, and basic ordering assistance.

CONTEXT:
You are part of a food-delivery application.
Be concise, friendly, and conversational.
Never invent restaurant names, prices, delivery times,
availability, or order status.
If information is unavailable, clearly say that you don't
have access to that information.

Do not claim that an order has been placed unless an
actual ordering tool confirms the order.

FORMAT:
Respond naturally and keep responses concise.


FEW-SHOT EXAMPLES:

Example 1:

User:
I want something spicy.

Assistant:
Sure! What cuisine are you in the mood for?


Example 2:

User:
I want biryani under 300 rupees.

Assistant:
Absolutely! Do you prefer chicken, mutton, or vegetarian biryani?


Example 3:

User:
I want pizza.

Assistant:
Sure! What type of pizza would you like, and what's your budget?


Example 4:

User:
I want something healthy under ₹250.

Assistant:
Got it! Would you prefer Indian, continental, or salad-based options?


Follow these examples to maintain the expected conversational style.
"""


# --------------------------------------------------
# 2. LLM CALL
# --------------------------------------------------

def call_llm(messages):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        temperature=0.4,
    )

    return response.choices[0].message.content


# --------------------------------------------------
# 3. FALLBACK PROMPT
# --------------------------------------------------

FALLBACK_PROMPT = """
You are a fallback food-delivery chatbot.

Answer the user's question safely and concisely.

Rules:
- Do not invent restaurant information.
- Do not invent prices or order status.
- If you don't know something, say so.
- Ask a clarifying question when necessary.
"""


# --------------------------------------------------
# 4. CHAT FUNCTION WITH FALLBACK
# --------------------------------------------------

conversation = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


def chat(user_message):

    # Add user message
    conversation.append({
        "role": "user",
        "content": user_message
    })

    try:

        # Primary prompt
        response = call_llm(conversation)

        # Save assistant response
        conversation.append({
            "role": "assistant",
            "content": response
        })

        return response

    except Exception as error:

        print(f"\nPrimary model failed: {error}")
        print("Using fallback...\n")

        fallback_messages = [
            {
                "role": "system",
                "content": FALLBACK_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ]

        try:

            response = call_llm(fallback_messages)

            conversation.append({
                "role": "assistant",
                "content": response
            })

            return response

        except Exception:

            return "Sorry, I'm having trouble right now. Please try again."


# --------------------------------------------------
# 5. CHAT LOOP
# --------------------------------------------------

print("🍔 Food Assistant")
print("Type 'exit' to quit.\n")


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Bot: Goodbye! 👋")
        break

    response = chat(user_input)

    print(f"Bot: {response}\n")