from typing import List, Dict, TypedDict, Literal, Tuple, Optional, Annotated, Any

# Custom merge function for brand_data dictionaries
def merge_brand_data_dicts(d1: Dict[str, List[Any]], d2: Dict[str, List[Any]]) -> Dict[str, List[Any]]:
    """Merges two dictionaries containing brand sneaker data."""
    # Ensure inputs are dictionaries. If a branch doesn't run or returns None for brand_data,
    # it might pass None. Initialize with empty dicts if so.
    # However, the nodes are structured to always return a dict for brand_data, even if empty.
    merged = (d1 or {}).copy() # Start with a copy of the first dict
    for key, value_list in (d2 or {}).items():
        if key in merged:
            # This case should ideally not happen if each brand agent uses a unique key (brand name)
            # If it could, decide on merging logic (e.g., extend list, overwrite, error)
            # For now, let's assume keys are unique per brand agent call.
            # If a brand agent could be called multiple times with updates, this would need adjustment.
            merged[key].extend(value_list) # Example: if keys could collide and values are lists
        else:
            merged[key] = value_list
    return merged

class UserPreferences(TypedDict):
    preferred_brands: List[Literal["Nike", "Adidas", "Puma"]]
    gender_age_group: Literal["male", "female", "kid"]
    budget_range: Tuple[float, float]
    style: Optional[str]  # e.g., "sporty", "casual", "formal"
    color: Optional[str]
    use_case: Optional[str] # e.g., "running", "daily wear", "basketball"

class Sneaker(TypedDict):
    brand: str
    name: str
    price: float
    url: str
    gender: Literal["male", "female", "kid"]
    description: str
    image_url: Optional[str]

class Recommendation(TypedDict):
    name: str
    brand: str
    price: float
    url: str
    reason: str
    image_url: Optional[str]

class AgentState(TypedDict):
    user_preferences: UserPreferences
    selected_brands: List[Literal["Nike", "Adidas", "Puma"]]
    # Data from each brand agent will be collected here using our custom merge function
    brand_data: Annotated[Dict[str, List[Sneaker]], merge_brand_data_dicts]
    aggregated_sneakers: List[Sneaker]
    final_recommendations: List[Recommendation]
    error_message: Optional[str]
    # For Gemini API key
    gemini_api_key: str
