from crewai import Crew, Process

from agents.property_analyst import create_property_analyst
from agents.rental_advisor import create_rental_advisor
from tasks.analysis_task import create_analysis_task
from tasks.advisory_task import create_advisory_task
from utils.data_loader import load_properties


def run_rentwise_crew(requirements:dict) -> str:
    """
    Assembles and runs the full RentWise AI crew.

    Args:
        requirements: Dictionary containing the renter's needs.

    Returns:
        The final advisory report as a string.
    """

    # Load property data 
    properties = load_properties()


    # create agents 

    analyst = create_property_analyst()
    advisor = create_rental_advisor()


    #create tasks 
    analysis = create_analysis_task(analyst, properties, requirements)
    advisory = create_advisory_task(advisor, requirements)

    #Assemble the crew 
    crew = Crew(

        agents=[analyst, advisor],
        tasks=[analysis, advisory],
        process=Process.sequential,
        verbose=True
    )

    # Run and return the result
    result = crew.kickoff()
    return str(result)
