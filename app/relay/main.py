from fastapi import FastAPI, BackgroundTasks
from schemas import FailurePayload
from db import insert_failure_log

app = FastAPI()


def process_failure(payload: dict):
    """백그라운드 처리: 지금은 저장까지만, 다음 단계에서 LLM 세션 오픈 예정"""
    try:
        row_id = insert_failure_log(payload)
        print(f"[relay] failure_logs 저장 완료 id={row_id}, task={payload['task_id']}")

        # TODO(다음 단계): 여기서 Ollama LLM 세션 열고 RCA 파이프라인 시작
        # start_llm_analysis(row_id, payload)

    except Exception as e:
        print(f"[relay] 처리 중 에러: {e}")


@app.post("/failure", status_code=202)
async def receive_failure(payload: FailurePayload, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_failure, payload.model_dump())
    return {"status": "accepted"}


@app.get("/health")
async def health():
    return {"status": "ok"}