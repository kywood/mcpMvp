
from airflow import DAG
from airflow.operators.python import PythonOperator
import time
from datetime import datetime



def on_task_failure(context):
    """Task 실패 시 relay 서버로 POST (fire-and-forget)"""
    ti = context["task_instance"]
    exc = context.get("exception")
    import traceback
    exc_text = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)) if exc else "N/A"



    payload = {
        "dag_id": context["dag"].dag_id,
        "task_id": ti.task_id,
        "run_id": context["run_id"],
        "try_number": ti.try_number,
        "exception": exc_text,
        "log_url": ti.log_url,
        "execution_date": str(context.get("execution_date")),
    }
    try:
        import requests
        requests.post(
            "http://relay-server:8000/failure",
            json=payload,
            timeout=3,
        )
        print(f"[callback] relay 서버로 실패 알림 전송 완료: {payload['task_id']}")
    except Exception as e:
        # 콜백 자체가 죽으면 안되니까 여기선 그냥 로그만
        print(f"[callback] relay 서버 호출 실패: {e}")



def entry():
    print(f" parser dag start!! ")

    ## 한 11 초 쉬다가
    ## 20%의 확률로 실패하자


    time.sleep(5)

    import random
    if random.random() < 0.2:
        0/0
        100/0
        0/100

        # raise Exception("랜덤 실패 테스트 - 20% 확률로 발생")


    print("정상 종료")



with DAG(
    dag_id="realtime_parser_dag",
    description="Task 1개로 1,2,3,4,5 찍는 테스트용 DAG",
    schedule=None,  # 수동 트리거 전용
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=5,  # 동시에 여러 run이 겹쳐 돌지 않도록 제한
    tags=["mcpMvp", "test"],
) as dag:
    tasks = PythonOperator(
            task_id=f"realtime_parser_task",
            python_callable=entry,
            on_failure_callback=on_task_failure
        )


