# MCP Server for Live Weather (with CrewAI- Agentic AI Solution)

This project implements an MCP (Model Context Protocol) server to fetch live weather details using the [WeatherAPI.com](https://www.weatherapi.com/) API. It supports querying weather data by city name or latitude/longitude and integrates with CrewAI for agent-based workflows and A2A (Agent-to-Agent) communication for collaborative data processing.

## *Author by Saida.D*

## Features
- **Real-Time Weather Data**: Fetch current weather conditions, including temperature, wind speed, humidity, and more.
- **Geolocation Support**: Query weather by city name or latitude/longitude coordinates.
- **CrewAI Integration**: Uses CrewAI agents for data retrieval and summarization.
- **A2A Communication**: Enables structured agent-to-agent interaction for enhanced data processing.
- **FastAPI with SSE**: Lightweight MCP server using Server-Sent Events for real-time communication.
- **Scalable and Secure**: Designed for scalability with robust error handling.

## Prerequisites
- Python 3.10 strictly equal or higher version (for crewai_tools)
- A free API key from [WeatherAPI.com](https://www.weatherapi.com/)
- Basic understanding of CrewAI, MCP, and A2A protocols

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/mcp-findweather.git
   cd mcp-findweather
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Packages**:
   Install the necessary Python packages using pip:
   ```bash
   pip install fastapi>=0.100.0 uvicorn>=0.22.0 pydantic>=2.0.0 python-dotenv>=1.0.0 httpx>=0.24.0 mcp>=1.2.1 crewai>=0.118.0 crewai-tools>=0.43.0 crewai-tools[mcp]
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the project root and add your WeatherAPI key:
   ```env
   WEATHER_API_KEY=your_weatherapi_key_here
   ```

## Project Structure
- `mcp_server.py`: MCP server implementation using FastAPI to fetch weather data.
- `client_crewai.py`: CrewAI workflow with agents for fetching and summarizing weather data.
- `.env`: Environment file for storing the WeatherAPI key.
- `README.md`: This file.

## Usage

1. **Start the MCP Server**:
   Run the MCP server to expose the `get_weather` tool:
   ```bash
   python mcp_server.py
   ```
   The server will be available at `http://localhost:8000/sse`.

2. **Run the CrewAI Workflow**:
   Execute the CrewAI script to fetch and summarize weather data:
   ```bash
   python client_crewai.py
   ```
   Example output:
   ```
   Weather Report for London: The current temperature is 11°C with a wind speed of 6.1 km/h. The weather is partly cloudy.
   ```

3. **Query Weather Data**:
   - By city: The server accepts city names (e.g., "London") and uses WeatherAPI's geolocation to fetch coordinates.
   - By coordinates: Pass latitude and longitude directly (e.g., `lat=51.52, lon=-0.11`).

## Example Code

### MCP Server (`mcp_server.py`)
```python
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import httpx
import json
from typing import Any
from pydantic import BaseModel
import os
from dotenv import load_dotenv

........
........
........

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

### CrewAI Workflow (`client_crewai.py`)
```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter

server_params = {
    "url": "http://localhost:8000/sse",
    "transport": "sse"
}
........
........
........
if __name__ == "__main__":
    run_crew()
```

## Configuration
- **WeatherAPI Key**: Obtain a free API key from [WeatherAPI.com](https://www.weatherapi.com/) and add it to the `.env` file.
- **MCP Server**: Runs on `localhost:8000` by default. Update the `server_params` in `crewai_weather.py` if hosted elsewhere.
- **A2A Communication**: Implicitly handled via CrewAI task context. Extend with explicit A2A protocols for complex workflows.

## Testing
1. **Test the MCP Server**:
   ```bash
   curl http://localhost:8000/sse
   ```
2. **Test Weather Data**:
   Use a tool like Postman to send a request:
   ```json
   {
       "city": "London"
   }
   ```
   Or:
   ```json
   {
       "lat": 51.52,
       "lon": -0.11
   }
   ```

## Deployment
- **Local Development**: Run locally for testing.
- **Cloud Deployment**: Deploy the MCP server on platforms like AWS, Azure, or Heroku for production use.
- **Security**: Bind the server to `127.0.0.1` for development and validate Origin headers for SSE connections.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for bugs, features, or improvements.

## License
MIT License
