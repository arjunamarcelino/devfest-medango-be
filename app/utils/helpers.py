def generate_prompt(request):
    return f"""
    Create an itinerary for a {request.duration} trip with the following preferences:
    Activity Types: {', '.join(request.activity_types)}
    Travel Preferences: {request.travel_preferences}
    """

def query_openai(prompt):
    # Replace with Gemini API call
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()
