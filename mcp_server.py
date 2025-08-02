from fastapi import FastAPI, APIRouter
from mcp.server.fastmcp import FastMCP
from fastapi.responses import StreamingResponse
import logging
import httpx
import json
import asyncio
from typing import Any

app = FastAPI()
router = APIRouter()  # Create a new FastAPI router
mcp = FastMCP('weather')

# Your WeatherAPI.com key (store securely in .env in production)
WEATHER_API_KEY = "YOUR_API_KEY"
BASE_URL = "http://api.weatherapi.com/v1"
user_agent = "weather-agent/1.0"

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Request
async def make_weatherapi_request(url: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": user_agent,
        "Accept": "application/json"
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"WeatherAPI request failed: {e}")
        return None

# Register the endpoint with FastAPI router
@router.get("/weather/{city}")
@mcp.tool()  # Assuming mcp.tool is a decorator for processing
async def get_weather(city: str) -> str:
    """Get current weather for a city using WeatherAPI.com."""
    url = f"{BASE_URL}/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"

    data = await make_weatherapi_request(url)
    if not data:
        return "Failed to fetch weather data."

    location = data.get("location", {})
    current = data.get("current", {})
    condition = current.get("condition", {})

    # resuilt
    result = {
        "city": location.get("name"),
        "region": location.get("region"),
        "country": location.get("country"),
        "local_time": location.get("localtime"),
        "latitude": location.get("lat"),
        "longitude": location.get("lon"),
        "temperature_c": current.get("temp_c"),
        "feelslike_c": current.get("feelslike_c"),
        "humidity": current.get("humidity"),
        "wind_kph": current.get("wind_kph"),
        "wind_dir": current.get("wind_dir"),
        "pressure_mb": current.get("pressure_mb"),
        "uv_index": current.get("uv"),
        "visibility_km": current.get("vis_km"),
        "condition": condition.get("text"),
        "condition_icon": condition.get("icon")
    }

    return json.dumps(result, indent=2)

# SSE for MCP Client access
async def sse_weather_stream(city: str = "Jakarta"):
    """Stream weather data for a city using SSE."""
    logger.debug(f"Starting SSE stream for {city}")
    while True:
        try:
            url = f"{BASE_URL}/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
            data = await make_weatherapi_request(url)
            if data:
                location = data.get("location", {})
                current = data.get("current", {})
                condition = current.get("condition", {})
                result = {
                    "city": location.get("name"),
                    "region": location.get("region"),
                    "country": location.get("country"),
                    "local_time": location.get("localtime"),
                    "latitude": location.get("lat"),
                    "longitude": location.get("lon"),
                    "temperature_c": current.get("temp_c"),
                    "feelslike_c": current.get("feelslike_c"),
                    "humidity": current.get("humidity"),
                    "wind_kph": current.get("wind_kph"),
                    "wind_dir": current.get("wind_dir"),
                    "pressure_mb": current.get("pressure_mb"),
                    "uv_index": current.get("uv"),
                    "visibility_km": current.get("vis_km"),
                    "condition": condition.get("text"),
                    "condition_icon": condition.get("icon")
                }
                logger.debug(f"SSE event for {city}: {result}")
                yield f"event: get_weather\ndata: {json.dumps(result)}\n\n"
            else:
                logger.error(f"SSE error for {city}: Failed to fetch data")
                yield f"event: error\ndata: {json.dumps({'error': 'Failed to fetch weather data'})}\n\n"
            await asyncio.sleep(60)
        except Exception as e:
            logger.error(f"SSE stream error for {city}: {e}")
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
            await asyncio.sleep(60)

@app.get("/sse")
async def sse_endpoint(city: str = "Jakarta"):
    """SSE endpoint for streaming weather updates."""
    logger.debug(f"SSE connection established for {city}")
    return StreamingResponse(sse_weather_stream(city), media_type="text/event-stream")

# Include the router in the FastAPI app
app.include_router(router)

# Start the server
if __name__ == "__main__":
    import uvicorn
    # host =0.0.0.0 for all
    uvicorn.run(app, host="127.0.0.1", port=8000)


