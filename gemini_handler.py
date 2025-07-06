# === gemini_handler.py ===

import google.generativeai as genai

def generate_with_gemini(prompt: str, api_key: str = None) -> str:
    """
    Generates content with Gemini 1.5 Flash model.
    Only uses the api_key passed as parameter to the function;
    if api_key is missing, throws an error.
    """
    if not api_key:
        raise ValueError(
            "Gemini API key not found. "
            "Please enter your own key from the sidebar."
        )

    # Configure with user-provided key only
    genai.configure(api_key=api_key)

    # Create model instance and generate content
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    try:
        response = model.generate_content(prompt)
        return response.text or "🛑 No response received."
    except Exception as e:
        return f"❌ Error occurred: {e}"