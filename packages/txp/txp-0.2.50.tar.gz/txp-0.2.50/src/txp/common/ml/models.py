from enum import Enum
from pydantic import BaseModel
from typing import Union


class ModelFeedback(BaseModel):
    pass


class ErrorModelFeedback(ModelFeedback):
    error_message: str


class SuccessModelFeedback(ModelFeedback):
    metrics: dict


class DefaultModelFeedback(ModelFeedback):
    pass


class ModelMetadata(BaseModel):
    feedback: Union[ErrorModelFeedback, SuccessModelFeedback, DefaultModelFeedback]
    tenant_id: str
    machine_id: str
    task_id: str


class ModelStateValue(Enum):
    ACKNOWLEDGE = "acknowledge"
    ACTIVE = "active"
    OLD = "old"
    TRAINING = "training"
    ERROR = "error"


class ModelState(BaseModel):
    value: ModelStateValue
    creation_date: str
    publishment_date: str
    deprecation_date: str


class ModelRegistry(BaseModel):
    metadata: ModelMetadata
    file_path: str
    state: ModelState
