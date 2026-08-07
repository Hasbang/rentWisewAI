# tasks/advisory_task.py

from crewai import Task


def create_advisory_task(agent, filter_results: dict, requirements: dict):
    """
    Creates the advisory task. Now aware of the Python-filtered results
    so it can give precise, reliable advice.
    """
    shortlist = filter_results["shortlist"]
    has_results = len(shortlist) > 0

    return Task(
        description=f"""
You are a Rental Advisor helping a renter make their final housing decision.

THE RENTER'S SITUATION:
- Budget: NLE {requirements['budget']:,}
- Looking for: {requirements['bedrooms']} bedroom {requirements['property_type']}
- Preferred location: {requirements['location']}
- Bathrooms needed: {requirements['bathrooms']}
- Their notes: {requirements['notes']}

SCREENING RESULTS:
- Properties analysed: {len(filter_results['shortlist']) + len(filter_results['rejected'])}
- Properties rejected: {len(filter_results['rejected'])}
- Properties shortlisted: {len(shortlist)}

{"The system found " + str(len(shortlist)) + " affordable propert" + ("y" if len(shortlist) == 1 else "ies") + " that match the renter's requirements." if has_results else "No properties matched the renter's budget and requirements."}

Using the analysis provided to you, write a clear and helpful advisory report.

YOUR INSTRUCTIONS:

{"For each shortlisted property (best to worst): explain in plain language why it suits or does not fully suit this renter, mention risk flags and what they mean practically, and be honest about weaknesses not just strengths." if has_results else "No properties were found. Explain this honestly and give 3 to 4 specific, practical suggestions the renter can act on to improve their chances - such as adjusting budget, broadening location, or reducing bedroom requirements."}

{"Give a clear FINAL RECOMMENDATION naming the single best property and explaining exactly why." if has_results else "Encourage the renter and remind them that the market changes regularly."}

Close with one practical piece of advice for this renter's specific situation.

Write directly to the renter. Use clear, simple language. Be warm but honest.
""",
        expected_output=(
            "A personalised rental advisory report written directly to the renter."
        ),
        agent=agent,
    )