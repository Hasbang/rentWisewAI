# crew/rentwise_crew.py

from crewai import Crew, Process

from agents.property_analyst import create_property_analyst
from agents.rental_advisor import create_rental_advisor
from tasks.analysis_task import create_analysis_task
from tasks.advisory_task import create_advisory_task
from utils.data_loader import load_properties
from utils.property_filter import filter_and_rank_properties


def run_rentwise_crew(requirements: dict) -> dict:
    """
    Assembles and runs the RentWise AI crew.
    Now returns both the AI report and the Python filter results
    so the UI can display structured property cards.

    Returns:
        dict with keys 'result' (AI report) and 'filter_results'
    """
    # Load properties from Supabase
    properties = load_properties()

    # ── PYTHON DOES THE MATHS ────────────────────────────────────
    filter_results = filter_and_rank_properties(properties, requirements)

    # Create agents
    analyst = create_property_analyst()
    advisor = create_rental_advisor()

    # Create tasks — pass filter_results instead of raw properties
    analysis = create_analysis_task(analyst, filter_results, requirements)
    advisory = create_advisory_task(advisor, filter_results, requirements)

    # Assemble and run the crew
    crew = Crew(
        agents=[analyst, advisor],
        tasks=[analysis, advisory],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    return {
        "result": str(result),
        "filter_results": filter_results,
    }