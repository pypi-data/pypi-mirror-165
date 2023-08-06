from pydantic.main import BaseModel


class TrainCommand(BaseModel):
    dataset_name: str
    dataset_versions: list
    tenant_id: str
    machine_id: str
    task_id: str
