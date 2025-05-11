from typing import Dict, Any, List
from .state_management import AgentState, Sneaker, UserPreferences

# Mock data - replace with actual API calls or scraping logic
MOCK_NIKE_SNEAKERS = [
    Sneaker(brand="Nike", name="Nike Air Max 270", price=150.00, url="https://nike.com/airmax270", gender="male", description="The Nike Air Max 270 features Nike’s biggest and boldest Max Air unit yet.", image_url="https://static.nike.com/a/images/t_PDP_864_v1/f_auto,b_rgb:f5f5f5/abc/nike-air-max-270.png"),
    Sneaker(brand="Nike", name="Nike Revolution 6", price=65.00, url="https://nike.com/revolution6", gender="female", description="Lightweight comfort for your run.", image_url="https://static.nike.com/a/images/t_PDP_864_v1/f_auto,b_rgb:f5f5f5/def/nike-revolution-6.png"),
    Sneaker(brand="Nike", name="Nike Flex Runner 2", price=50.00, url="https://nike.com/flexrunner2", gender="kid", description="Easy to slip on, super flexible for kids.", image_url="https://static.nike.com/a/images/t_PDP_864_v1/f_auto,b_rgb:f5f5f5/ghi/nike-flex-runner-2.png"),
    Sneaker(brand="Nike", name="Nike Air Force 1", price=110.00, url="https://nike.com/airforce1", gender="male", description="Iconic style that transcends generations.", image_url="https://static.nike.com/a/images/t_PDP_864_v1/f_auto,b_rgb:f5f5f5/jkl/nike-air-force-1.png"),
]

class NikeDataCollectorAgent:
    def collect_data(self, state: AgentState) -> Dict[str, Any]:
        print("---AGENT: Nike Data Collector---")
        preferences: UserPreferences = state["user_preferences"]
        gender = preferences["gender_age_group"]
        min_price, max_price = preferences["budget_range"]

        collected_sneakers: List[Sneaker] = []
        for sneaker in MOCK_NIKE_SNEAKERS:
            if sneaker["gender"] == gender and min_price <= sneaker["price"] <= max_price:
                collected_sneakers.append(sneaker)
        
        print(f"NikeAgent: Found {len(collected_sneakers)} sneakers matching criteria.")
        # The key "Nike" must match the brand name for the aggregator
        return {"brand_data": {"Nike": collected_sneakers}} 
