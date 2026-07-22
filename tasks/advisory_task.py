# tasks/advisory_task.py

from crewai import Task


def create_advisory_task(agent, requirements: dict):
    """
    Creates the rental advice task for the Rental Advisor agent.

    This task runs AFTER the analysis task. CrewAI automatically passes
    the output of the previous task into this task's context.

    Args:
        agent: The Rental Advisor agent instance.
        requirements: The renter's requirements for personalising advice.
    """
    return Task(
        description=f"""
You are advising a renter based on the property analysis already completed.

THE RENTER'S SITUATION:
- Budget: NLE {requirements['budget']:,}
- Looking for: {requirements['bedrooms']} bedroom {requirements['property_type']}
- Preferred location: {requirements['location']}
- Their notes: {requirements['notes']}

Using the analysis provided to you, write a clear and helpful advisory report.

YOUR INSTRUCTIONS:

1. Start with a brief summary of what the analysis found.

2. For each affordable property (best to worst):
   - Explain in plain language why it does or does not suit this renter
   - Mention any risk flags and what they mean practically
   - Be honest about weaknesses, not just strengths

3. Give a clear FINAL RECOMMENDATION:
   - Name the single best property for this renter
   - Explain exactly why it is the best choice
   - Mention what the renter should be aware of before committing

4. Close with one practical piece of advice for this renter's situation.

Write as if you are speaking directly to the renter.
Use clear, simple language. Avoid jargon.
Be warm but honest.
""",
        expected_output=(
            "A personalised rental advisory report written directly to the renter, "
            "covering all shortlisted properties, risk explanations, a clear final "
            "recommendation, and one practical closing tip."
        ),
        agent=agent,
    )