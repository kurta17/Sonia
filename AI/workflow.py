from langgraph.graph import StateGraph, END
from typing import List, Dict, Literal, Any, Optional

from tools.state_management import AgentState, UserPreferences, Recommendation, Sneaker
from tools.selector import BrandSelectorAgent
from tools.nike import NikeDataCollectorAgent
from tools.addidas import AdidasDataCollectorAgent # Corrected filename if it was addidas.py
from tools.puma import PumaDataCollectorAgent
from tools.aggregator import AggregatorAgent
from tools.general_agent import GeneralAgent

# --- Define Nodes: Each node will call an agent method and update the state --- 

def brand_selector_node(state: AgentState) -> Dict[str, Any]:
    agent = BrandSelectorAgent()
    result = agent.select_brands(state)
    # Ensure brand_data is initialized if not already, for parallel branches
    if "brand_data" not in result:
        result["brand_data"] = {}
    return result

def nike_data_collector_node(state: AgentState) -> Dict[str, Any]:
    agent = NikeDataCollectorAgent()
    return agent.collect_data(state) # Expected to return {"brand_data": {"Nike": [...]}}

def adidas_data_collector_node(state: AgentState) -> Dict[str, Any]:
    agent = AdidasDataCollectorAgent()
    return agent.collect_data(state) # Expected to return {"brand_data": {"Adidas": [...]}}

def puma_data_collector_node(state: AgentState) -> Dict[str, Any]:
    agent = PumaDataCollectorAgent()
    return agent.collect_data(state) # Expected to return {"brand_data": {"Puma": [...]}}

def aggregator_node(state: AgentState) -> Dict[str, Any]:
    agent = AggregatorAgent()
    return agent.aggregate_sneakers(state)

def general_agent_node(state: AgentState) -> Dict[str, Any]:
    # The API key is passed in the initial state when the graph is invoked
    api_key = state.get("gemini_api_key")
    if not api_key:
        return {"error_message": "Gemini API key not found in state."}
    agent = GeneralAgent(api_key=api_key)
    return agent.get_recommendations(state)

def error_handler_node(state: AgentState) -> Dict[str, Any]:
    print(f"---WORKFLOW ERROR HANDLER---")
    error = state.get("error_message", "An unspecified error occurred.")
    print(f"Error in workflow: {error}")
    # Potentially clear recommendations if an error occurs upstream
    return {"final_recommendations": [], "error_message": error}

# --- Define Conditional Edges --- 

def route_from_brand_selector(state: AgentState) -> List[str] | str:
    if state.get("error_message"):
        return "error_handler_route"
    selected_brands = state.get("selected_brands", [])
    active_brand_routes = []
    if "Nike" in selected_brands:
        active_brand_routes.append("nike_agent_route")
    if "Adidas" in selected_brands:
        active_brand_routes.append("adidas_agent_route")
    if "Puma" in selected_brands:
        active_brand_routes.append("puma_agent_route")
    
    if not active_brand_routes:
        print("BrandSelectorRouter: No brands selected or to process. Routing to aggregator.")
        # If no brands are selected, we still go to aggregator to potentially handle this (e.g., return empty list)
        return "aggregator_direct_route"
    
    print(f"BrandSelectorRouter: Routing to {active_brand_routes}")
    return active_brand_routes

def route_after_aggregation(state: AgentState) -> str:
    if state.get("error_message"):
        return "error_handler_route"
    
    aggregated_sneakers = state.get("aggregated_sneakers", [])
    if not aggregated_sneakers:
        print("AggregatorRouter: No sneakers aggregated. Setting message and ending.")
        # This state will be returned to the user by the main run function
        # No need to route to LLM if there's nothing to recommend.
        # The main function will craft the final error/message.
        return END 
    return "general_agent_route"

# --- Build the Graph --- 
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("brand_selector", brand_selector_node)
workflow.add_node("nike_data_collector", nike_data_collector_node)
workflow.add_node("adidas_data_collector", adidas_data_collector_node)
workflow.add_node("puma_data_collector", puma_data_collector_node)
workflow.add_node("aggregator", aggregator_node)
workflow.add_node("general_agent_llm", general_agent_node)
workflow.add_node("error_handler", error_handler_node)

# Set entry point
workflow.set_entry_point("brand_selector")

# Conditional routing from brand selector
workflow.add_conditional_edges(
    "brand_selector",
    route_from_brand_selector,
    {
        "nike_agent_route": "nike_data_collector",
        "adidas_agent_route": "adidas_data_collector",
        "puma_agent_route": "puma_data_collector",
        "aggregator_direct_route": "aggregator", # If no brands selected, skip brand agents
        "error_handler_route": "error_handler"
    }
)

# Edges from brand data collectors to aggregator
workflow.add_edge("nike_data_collector", "aggregator")
workflow.add_edge("adidas_data_collector", "aggregator")
workflow.add_edge("puma_data_collector", "aggregator")

# Conditional routing from aggregator
workflow.add_conditional_edges(
    "aggregator",
    route_after_aggregation,
    {
        "general_agent_route": "general_agent_llm",
        "error_handler_route": "error_handler",
        END: END # If no sneakers aggregated, end the flow
    }
)

# Final steps
workflow.add_edge("general_agent_llm", END) # Successful path ends after LLM
workflow.add_edge("error_handler", END)    # Error path ends

# Compile the graph
app = workflow.compile()

# --- Main execution function (to be called by main.py) ---
def run_sneaker_workflow(preferences: UserPreferences, gemini_api_key: str) -> Dict[str, Any]:
    initial_state: AgentState = {
        "user_preferences": preferences,
        "selected_brands": [],
        "brand_data": {}, # Crucial for operator.add to work correctly from the start
        "aggregated_sneakers": [],
        "final_recommendations": [],
        "error_message": None,
        "gemini_api_key": gemini_api_key
    }
    
    print(f"Starting workflow with preferences: {preferences}")
    # config = {"recursion_limit": 25} # Default, adjust if needed
    final_state = app.invoke(initial_state) #, config=config)
    
    print("--- Workflow Ended --- Final State ---")
    # print(final_state) # For debugging the entire final state

    recommendations = final_state.get("final_recommendations", [])
    error_message = final_state.get("error_message")

    # Craft a user-friendly message if no recommendations and no specific error
    if not recommendations and not error_message:
        if not final_state.get("selected_brands"):
            error_message = "No brands were specified in your preferences. Please select at least one brand."
        elif not final_state.get("aggregated_sneakers"):
            error_message = "No sneakers were found matching your criteria (gender, budget) from the selected brands."
        else:
            error_message = "The AI advisor reviewed the available sneakers but could not find a specific match for your detailed preferences (style, color, use case). Try broadening your criteria."

    if error_message:
        print(f"Workflow resulted in an error/no recommendations: {error_message}")
        return {"error": error_message, "recommendations": []}
    
    print(f"Workflow successful. Recommendations: {len(recommendations)}")
    return {"recommendations": recommendations}

save_path = "workflow_graph.png"
graph = app.get_graph(xray=True).draw_mermaid_png()
with open(save_path, "wb") as f:
    f.write(graph)
