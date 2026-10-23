
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. Define the shared state
class RestaurantState(TypedDict):
    message: str


# 2. Define a node
def greet_customer(state: RestaurantState):
    return {
        "message": "Welcome to our restaurant!"
    }


# 3. Create the graph
builder = StateGraph(RestaurantState)

# 4. Add the node
builder.add_node("greet", greet_customer)

# 5. Connect START -> greet -> END
builder.add_edge(START, "greet")
builder.add_edge("greet", END)

# 6. Compile the graph
graph = builder.compile()

# 7. Execute the graph
result = graph.invoke({"message": "Hi!"})

print(result)
