from txp.ml.common.tasks.vibration_basic_task import *
from txp.ml.common.tasks.slic_cv_tasks.slic_patch_recognition_classifier import SlicPatchRecognitionTask
from txp.ml.training_service.model_trainers.vibration_model_trainer import (
    RayVibrationModelTrainer,
)
from txp.ml.training_service.model_trainers.computer_vision_trainer import (
    RayComputerVisionSlicClassificationTrainer,
)
import logging
import json
from google.oauth2 import service_account
import google.cloud.firestore as firestore
from txp.common.ml.tasks import AssetTask


class TrainerFactory:
    # TODO: We should ensure that all the values in DB are coherent
    #   with the class names only. This will give us safety.
    _VIBRATION_MODELS = [
        VibrationBasicTask.__class__.__name__,
        "VibrationBasicGradientBoostTask",
        "VibrationBasicDecisionTreeTask",
    ]

    # TODO: We should ensure that all the values in DB are coherent
    #   with the class names only. This will give us safety.
    _COMPUTER_VISION_SLIC_MODELS = [
        SlicPatchRecognitionTask.__class__.__name__,
        'SlicPatchRecognitionTask'
    ]

    def __init__(self, credentials_str, models_bucket_name, data_warehouse_bucket_name, prediction_service_topic,
                 models_registry_collection_name, log_level=logging.INFO):

        logging.basicConfig(level=log_level)
        self._log_level = log_level

        self.models_bucket_name = models_bucket_name
        self.data_warehouse_bucket_name = data_warehouse_bucket_name
        self.prediction_service_topic = prediction_service_topic
        self.models_registry_collection_name = models_registry_collection_name
        self._credentials_str = credentials_str

        json_dict_service_account = json.loads(credentials_str, strict=False)
        credentials = service_account.Credentials.from_service_account_info(
            json_dict_service_account
        )
        self._credentials_str = credentials_str
        self._firestore_db = firestore.Client(
            credentials=credentials, project=credentials.project_id
        )

    def get_task_and_trainer(self, task_definition: AssetTask):
        logging.info(f"{self.__class__.__name__} finding task for {task_definition.dict()}.")
        task_type = task_definition.task_type
        if task_type in self._VIBRATION_MODELS:
            showroom_task = VibrationBasicTask(task_definition=task_definition, decision_tree_policy=False)
            vibration_trainer = RayVibrationModelTrainer.remote(
                self._credentials_str,
                self.models_bucket_name,
                self.data_warehouse_bucket_name,
                self.prediction_service_topic,
                self.models_registry_collection_name,
                self._log_level,
            )
            return showroom_task, vibration_trainer

        elif task_type in self._COMPUTER_VISION_SLIC_MODELS:
            logging.info(
                f"{self.__class__.__name__} received train request for " f"{task_type}."
            )
            slic_task = SlicPatchRecognitionTask(task_definition)
            trainer = RayComputerVisionSlicClassificationTrainer.remote(
                self._credentials_str,
                self.models_bucket_name,
                self.data_warehouse_bucket_name,
                self.prediction_service_topic,
                self.models_registry_collection_name,
                self._log_level,
            )

            return slic_task, trainer

        else:
            logging.error(f"Could not match any task for task_type: {task_type}")
            return None, None
