import openai

def get_ai_insight(indicator_name, indicator_value, api_key):
    """
    Generates an AI-driven insight for a given indicator and its value using LLM.

    Args:
        indicator_name (str): Name of the technical indicator.
        indicator_value (float): Value of the technical indicator.
        api_key(str) : API key for accessing the LLM

    Returns:
        str: AI-generated insight.
    """
    client = openai.OpenAI(api_key = api_key)
    try:
        prompt = f"Explain the significance of a {indicator_name} value of {indicator_value} in stock trading in one sentence."
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # Use "gpt-3.5-turbo" for faster and cheaper results
            messages=[{"role": "system", "content": "You are a stock trading expert."},
                      {"role": "user", "content": prompt}],
            temperature=0.5  # Moderate creativity
        )

        return response.choices[0].message.content.strip()
    
    except openai.AuthenticationError:
        return "Invalid OpenAI API key. Please check your API key in Streamlit secrets."
    except openai.RateLimitError:
        return "OpenAI API rate limit exceeded. Try again later."
    except Exception as e:
        return f"Error generating AI insight: {e}"
