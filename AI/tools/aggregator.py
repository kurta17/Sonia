
from typing import Dict, Any, List
from .state_management import AgentState, Sneaker

class AggregatorAgent:
    def aggregate_sneakers(self, state: AgentState) -> Dict[str, Any]:
        print("---AGENT: Aggregator---")
        brand_data: Dict[str, List[Sneaker]] = state.get("brand_data", {})
        all_sneakers: List[Sneaker] = []

        for brand_name, sneaker_list in brand_data.items():
            if sneaker_list:
                all_sneakers.extend(sneaker_list)
            print(f"Aggregator: Received {len(sneaker_list) if sneaker_list else 0} sneakers from {brand_name}")

        # Simple deduplication based on brand and name
        deduplicated_sneakers_map: Dict[str, Sneaker] = {}
        for sneaker in all_sneakers:
            key = f"{sneaker['brand']}_{sneaker['name']}"
            if key not in deduplicated_sneakers_map:
                deduplicated_sneakers_map[key] = sneaker
        
        final_list = list(deduplicated_sneakers_map.values())
        print(f"Aggregator: Aggregated and deduplicated to {len(final_list)} sneakers.")
        return {"aggregated_sneakers": final_list}
