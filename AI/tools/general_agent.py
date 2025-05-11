import google.generativeai as genai

from typing import Dict, Any, List
import json # For parsing LLM response

from langchain_core.prompts.chat import SystemMessage
import os
from .state_management import AgentState, Sneaker, UserPreferences, Recommendation

class GeneralAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash') # Using a cost-effective and capable model

    def get_recommendations(self, state: AgentState) -> Dict[str, Any]:
        print("---AGENT: General Agent (LLM Decision Maker)---")
        
        if state.get("error_message"):
            print(f"GeneralAgent: Skipping due to previous error: {state['error_message']}")
            return {}

        aggregated_sneakers: List[Sneaker] = state.get("aggregated_sneakers", [])
        user_preferences: UserPreferences = state["user_preferences"]

        if not aggregated_sneakers:
            print("GeneralAgent: No sneakers were aggregated. Cannot make recommendations.")
            return {"final_recommendations": [], "error_message": "No sneakers found to recommend after filtering by brand agents."}

        # Construct the prompt for Gemini
        prompt_parts = [
            "You are an expert AI Sneaker Advisor.",
            "Your task is to analyze a list of available sneakers and a user\'s preferences to recommend the top 1 to 3 best-fitting sneakers.",
            "For each recommended sneaker, you MUST provide its exact name, brand, price, URL, image_url (if available), and a concise one-line reason for the recommendation based on the user\'s preferences and the sneaker\'s description.",
            "The user\'s budget has already been applied to filter the initial list, so focus on matching style, use case, color, and overall suitability based on the descriptions.",
            "If multiple sneakers are good fits, prioritize those that match more of the user\'s specific preferences (style, color, use case).",
            "Format your response as a JSON array of objects. Each object should represent a recommended sneaker and include the fields: \"name\", \"brand\", \"price\", \"url\", \"image_url\", \"reason\".",
            "If no sneakers from the list are a good match for the user\'s specific style, color, or use case preferences, return an empty JSON array [].",
            "\nUser Preferences:",
            f"- Gender/Age Group: {user_preferences['gender_age_group']}",
            f"- Budget Range: ${user_preferences['budget_range'][0]:.2f} - ${user_preferences['budget_range'][1]:.2f}",
            f"- Preferred Brands: {', '.join(user_preferences['preferred_brands']) if user_preferences['preferred_brands'] else 'Any'}",
            f"- Desired Style: {user_preferences.get('style', 'Not specified')}",
            f"- Desired Color: {user_preferences.get('color', 'Not specified')}",
            f"- Intended Use Case: {user_preferences.get('use_case', 'Not specified')}",
            "\nAvailable Sneakers (ensure your recommendations come ONLY from this list):"
        ]

        # Create a list of dictionaries, suitable for json.dumps
        sneaker_list_for_json = []
        for s_obj in aggregated_sneakers: # s_obj is a Sneaker TypedDict
            sneaker_dict = {
                "brand": s_obj['brand'],
                "name": s_obj['name'],
                "price": s_obj['price'],
                "description": s_obj['description'], # json.dumps will handle escaping
                "url": s_obj['url'],
                "image_url": s_obj.get('image_url', '') # Provide empty string if None, or adjust if null is preferred
            }
            sneaker_list_for_json.append(sneaker_dict)
        
        # Convert the list of dictionaries to a JSON string
        # indent=2 makes it more readable in the debug output of the prompt
        available_sneakers_json_str = json.dumps(sneaker_list_for_json, indent=2) 
        
        prompt_parts.append(available_sneakers_json_str)
        
        prompt_parts.append("\nBased on the user preferences and the available sneakers listed above, provide your top 1 to 3 recommendations in the specified JSON format.")
        
        final_prompt = "\n".join(prompt_parts)
        print("\n--- General Agent Prompt to Gemini ---")
        print(final_prompt)
        print("---------------------------------------\n")

        try:
            response = self.model.generate_content(final_prompt)
            
            print("--- Gemini Response Text ---")
            # print(response.text) # Full text for debugging
            # Clean the response text to extract valid JSON part
            # Gemini might add backticks or "json" prefix
            cleaned_response_text = response.text.strip()
            if cleaned_response_text.startswith("```json"):
                cleaned_response_text = cleaned_response_text[7:]
            if cleaned_response_text.endswith("```"):
                cleaned_response_text = cleaned_response_text[:-3]
            cleaned_response_text = cleaned_response_text.strip()
            
            print(f"Cleaned Response for JSON parsing: {cleaned_response_text}")

            llm_recommendations = json.loads(cleaned_response_text)
            
            # Validate and structure the recommendations
            final_recommendations: List[Recommendation] = []
            if isinstance(llm_recommendations, list):
                for rec_data in llm_recommendations:
                    if all(key in rec_data for key in ["name", "brand", "price", "url", "reason"]):
                        # Find the original image_url from aggregated_sneakers if not directly in LLM response, or use what LLM provided
                        original_sneaker = next((s for s in aggregated_sneakers if s['name'] == rec_data['name'] and s['brand'] == rec_data['brand']), None)
                        image_url = rec_data.get("image_url")
                        if not image_url and original_sneaker: # If LLM didn't provide image_url, try to get it from original data
                            image_url = original_sneaker.get("image_url")
                        
                        final_recommendations.append(Recommendation(
                            name=str(rec_data["name"]),
                            brand=str(rec_data["brand"]),
                            price=float(rec_data["price"]),
                            url=str(rec_data["url"]),
                            reason=str(rec_data["reason"]),
                            image_url=str(image_url) if image_url else None
                        ))
                    else:
                        print(f"GeneralAgent: LLM recommendation missing required keys: {rec_data}")
            
            if not final_recommendations and aggregated_sneakers:
                 print("GeneralAgent: LLM returned no valid recommendations, or no sneakers matched detailed criteria.")
                 # error_message = "The LLM advisor couldn\'t find a specific match based on your detailed preferences from the available options."
                 # return {"final_recommendations": [], "error_message": error_message} # Let workflow handle empty list

            print(f"GeneralAgent: Generated {len(final_recommendations)} recommendations.")
            return {"final_recommendations": final_recommendations}

        except json.JSONDecodeError as e:
            print(f"GeneralAgent: Error decoding JSON from LLM response: {e}")
            print(f"LLM Raw Response was: {response.text if 'response' in locals() else 'Response object not created'}")
            return {"error_message": f"LLMResponseParseError: Could not parse recommendations. Raw: {response.text if 'response' in locals() else 'N/A'}"}
        except Exception as e:
            print(f"GeneralAgent: An unexpected error occurred during LLM call: {e}")
            # Check if response object exists before trying to access its text attribute
            error_details = str(e)
            if 'response' in locals() and hasattr(response, 'text'):
                error_details += f" LLM Raw Response: {response.text}"
            return {"error_message": f"LLMError: {error_details}"}
