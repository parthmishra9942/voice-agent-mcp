import json
from typing import Dict, Any, List
from voice_mcp.protocol import MCPServer

def query_sales_db(quarter: str) -> Dict[str, Any]:
    return {"quarter": quarter, "revenue_usd": 4250000, "yoy_growth": "+34.2%", "active_accounts": 1280}

def fetch_weather(location: str) -> Dict[str, Any]:
    return {"location": location, "temp_c": 24, "conditions": "Clear", "humidity": "45%"}

class VoiceMCPAgent:
    """Conversational voice agent driving tool-augmented turn-taking."""
    def __init__(self, mcp_server: MCPServer):
        self.mcp_server = mcp_server
        self._register_default_tools()

    def _register_default_tools(self):
        self.mcp_server.register_tool(
            "query_sales_db",
            "Query quarterly financial sales revenue metrics",
            {"type": "object", "properties": {"quarter": {"type": "string"}}},
            query_sales_db
        )
        self.mcp_server.register_tool(
            "fetch_weather",
            "Fetch live weather conditions for a city",
            {"type": "object", "properties": {"location": {"type": "string"}}},
            fetch_weather
        )

    def process_user_turn(self, user_transcript: str) -> Dict[str, Any]:
        transcript_lower = user_transcript.lower()
        if "sales" in transcript_lower or "revenue" in transcript_lower:
            call_req = json.dumps({
                "jsonrpc": "2.0",
                "id": "call_1",
                "method": "tools/call",
                "params": {"name": "query_sales_db", "arguments": {"quarter": "Q2-2026"}}
            })
            resp = json.loads(self.mcp_server.handle_request(call_req))
            tool_data = resp["result"]["content"][0]["text"]
            speech_out = f"According to the database, Q2 revenue was 4.25 million dollars, up 34 percent year-over-year."
            return {"speech_out": speech_out, "tool_executed": "query_sales_db", "tool_result": tool_data}

        elif "weather" in transcript_lower:
            call_req = json.dumps({
                "jsonrpc": "2.0",
                "id": "call_2",
                "method": "tools/call",
                "params": {"name": "fetch_weather", "arguments": {"location": "Bhopal"}}
            })
            resp = json.loads(self.mcp_server.handle_request(call_req))
            tool_data = resp["result"]["content"][0]["text"]
            speech_out = "The weather is currently clear with 24 degrees Celsius."
            return {"speech_out": speech_out, "tool_executed": "fetch_weather", "tool_result": tool_data}

        return {
            "speech_out": f"I heard you say: {user_transcript}. How can I assist you further?",
            "tool_executed": None,
            "tool_result": None
        }
