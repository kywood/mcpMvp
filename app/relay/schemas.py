from pydantic import BaseModel
from typing import Optional


class FailurePayload(BaseModel):
    dag_id: str
    task_id: str
    run_id: str
    try_number: int
    exception: Optional[str] = None
    log_url: Optional[str] = None
    execution_date: Optional[str] = None