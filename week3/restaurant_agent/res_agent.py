import os
from typing import TypedDict, Literal

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)


class RestaurantState(TypedDict):
    message: str
    intent: str
    response: str


def understand_customer(state: RestaurantState):
    prompt = f"""
    Classify this restaurant customer's intent.

    Customer message: {state["message"]}

    Choose exactly one category:
    - menu: asking about food or menu
    - booking: reserving a table
    - order: ordering food

    Return only the category name.
    """

    result = llm.invoke(prompt)
    intent = result.content.strip().lower()

    if intent not in {"menu", "booking", "order"}:
        intent = "menu"

    print("Detected intent:", intent)
    return {"intent": intent}


def route_intent(
    state: RestaurantState,
) -> Literal["menu", "booking", "order"]:
    return state["intent"]


def show_menu(state: RestaurantState):
    return {"response": "Today's menu: Pizza, Burger, Pasta."}


def book_table(state: RestaurantState):
    return {"response": "Sure! How many people and what time?"}


def place_order(state: RestaurantState):
    return {"response": "Sure! What would you like to order?"}


builder = StateGraph(RestaurantState)

builder.add_node("understand", understand_customer)
builder.add_node("menu", show_menu)
builder.add_node("booking", book_table)
builder.add_node("order", place_order)

builder.add_edge(START, "understand")

builder.add_conditional_edges(
    "understand",
    route_intent,
    {
        "menu": "menu",
        "booking": "booking",
        "order": "order",
    },
)

builder.add_edge("menu", END)
builder.add_edge("booking", END)
builder.add_edge("order", END)

graph = builder.compile()

customMessage = input("Hey There Iam Cody your tummy Buddy: ")
result = graph.invoke({
    "message": customMessage,
    "intent": "",
    "response": "",
})

print("Final response:", result["response"])