from app.models.request_models import ItineraryRequest

def generate_prompt(request: ItineraryRequest) -> str:
    prompt = f"""
    Create a personalized itinerary for a trip to Medan based on the following preferences:

    1. Duration: {request.duration}
    2. Trip Type: {request.trip_type} 
    3. Visitor Type: {request.visitor_type} 
    4. Activity Types: {', '.join(request.activity_types)}
    5. Travel Preferences: {request.travel_preferences} 
    6. Preferences: {request.preferences}
    7. Budget: {request.budget} in IDR

    Based on these details, suggest a variety of activities in Medan that align with the user's preferences. Provide the following information for each activity:

    - **Waktu (Time)**: The recommended time for the activity
    - **Lokasi/Tempat (Location)**: The name of the place or venue
    - **Alamat Lengkap (Full Address)**: The full address of the location
    - **Type Kegiatan (Activity Type)**: The type of activity (for use with an icon on the UI, such as "Culture", "Nature", "Shopping", etc.)
    
    Please provide the output in the following JSON format:

    {{
    "itinerary": [
    {{
      "day": ..,
      "time": ...,
      "location": ...,
      "full_address": ...,
      "activity_type": ...
    }},
    ...
    ],
    "notes": ....
    }}

    Additional considerations:
    - If the visitor type is "Turis" (tourist), make sure to include places where they can buy unique local souvenirs (oleh-oleh khas Medan) such as Bika Ambon, Durian Ucok, and local Batik stores.
    - If the preferences are "Outside Medan," include day trips or excursions to nearby areas in North Sumatra like Lake Toba, Berastagi, or Sibolangit, along with travel options and time estimates.
    - Focus on providing an enjoyable and enriching experience, considering their specific needs. The suggestions should be tailored to the visitor's type (tourist or local) and the trip's duration.
    """
    
    return prompt
