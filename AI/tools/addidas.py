from typing import Dict, Any, List
from .state_management import AgentState, Sneaker, UserPreferences

# Mock data - replace with actual API calls or scraping logic
MOCK_ADIDAS_SNEAKERS = [
    Sneaker(brand="Adidas", name="Adidas Ultraboost Light", price=180.00, url="https://adidas.com/ultraboostlight", gender="male", description="Experience epic energy with the new Ultraboost Light, our lightest Ultraboost ever.", image_url="https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/123/Ultraboost_Light.jpg"),
    Sneaker(brand="Adidas", name="Adidas Stan Smith", price=100.00, url="https://adidas.com/stansmith", gender="female", description="Timeless style for every day.", image_url="https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/456/Stan_Smith.jpg"),
    Sneaker(brand="Adidas", name="Adidas Grand Court", price=60.00, url="https://adidas.com/grandcourt", gender="kid", description="Comfortable shoes for little feet.", image_url="https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/789/Grand_Court.jpg"),
    Sneaker(brand="Adidas", name="Adidas NMD_R1", price=140.00, url="https://adidas.com/nmd_r1", gender="male", description="Progressive style with a comfortable feel.", image_url="https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/abc/NMD_R1.jpg"),
]

class AdidasDataCollectorAgent:
    def collect_data(self, state: AgentState) -> Dict[str, Any]:
        print("---AGENT: Adidas Data Collector---")
        preferences: UserPreferences = state["user_preferences"]
        gender = preferences["gender_age_group"]
        min_price, max_price = preferences["budget_range"]

        collected_sneakers: List[Sneaker] = []
        for sneaker in MOCK_ADIDAS_SNEAKERS:
            if sneaker["gender"] == gender and min_price <= sneaker["price"] <= max_price:
                collected_sneakers.append(sneaker)
        
        print(f"AdidasAgent: Found {len(collected_sneakers)} sneakers matching criteria.")
        return {"brand_data": {"Adidas": collected_sneakers}}
