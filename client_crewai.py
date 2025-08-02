from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from typing import List
import logging
import warnings
from pydantic import PydanticDeprecatedSince20

# Suppress Pydantic warning
warnings.filterwarnings("ignore", category=PydanticDeprecatedSince20)

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# define MCP server parameters
server_params={
    "url":"http://44.202.41.246:8000/sse?city=Jakarta",
    "transport": "sse"
}

# create weather agent
weather_agent=Agent(
    role="Weather Data Fetcher",
    goal="Fetch real-time weather data for a given city using an MCP server.",
    backstory="An AI skilled in retrieving and processing weather data from external APIs via MCP.",
    tools=[MCPServerAdapter(server_params)],
    verbose=True
)

# Summary Agent
summary_agent = Agent(
    role="Weather Analyst",
    goal="Summarize weather data into a concise report.",
    backstory="An AI expert in analyzing and presenting weather data clearly.",
    verbose=True
)

#tasks
weather_task=Task(
    description="Fetch the current weather for New York using the MCP weather server.",
    expected_output="A JSON string containing weather data for New York.",
    agent=weather_agent
)

summary_task = Task(
    description="Summarize the weather data into a human-readable report.",
    expected_output="A concise weather report for New York.",
    agent=summary_agent,
    context=[weather_task]  # Use output from weather_task
)

#crew
crew=Crew(
    agents=[weather_agent, summary_agent],
    tasks=[weather_task, summary_task],
    process=Process.sequential,
    verbose=True
)

# A2A Communication Setup
# A2A is implicit in CrewAI via task context; agents share data through task outputs
# Run the crew
def run_crew():
    try:
        logger.debug(f"Initial tools for weather_agent: {[tool.name for tool in weather_agent.tools]}")
        with MCPServerAdapter(server_params) as tools:
            logger.debug(f"Tools from context manager: {[tool.name for tool in tools]}")
            weather_agent.tools = tools
            result = crew.kickoff()
            logger.info("\nCrew Result:\n%s", result)
            return result
    except Exception as e:
        logger.error(f"Error running crew: {e}", exc_info=True)
        raise

if __name__=="__main__":
    run_crew()