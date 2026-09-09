import os
import httpx
from fastmcp import Client as MCPClient
from db import save_rca_result

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434/api/chat")
MCP_URL = os.getenv("MCP_URL", "http://mcp-server:8001/mcp")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "airflow-sre")
MAX_TURNS = 6


def build_failure_prompt(payload: dict) -> str:
    return (
        f"Airflow 태스크 실패가 발생했습니다.\n"
        f"- dag_id: {payload.get('dag_id')}\n"
        f"- task_id: {payload.get('task_id')}\n"
        f"- run_id: {payload.get('run_id')}\n"
        f"- try_number: {payload.get('try_number')}\n"
        f"- exception:\n{payload.get('exception')}\n\n"
        f"위 실패의 근본 원인(RCA)을 분석해줘. 필요하면 도구를 사용해서 추가 정보를 조회해."
    )


def mcp_tool_to_ollama_schema(tool) -> dict:
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description or "",
            "parameters": tool.input_schema or {"type": "object", "properties": {}},
        },
    }


async def start_llm_analysis(row_id: int, payload: dict):
    try:
        async with MCPClient(MCP_URL) as mcp_client:
            tools = await mcp_client.list_tools()
            tool_schemas = [mcp_tool_to_ollama_schema(t) for t in tools]

            messages = [
                {"role": "system", "content": "너는 Airflow 실패를 분석하는 SRE 에이전트다. 근거 있는 RCA 결론을 한국어로 명확히 제시해라."},
                {"role": "user", "content": build_failure_prompt(payload)},
            ]

            async with httpx.AsyncClient(timeout=120) as http_client:
                for turn in range(MAX_TURNS):
                    resp = await http_client.post(
                        OLLAMA_URL,
                        json={
                            "model": OLLAMA_MODEL,
                            "messages": messages,
                            "tools": tool_schemas,
                            "stream": False,
                        },
                    )
                    resp.raise_for_status()
                    msg = resp.json()["message"]
                    messages.append(msg)

                    tool_calls = msg.get("tool_calls")
                    if not tool_calls:
                        rca_text = msg.get("content", "")
                        save_rca_result(row_id, rca_text, status="completed")
                        print(f"[llm_agent] RCA 완료 id={row_id}")
                        return

                    for call in tool_calls:
                        fn_name = call["function"]["name"]
                        fn_args = call["function"].get("arguments", {})
                        try:
                            result = await mcp_client.call_tool(fn_name, fn_args)
                            result_text = str(getattr(result, "data", result))
                        except Exception as e:
                            result_text = f"tool 호출 에러: {e}"

                        messages.append({"role": "tool", "content": result_text})

                save_rca_result(row_id, "MAX_TURNS 초과 - 결론 도출 실패", status="incomplete")
                print(f"[llm_agent] MAX_TURNS 초과 id={row_id}")

    except Exception as e:
        print(f"[llm_agent] 분석 중 에러: {e}")
        save_rca_result(row_id, f"분석 실패: {e}", status="error")