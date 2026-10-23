from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END


class RestaurantState(TypedDict):
    intent: str
    response: str


def understand_customer(state: RestaurantState):
    print("Understanding customer intent...")
    return {}


def route_intent(
    state: RestaurantState,
) -> Literal["menu", "booking", "order"]:
    if state["intent"] == "menu":
        return "menu"
    elif state["intent"] == "booking":
        return "booking"
    else:
        return "order"


def show_menu(state: RestaurantState):
    return {"response": "Today's menu: Pizza, Burger, Pasta."}


def book_table(state: RestaurantState):
    return {"response": "Let's help you book a table!"}


def place_order(state: RestaurantState):
    return {"response": "Let's take your food order!"}


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
        "booking": "order",
        "order": "order",
    },
)

builder.add_edge("menu", END)
builder.add_edge("booking", END)
builder.add_edge("order", END)

graph = builder.compile()

result = graph.invoke({
    "intent": "booking",
    "response": "",
})

print("Final State:", result)