# agents/rental_advisor.py

from crewai import Agent
from config.settings import llm


def create_rental_advisor():
    """
    Creates the Rental Advisor agent.

    This agent receives the filtered, ranked property list from the
    Property Analyst and focuses entirely on clear, empathetic advice
    to help the renter make their final decision.
    """
    return Agent(
        role="Rental Advisor",
        goal=(
            "Help the renter make a confident, informed housing decision "
            "by clearly explaining why each shortlisted property is a good "
            "or poor match, highlighting trade-offs, and giving a clear "
            "final recommendation with honest reasoning."
        ),
        backstory=(
            "You are a trusted housing advisor who has helped hundreds of "
            "families and professionals find homes in Freetown. "
            "You communicate clearly and honestly — you never oversell a property. "
            "You understand that choosing a home is one of the most stressful "
            "financial decisions a person makes, and you treat every renter "
            "with respect and patience. "
            "You always explain your reasoning so the renter feels informed, "
            "not just told what to do."
        ),
        llm=llm,
        verbose=True,
    )