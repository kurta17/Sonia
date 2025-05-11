from typing import Dict, Any, List
from .state_management import AgentState, Sneaker, UserPreferences

# Mock data - replace with actual API calls or scraping logic
MOCK_PUMA_SNEAKERS = [
    Sneaker(brand="Puma", name="Puma Suede Classic XXI", price=75.00, url="https://puma.com/suedeclassic", gender="male", description="The iconic PUMA Suede, a footwear legend.", image_url="https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:fafafa,w_1200,h_1200/global/374915/01/sv01/fnd/PNA/fmt/png/PUMA-Suede-Classic-XXI-Men's-Sneakers"),
    Sneaker(brand="Puma", name="Puma Carina Street", price=65.00, url="https://puma.com/carinastreet", gender="female", description="Retro sport-inspired, platform style.", image_url="https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:fafafa,w_1200,h_1200/global/389390/01/sv01/fnd/PNA/fmt/png/Carina-Street-Women's-Sneakers"),
    Sneaker(brand="Puma", name="Puma Anzarun Lite SlipOn", price=50.00, url="https://puma.com/anzarunliteslipon", gender="kid", description="Lightweight and easy for kids on the go.", image_url="https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:fafafa,w_1200,h_1200/global/377493/02/sv01/fnd/PNA/fmt/png/Anzarun-Lite-Slip-On-Kids'-Shoes"),
    Sneaker(brand="Puma", name="Puma RS-X Efekt", price=110.00, url="https://puma.com/rsxefekt", gender="male", description="Futuristic design with bold detailing.", image_url="https://images.puma.com/image/upload/f_auto,q_auto,b_rgb:fafafa,w_1200,h_1200/global/390776/01/sv01/fnd/PNA/fmt/png/RS-X-Efekt-Gradient-Men's-Sneakers"),
]

class PumaDataCollectorAgent:
    def collect_data(self, state: AgentState) -> Dict[str, Any]:
        print("---AGENT: Puma Data Collector---")
        preferences: UserPreferences = state["user_preferences"]
        gender = preferences["gender_age_group"]
        min_price, max_price = preferences["budget_range"]

        collected_sneakers: List[Sneaker] = []
        for sneaker in MOCK_PUMA_SNEAKERS:
            if sneaker["gender"] == gender and min_price <= sneaker["price"] <= max_price:
                collected_sneakers.append(sneaker)
        
        print(f"PumaAgent: Found {len(collected_sneakers)} sneakers matching criteria.")
        return {"brand_data": {"Puma": collected_sneakers}}
