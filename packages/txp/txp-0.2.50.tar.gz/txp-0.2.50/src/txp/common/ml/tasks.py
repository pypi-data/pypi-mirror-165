"""
This module defines the classes that supports the common structure
for ML Tasks of assets.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Union, Optional
from enum import Enum


class TaskEventTaxonomyEnum(Enum):
    """An event produced by a task, can be classified within this
    taxonomy.

    For example, for a ML task that recognizes the normal operation
    of a machine, the prediction output could be 'NormalOperation'.
    This output could be categorized as `Harmless`.
    """
    Detrimental = 'Detrimental'
    Harmless = 'Harmless'
    Neutral = 'Neutral'


class ClassificationLabelDefinition(BaseModel):
    labels: List[str]
    label_to_int: Dict[str, int]
    int_to_label: Dict[int, str]
    label_to_taxonomy: Dict[str, TaskEventTaxonomyEnum]


class AssetTask(BaseModel):
    """
    Args:
        label_def: The definition for the event labels of the task.

        task_id: A unique task_id under a given tenant asset.

        asset_id: The asset_id to which this task is associated.

        task_data: A string path in storage for the task model data.

        edges: The list of edges logical ids that feed this tasks as
            signal inputs.

        schema_: A Dictionary of Edges to expected Perception name and
            table name.

    A example of a schema would be:

    """
    label_def: ClassificationLabelDefinition
    task_type: str
    task_id: str
    asset_id: str = Field(alias='machine_id')
    task_data: Optional[str]
    edges: List[str]
    schema_: Dict[str, Dict[str, Dict[str, Union[bool, List]]]] = Field(alias='schema')
    parameters: dict

    class Config:
        # https://github.com/samuelcolvin/pydantic/issues/602#issuecomment-503189368
        allow_population_by_field_name = True


class AssetStateCondition(Enum):
    OPTIMAL = "OPTIMAL"
    OPERATIONAL = "OPERATIONAL"
    UNDEFINED = "UNDEFINED"
    CRITICAL = "CRITICAL"
    GOOD = "GOOD"


class AssetState(BaseModel):
    events: List[str]
    asset_id: str
    condition: AssetStateCondition
    observation_timestamp: int
    tenant_id: str
    partition_timestamp: str

