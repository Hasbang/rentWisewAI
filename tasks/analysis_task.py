# tasks/analysis_task.py

from crewai import Task


def create_analysis_task(agent, properties: list, requirements: dict):
    """
    Creates the property analysis task for the Property Analyst agent.

    Args:
        agent: The Property Analyst agent instance.
        properties: The full list of property dictionaries from JSON.
        requirements: The renter's requirements as a dictionary.
    """

    # Format properties into readable text for the prompt
    properties_text = ""
    for p in properties:
        properties_text += f"""
Property ID: {p['id']}
Title: {p['title']}
Location: {p['location']}
Yearly Rent: NLE {p['yearlyRent']:,}
Advance Required: {p['advanceRequired']} year(s)
Move-in Cost: NLE {p['yearlyRent'] * p['advanceRequired']:,}
Bedrooms: {p['bedrooms']}
Bathrooms: {p['bathrooms']}
Type: {p['propertyType']}
Furnished: {p['furnished']}
Parking: {p['parking']}
Water Supply: {p['waterSupply']}
Electricity: {p['electricity']}
Description: {p['description']}
---"""

    return Task(
        description=f"""
You are analyzing rental properties for a renter with the following requirements:

RENTER REQUIREMENTS:
- Cash Available Today: NLE {requirements['budget']:,}
- Preferred Location: {requirements['location']}
- Bedrooms Needed: {requirements['bedrooms']}
- Bathrooms Needed: {requirements['bathrooms']}
- Property Type: {requirements['property_type']}
- Additional Notes: {requirements['notes']}

AVAILABLE PROPERTIES:
{properties_text}

YOUR INSTRUCTIONS:

Step 1 — Financial Filtering:
For each property, calculate: Move-in Cost = yearlyRent × advanceRequired
If Move-in Cost > renter's available cash, REJECT the property.
Clearly state which properties are rejected and why.

Step 2 — Risk Flagging:
For each affordable property, calculate: Remaining Cash = budget - Move-in Cost
If Remaining Cash < 10% of the original budget, flag it as HIGH UPFRONT CAPITAL RISK.

Step 3 — Preference Matching:
From the affordable properties, assess how well each matches:
- Location preference
- Number of bedrooms
- Number of bathrooms
- Property type
- Notes and special requirements

Step 4 — Ranking:
Rank the affordable properties from best match to worst match.
Give each a brief reason for its ranking position.

OUTPUT FORMAT:
Return a structured summary that includes:
1. Rejected properties (with reason)
2. Affordable properties ranked by match quality
3. Risk flags where applicable
4. A brief note on each property's strengths and weaknesses
""",
        expected_output=(
            "A structured analysis listing rejected properties with reasons, "
            "followed by affordable properties ranked by match quality, "
            "with risk flags and brief notes on each property's fit."
        ),
        agent=agent,
    )