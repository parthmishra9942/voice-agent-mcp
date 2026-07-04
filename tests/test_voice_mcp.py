import json
from voice_mcp.protocol import MCPServer
from voice_mcp.agent import VoiceMCPAgent
from voice_mcp.audio_stream import VoiceActivityDetector
from voice_mcp.barge_in import BargeInInterruptionManager

def test_mcp_json_rpc_handshake():
    server = MCPServer()
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
    resp = json.loads(server.handle_request(init_req))
    assert resp["result"]["protocolVersion"] == "2024-11-05"

def test_voice_agent_tool_invocation():
    server = MCPServer()
    agent = VoiceMCPAgent(server)
    res = agent.process_user_turn("What was our Q2 sales revenue?")
    assert res["tool_executed"] == "query_sales_db"
    assert "4.25 million" in res["speech_out"]

def test_barge_in_interruption():
    vad = VoiceActivityDetector(energy_threshold=0.1)
    barge = BargeInInterruptionManager(vad)
    barge.on_agent_playback_start()

    # User speaks loudly mid-response (energy=0.8)
    should_interrupt = barge.on_audio_frame(0.8)
    assert should_interrupt is True
    assert barge.interrupted is True
