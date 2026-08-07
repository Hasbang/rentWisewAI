# tasks/analysis_task.py

from crewai import Task


def create_analysis_task(agent, filter_results: dict, requirements: dict):
    """
    Creates the analysis task. Now receives pre-filtered results
    from Python rather than raw properties.

    Args:
        agent: The Property Analyst agent instance.
        filter_results: Output from filter_and_rank_properties()
        requirements: The renter's requirements dictionary.
    """
    shortlist = filter_results["shortlist"]
    rejected = filter_results["rejected"]

    # Format rejected properties
    rejected_text = ""
    for p in rejected:
        rejected_text += f"""
- {p['title']} ({p['location']})
  Move-in Cost: NLE {p['moveInCost']:,}
  Reason Rejected: {p['rejectionReason']}
"""

    # Format shortlisted properties
    shortlist_text = ""
    if shortlist:
        for i, p in enumerate(shortlist, 1):
            risk_flag = "⚠ HIGH UPFRONT CAPITAL RISK" if p["highRisk"] else "✅ Financially Safe"
            shortlist_text += f"""
Rank #{i} (Match Score: {p['matchScore']}/100)
Property ID: {p['id']}
Title: {p['title']}
Location: {p['location']}
Yearly Rent: NLE {p['yearlyRent']:,}
Advance Required: {p['advanceRequired']} year(s)
Move-in Cost: NLE {p['moveInCost']:,}
Remaining Cash After Move-in: NLE {p['remainingCash']:,}
Financial Risk: {risk_flag}
Bedrooms: {p['bedrooms']}
Bathrooms: {p['bathrooms']}
Type: {p['propertyType']}
Furnished: {p['furnished']}
Parking: {p['parking']}
Water Supply: {p['waterSupply']}
Electricity: {p['electricity']}
Description: {p['description']}
---"""
    else:
        shortlist_text = "No affordable properties found that match the renter's requirements."

    return Task(
        description=f"""
You are a Property Analyst reviewing the results of a financial screening
already completed by our system.

RENTER REQUIREMENTS:
- Budget: NLE {requirements['budget']:,}
- Location: {requirements['location']}
- Bedrooms: {requirements['bedrooms']}
- Bathrooms: {requirements['bathrooms']}
- Property Type: {requirements['property_type']}
- Notes: {requirements['notes']}

PROPERTIES REJECTED BY THE SYSTEM (do not reconsider these):
{rejected_text if rejected_text else "None"}

SHORTLISTED PROPERTIES (pre-ranked by match score):
{shortlist_text}

YOUR INSTRUCTIONS:
The financial filtering and ranking has already been done.
Do NOT recalculate costs or change the ranking order.

Your job is to:
1. Briefly confirm what the system found (how many rejected, how many shortlisted)
2. For each shortlisted property, explain WHY it scored well or poorly
3. For any HIGH UPFRONT CAPITAL RISK property, explain what that means practically
4. Note any strengths or weaknesses not captured by the score
5. Pass this analysis to the Rental Advisor
""",
        expected_output=(
            "A clear summary of the screening results with explanations "
            "of why each shortlisted property ranked where it did, "
            "including practical notes on any risk flags."
        ),
        agent=agent,
    )