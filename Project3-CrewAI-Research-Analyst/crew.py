from crewai import Crew 
from agents import(
    research_agent,
    summary_agent,
    gap_agent,
    writer_agent
)

from tasks import create_task 

def create_crew(topic):
    tasks = create_task(topic)
    crew = Crew(
        agents=[
            research_agent,
            summary_agent,
            gap_agent,
            writer_agent
        ],
        tasks=tasks,
        verbose=True
    )
    return crew