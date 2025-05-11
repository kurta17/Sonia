from typing import Dict, Any, List
from .state_management import AgentState, UserPreferences

class BrandSelectorAgent:
    def select_brands(self, state: AgentState) -> Dict[str, Any]:
        print("---AGENT: Brand Selector---")
        user_preferences: UserPreferences = state["user_preferences"]
        preferred_brands = user_preferences.get("preferred_brands", [])
        
        # All known/supported brands by the system
        all_known_brands = ["Nike", "Adidas", "Puma"]
        
        selected_brands: List[str] = []

        if not preferred_brands: # If user provided no specific brands
            print("BrandSelectorAgent: No specific brands preferred by user. Selecting all known brands.")
            selected_brands = all_known_brands
        else:
            # Filter preferred brands to only those known by the system
            for brand in preferred_brands:
                if brand in all_known_brands:
                    selected_brands.append(brand)
                else:
                    print(f"BrandSelectorAgent: User preferred brand '{brand}' is not currently supported.")
            
            if not selected_brands:
                print("BrandSelectorAgent: None of the user-preferred brands are supported. Defaulting to all known brands to provide some options.")
                # Fallback: if user specified brands but none are supported, maybe offer all?
                # Or, this could be an error state / lead to no brands selected.
                # For a better UX, let's default to all known brands if their specific choices yield nothing.
                # This could be refined based on desired product behavior.
                selected_brands = all_known_brands 

        print(f"BrandSelectorAgent: Selected brands for processing: {selected_brands}")
        # Ensure brand_data is initialized for the merge strategy in AgentState
        # This is important because if this node is the first to try to write to brand_data (even if empty),
        # the key needs to exist for the Annotated merge function to work correctly if it's based on dict.update or similar.
        # However, the workflow initializes brand_data: {} in initial_state, so this might be redundant here
        # but doesn't hurt to ensure.
        return {"selected_brands": selected_brands, "brand_data": state.get("brand_data", {})}
