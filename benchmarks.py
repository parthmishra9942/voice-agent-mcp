import time
from voice_mcp.protocol import MCPServer
from voice_mcp.agent import VoiceMCPAgent

print("=== Sub-Second Voice AI Pipeline Latency Benchmark ===")
server = MCPServer()
agent = VoiceMCPAgent(server)

# Warmup
_ = agent.process_user_turn("Check weather in Bhopal")

latencies = []
for _ in range(100):
    t0 = time.perf_counter()
    _ = agent.process_user_turn("Check weather in Bhopal")
    t1 = time.perf_counter()
    latencies.append((t1 - t0) * 1000)

avg_ms = sum(latencies) / len(latencies)
p95_ms = sorted(latencies)[95]
print(f"Total Iterations: 100 turns")
print(f"Average MCP Tool Dispatch + Reasoning Latency: {avg_ms:.2f} ms")
print(f"P95 Latency: {p95_ms:.2f} ms")
print(f"Throughput: {1000 / avg_ms:.0f} turns/sec")
