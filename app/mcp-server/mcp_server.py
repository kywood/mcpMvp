from fastmcp import FastMCP
import httpx


mcp = FastMCP("mcpMvp")

AIRFLOW_URL = "http://airflow-webserver:8080"
AIRFLOW_USER = "airflow"
AIRFLOW_PASSWORD = "airflow"



@mcp.tool()
async def get_task_log(
    dag_id: str,
    dag_run_id: str,
    task_id: str,
    task_try_number: int = 1,
) -> str:
    """
    Airflow Task Instance의 실행 로그를 조회한다.

    Args:
        dag_id: DAG ID
        dag_run_id: DAG Run ID
        task_id: Task ID
        task_try_number: 실행 시도 번호
    """

    url = (
        f"{AIRFLOW_URL}/api/v1"
        f"/dags/{dag_id}"
        f"/dagRuns/{dag_run_id}"
        f"/taskInstances/{task_id}"
        f"/logs/{task_try_number}"
    )

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            url,
            auth=(AIRFLOW_USER, AIRFLOW_PASSWORD),
        )

        response.raise_for_status()

        return response.text


@mcp.tool()
def ping() -> str:
    """서버가 살아있는지 확인하는 테스트 툴 (동기 버전)"""
    return "pong"


@mcp.tool()
async def ping_async() -> str:
    """서버가 살아있는지 확인하는 테스트 툴 (비동기 버전)"""
    return "pong (async)"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8001)