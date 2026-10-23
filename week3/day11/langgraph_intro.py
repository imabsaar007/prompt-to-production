
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class RestaurantState(TypedDict):
    name: str
    greeting: str
    recommendation: str


# Node A: Greeting
def greet_customer(state: RestaurantState):
    print("Node A: Greeting customer")

    return {
        "greeting": f"Hello {state['name']}!"
    }


# Node B: Menu recommendation
def suggest_menu(state: RestaurantState):
    print("Node B: Suggesting menu")

    return {
        "recommendation": (
            f"{state['greeting']} Today's special is Pizza."
        )
    }


# Build graph
builder = StateGraph(RestaurantState)

builder.add_node("greet", greet_customer)
builder.add_node("menu", suggest_menu)

builder.add_edge(START, "greet")
builder.add_edge("greet", "menu")
builder.add_edge("menu", END)

graph = builder.compile()

result = graph.invoke({
    "name": "Absaar",
    "greeting": "",
    "recommendation": ""
})

print("\nFinal State:")
print(result)
