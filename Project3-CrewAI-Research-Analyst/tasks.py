from crewai import Task
from agents import (
    research_agent,
    summary_agent,
    gap_agent,
    writer_agent
)


def create_task(topic):
    research_task=Task(
        description=f"Research on {topic}",
        expected_output="A report on {topic}",
        agent=research_agent
    )
    summary_task=Task(
        description=f"Summarize the report on {topic}",
        excpected_output="A summary of the report on {topic}",
        agent=summary_agent
    )
    gap_task=Task(
        description=f"Identify gaps in the report on {topic}",
        excpected_output="A list of gaps in the report on {topic}",
        agent=gap_agent
    )
    
    writer_task=Task(
        description=f"Write a research paper on {topic}",
        excpected_output="A research paper on {topic}",
        agent=writer_agent
    )
    
    return[
        research_task,
        summary_task,
        gap_task,
        writer_task
    ]