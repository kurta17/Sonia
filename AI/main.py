import os
from workflow import run_sneaker_workflow, UserPreferences

# Example: Get user preferences from a hypothetical frontend or input mechanism
def get_user_input() -> UserPreferences:
    # In a real application, this would come from a UI, API request, etc.
    # For this example, we'll use a hardcoded preference set.
    # You can change these values to test different scenarios.
    print("Simulating user input...")
    preferences: UserPreferences = {
        "preferred_brands": ["Nike"], # Can be ["Nike"], ["Adidas"], ["Puma"], or any combination
        "gender_age_group": "male",       # "male", "female", or "kid"
        "budget_range": (10.00, 520.00),   # (min_price, max_price)
        "style": "casual",                # Optional: e.g., "sporty", "casual", "formal", "running"
        "color": "black",                 # Optional: e.g., "red", "blue", "black"
        "use_case": "daily wear"           # Optional: e.g., "running", "gym", "daily wear", "skateboarding"
    }
    print(f"User preferences: {preferences}")
    return preferences

def main():
    print("--- Starting MargoAI Sneaker Advisor --- ")
    
    # --- Configuration ---
    # It's best practice to load API keys from environment variables
    # For local development, you might temporarily hardcode it or use a .env file (not shown here for simplicity)
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        # Fallback for the provided key if environment variable is not set
        # IMPORTANT: Avoid committing actual API keys to version control.
        # This is for demonstration; prefer environment variables in production/shared code.
        gemini_api_key = ""
        print("Warning: GEMINI_API_KEY environment variable not found. Using a hardcoded key for demonstration.")
        # print("Please set the GEMINI_API_KEY environment variable for secure API key management.")
        # return # Or raise an error

    if gemini_api_key == "" and not os.getenv("GEMINI_API_KEY"):
        print("Using the default provided API Key. Ensure this is intended for your tests.")

    # --- Get User Input ---
    user_prefs = get_user_input()

    # --- Run the Sneaker Advisor Workflow ---
    print("\n--- Invoking Sneaker Advisor Workflow ---")
    results = run_sneaker_workflow(preferences=user_prefs, gemini_api_key=gemini_api_key)

    # --- Display Results ---
    print("\n--- MananaAI Sneaker Advisor Results ---")
    if results.get("error"):
        print(f"Sorry, I couldn't find recommendations due to an error: {results['error']}")
    elif not results.get("recommendations"):
        print("Sorry, I couldn't find any sneakers that match your exact preferences this time. Try adjusting your criteria!")
    else:
        print("Here are your top sneaker recommendations:")
        for i, rec in enumerate(results["recommendations"]):
            print(f"\nRecommendation #{i+1}:")
            print(f"  Name: {rec['name']}")
            print(f"  Brand: {rec['brand']}")
            print(f"  Price: ${rec['price']:.2f}")
            print(f"  URL: {rec['url']}")
            if rec.get('image_url'):
                print(f"  Image: {rec['image_url']}")
            print(f"  Reason: {rec['reason']}")
    
    print("\n--- MargoAI Session Ended ---")

if __name__ == "__main__":
    main()
