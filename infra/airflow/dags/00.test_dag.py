from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def print_number(n: int):
    print(f"{n}")


with DAG(
    dag_id="test_dag",

    description="1,2,3,4,5 찍고 끝나는 테스트용 DAG",
    schedule=None,          # 수동 트리거 전용 (자동 스케줄 없음)
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["mcpMvp", "test"],
) as dag:

    tasks = [
        PythonOperator(
            task_id=f"print_{i}",
            python_callable=print_number,
            op_kwargs={"n": i},
        )
        for i in range(1, 6)
    ]

    # 순차 실행: print_1 >> print_2 >> ... >> print_5
    for i in range(len(tasks) - 1):
        tasks[i] >> tasks[i + 1]