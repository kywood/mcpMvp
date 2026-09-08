from datetime import datetime
import time
from airflow import DAG
from airflow.operators.python import PythonOperator

#
# def triggerDag():
#     from airflow.api.client.local_client import Client
#     client = Client(api_base_url=None, auth=None)
#     client.trigger_dag(dag_id="realtime_parser_dag")
#
#     pass

def triggerDag():
    import requests


    resp = requests.post(
        "http://airflow-webserver:8080/api/v1/dags/realtime_parser_dag/dagRuns",
        json={"conf": {}},
        auth=("airflow", "airflow"),
        timeout=10,
    )
    resp.raise_for_status()
    print(f"Triggered dag_run_id={resp.json().get('dag_run_id')}")

def entry():
    print(f" consumer start!! ")

    while True:
        print(f" consumer start!! ")

        ## 여기서 realtime_parser_dag dag 를 트리거 해야함...

        triggerDag()


        time.sleep(6)


with DAG(
    dag_id="realtime_consumer_dag",
    description="Task 1개로 1,2,3,4,5 찍는 테스트용 DAG",
    schedule=None,  # 수동 트리거 전용
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,  # 동시에 여러 run이 겹쳐 돌지 않도록 제한
    tags=["mcpMvp", "test"],
) as dag:
    tasks = PythonOperator(
            task_id=f"realtime_consumer_task",
            python_callable=entry,
        )


