from typing import Dict, List

from txp.common.ml.models import ModelStateValue, ModelRegistry
from txp.common.utils.firestore_utils import ProjectModel, get_authenticated_client, get_current_project_model
from txp.ml.training_service.common import TrainCommand
from txp.web.core_components.main_view import MainView
from txp.web.core_components.app_profiles import AppProfile
import txp.common.utils.model_registry_utils as models_utils
from fastapi import status
import streamlit as st
import requests
import logging
from txp.common.config import settings
from google.cloud import firestore

log = logging.getLogger(__name__)
log.setLevel(settings.txp.general_log_level)


class TrainingView(MainView):
    """This view is used for training models based on datasets available
    in the data warehouse."""

    def __init__(self):
        super(TrainingView, self).__init__(component_key="training_view")
        self._asset_selectbox_val: str = ""
        self._asset_selectbox_key: str = "asset_sb"
        self._task_selectbox_val: str = ""
        self._task_selectbox_key: str = "task_sb"
        self._dataset_name_val: str = ""
        self._dataset_name_key: str = "dataset_name_key"
        self._versions_val: List[str] = []
        self._versions_key: str = "versions_form_key"
        self._project_configuration_data: ProjectModel = None
        self._model_registry_col: str = "txp_models_registry"
        self._pulled_model: ModelRegistry = None

    def get_associated_profile(self) -> AppProfile:
        return AppProfile.ANALYTICS

    @classmethod
    def get_display_name(cls) -> str:
        return "Entrenar Task"

    def _build_submenu_state(self) -> Dict:
        return {}

    def _build_content_state(self) -> Dict:
        return {}

    def _get_project_configuration(self):
        db = get_authenticated_client(
            self.app_state.authentication_info.role_service_account_credentials
        )
        self._project_configuration_data = get_current_project_model(
            db, self._tenant_id
        )
        self._current_gateway = list(
            self._project_configuration_data.gateways_table.keys()
        )[0]

    def _register_asset_value(self):
        self._asset_selectbox_val = st.session_state[self._asset_selectbox_key]

    def _register_dataset_name_value(self):
        self._dataset_name_val = st.session_state[self._dataset_name_key]

    def _register_dataset_versions_values(self):
        self._versions_val = (
            st.session_state[self._versions_key].replace(" ", "").split(",")
        )

    def _register_task_value(self):
        self._task_selectbox_val = st.session_state[self._task_selectbox_key]

    def _validate_training_allowed(
        self, dataset_name: str, dataset_versions: List[str]
    ) -> bool:
        firestore_db: firestore.Client = get_authenticated_client(
            self.app_state.authentication_info.role_service_account_credentials
        )
        model_registry_name = models_utils.get_gcs_dataset_prefix(
            dataset_name, dataset_versions
        )
        model = models_utils.get_ml_model(
            firestore_db,
            self._tenant_id,
            self._asset_selectbox_val,
            self._task_selectbox_val,
            model_registry_name,
            self._model_registry_col,
        )
        firestore_db.close()
        if not model:
            return True

        if model.state.value.value == ModelStateValue.TRAINING.value:
            return False

        else:
            return True

    def _train_model(self, train_payload: TrainCommand):
        headers = {"Authorization": f"Bearer {st.secrets['service_auth_token']}"}
        response = requests.post(
            f"{st.secrets.service_url}/training/train", json=train_payload.dict(),
            headers=headers
        )
        if response.status_code == status.HTTP_200_OK:
            st.success("Su modelo se ha empezado a entrenar correctamente")

        elif response.status_code == status.HTTP_404_NOT_FOUND:
            st.warning(f"Error al lanzar entrenamiento: {response.json()['Error']}")
        else:
            st.warning(f"Error desconocido al lanzar entrenamiento: ")
            st.json(response.json())

    def _publish_model(self, publish_payload: TrainCommand):
        headers = {"Authorization": f"Bearer {st.secrets['service_auth_token']}"}
        response = requests.post(
            f"{st.secrets.service_url}/training/publish", json=publish_payload.dict(),
            headers=headers
        )
        if response.status_code == status.HTTP_200_OK:
            st.success("Su modelo ha sido promovido correctamente al servicio de predicción")
            self._pulled_model = None  # Clear the memory from memory

        elif response.status_code == status.HTTP_404_NOT_FOUND:
            st.warning("Su modelo no existe o ya esta publicado en el servicio de predicción")
            st.text("Si el problema persiste, contacte a soporte.")

    def _render_content(self) -> None:
        if not self._project_configuration_data:
            self._get_project_configuration()

        st.markdown("Entrenar Task para un Activo")
        logging.info(f"Rendering selected active: {self._asset_selectbox_val}")
        logging.info(f"Rendering selected task: {self._task_selectbox_val}")

        self._asset_selectbox_val = st.selectbox(
            label="Seleccione Activo",
            options=list(self._project_configuration_data.machines_table.keys()),
            key=self._asset_selectbox_key,
            on_change=self._register_asset_value,
            index=0,
        )

        self._task_selectbox_val = st.selectbox(
            label="Seleccione Task",
            options=list(
                self._project_configuration_data.tasks_by_asset[
                    self._asset_selectbox_val
                ].keys()
            ),
            on_change=self._register_task_value,
            key=self._task_selectbox_key,
            index=0,
        )

        with st.form(key="dataset_info_form"):
            dataset_name = st.text_input(
                label="Ingrese el nombre del dataset",
                help="El nombre del dataset acordado por el equipo de anotación",
                key=self._dataset_name_key,
            )

            dataset_versions = st.text_input(
                label="Ingrese las versiones separadas por coma", key=self._versions_key
            )

            st.form_submit_button("Entrenar", on_click=self._start_train)

            st.form_submit_button(
                "Ver resultado",
                on_click=self._check_train_result,
            )

        if self._pulled_model:
            st.markdown("**Resumen del modelo:**")
            st.markdown(f"Tenant: {self._pulled_model.metadata.tenant_id}")
            st.markdown(f"Task: {self._pulled_model.metadata.task_id}")
            st.markdown(f"Asset: {self._pulled_model.metadata.machine_id}")
            st.markdown(f"Estado del modelo:")
            st.json(self._pulled_model.state.json())
            st.markdown(f"Feedback del modelo:")
            st.json(self._pulled_model.metadata.feedback.json())

            if self._pulled_model.state.value == ModelStateValue.ACKNOWLEDGE:
                st.info(
                    "El modelo ha terminado de entrenar, y puede ser promovido a predicción"
                )
                st.button("Promover", on_click=self._approve_ack_model)

    def _start_train(self):
        st.info("Starting training process...")
        self._register_asset_value()
        self._register_task_value()
        self._register_dataset_versions_values()
        self._register_dataset_name_value()

        training_allowed = self._validate_training_allowed(
            self._dataset_name_val, self._versions_val
        )
        if not training_allowed:
            st.warning(
                "Actualmente su Task se encuentra entrenando. "
                "Espere a que el task termine de entrenar"
            )
        else:
            train_payload = TrainCommand(
                dataset_name=self._dataset_name_val,
                dataset_versions=self._versions_val,
                tenant_id=self._tenant_id,
                machine_id=self._asset_selectbox_val,
                task_id=self._task_selectbox_val,
            )
            self._train_model(train_payload)
            self._pulled_model = None

    def _check_train_result(self):
        self._register_asset_value()
        self._register_task_value()
        self._register_dataset_versions_values()
        self._register_dataset_name_value()
        firestore_db: firestore.Client = get_authenticated_client(
            self.app_state.authentication_info.role_service_account_credentials
        )
        model_reg_name = models_utils.get_gcs_dataset_prefix(
            self._dataset_name_val, self._versions_val
        )
        logging.info(
            "Requesting model from models registry for: \n"
            f"Tenant: {self._tenant_id} \n"
            f"Asset: {self._asset_selectbox_val} \n"
            f"Task: {self._task_selectbox_val} \n"
            f"Model Registry: {model_reg_name}"
        )
        model = models_utils.get_ml_model(
            firestore_db,
            self._tenant_id,
            self._asset_selectbox_val,
            self._task_selectbox_val,
            model_reg_name,
            self._model_registry_col,
        )
        if model is None:
            st.error(
                "No se pudo encontrar registros para el modelo. Si el problema persiste, "
                "contacte a soporte"
            )
            self._pulled_model = None
            return

        else:
            self._pulled_model = model

    def _approve_ack_model(self):
        train_payload = TrainCommand(
            dataset_name=self._dataset_name_val,
            dataset_versions=self._versions_val,
            tenant_id=self._tenant_id,
            machine_id=self._asset_selectbox_val,
            task_id=self._task_selectbox_val,
        )
        self._publish_model(train_payload)

    def _render_submenu(self) -> None:
        if not self._project_configuration_data:
            self._get_project_configuration()
