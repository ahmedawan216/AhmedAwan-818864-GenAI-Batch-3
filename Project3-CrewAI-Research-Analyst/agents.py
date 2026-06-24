from crewai import Agent,LLM
from dotenv import load_dotenv
import os 
from crewai import LLM


llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)
load_dotenv()



research_agent=Agent(
    role="Reasearcher",
    goal="Research AI topics",
    backstory="Expert in AI and Machine Learning",
    llm=llm,
    verbose=True
)

summary_agent=Agent(
    role="Summerizer",
    goal="to Summerize AI repports",
    backstory="u are a smart researcher",
    llm=llm,
    verbose=True
)

gap_agent=Agent(
    role="Gap identidier",
    goal="Identify gaps in AI research",
    backstory="u are a smart researcher",
    llm=llm,
    verbose=True
)

writer_agent=Agent(
    role="Writer",
    goal="Write AI research papers",
    backstory="u are a smart researcher",
    llm=llm,
    verbose=True
)