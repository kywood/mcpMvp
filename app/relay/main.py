from fastapi import FastAPI, BackgroundTasks
from schemas import FailurePayload
from db import insert_failure_log
from llm_agent import start_llm_analysis

app = FastAPI()


async def process_failure(payload: dict):
    """백그라운드 처리: 저장 후 LLM RCA 파이프라인 시작"""
    try:
        row_id = insert_failure_log(payload)
        print(f"[relay] failure_logs 저장 완료 id={row_id}, task={payload['task_id']}")

        await start_llm_analysis(row_id, payload)

    except Exception as e:
        print(f"[relay] 처리 중 에러: {e}")


@app.post("/failure", status_code=202)
async def receive_failure(payload: FailurePayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_failure, payload.model_dump())
    return {"status": "accepted"}


@app.get("/health")
async def health():
    return {"status": "ok"}