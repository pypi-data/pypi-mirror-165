import io
from typing import Tuple, List, Dict, Set
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from segments import SegmentsClient, SegmentsDataset
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from txp.ml.common.tasks.policy import Policy
from txp.ml.common.tasks.slic_cv_tasks.slic_patch_image_helpers import SlicPatchImageProcessor
from txp.ml.common.tasks.task import Encoder, Task
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class SlicPatchRecognitionEncoder(Encoder):
    """Encoder definition for all the task implementations
    that uses the SlicPatch object recognition algorithm.
    """
    def __init__(
        self,
        number_of_segments: int,
        image_shape: Tuple,
        thermal_image_shape: Tuple,
        patch_x_y_image: Tuple,
        patch_x_y_thermal: Tuple,
        pandas_cols: List[str],
        schema: Dict
    ):
        super(SlicPatchRecognitionEncoder, self).__init__(schema)
        self._number_of_segments: int = number_of_segments
        self._image_shape: Tuple = image_shape
        self._thermal_image_shape: Tuple = thermal_image_shape
        self._patch_x_y_image: Tuple = patch_x_y_image
        self._patch_x_y_thermal: Tuple = patch_x_y_thermal
        self._slic_processor: SlicPatchImageProcessor = SlicPatchImageProcessor(
            self._number_of_segments
        )
        self._pandas_cols: List[str] = pandas_cols

    def build_training_dataset(self, tables, target, **kwargs) -> pd.DataFrame:
        """Builds the training dataset for the task.

        Args
          **kwargs:
            'segments_api_key' (str): The key to connect to segments API to download
                computer vision panoptic datasets
            'segments_dataset_id' (str): The dataset ID in segments hub.
            'segments_dataset_release' (str): The version release value for the
                dataset.
            'instance_ids' (List[int]): The list of instances ID's labels to
                recognize.
            'spot_id' (str): The spot name that helps to identify which images
                in the dataset correspond to the position to be trained.
            'image_type': The image type to process: 'image' or 'thermographic'
            'true_categories' (List[int]): The categories IDs present in an labeled image that
                indicates the presence of the object.
            'dataset' (pd.DataFrame): a training pandas DataFrame. If provided, the
                nothing will be downloaded from Segments.ai server.
        """
        if 'dataset' not in kwargs:
            segs_client = self._get_segments_client(
                kwargs['segments_api_key']
            )

            segments_ds = self._get_segments_dataset(
                kwargs['segments_dataset_id'],
                kwargs['segments_dataset_release'],
                segs_client
            )

            instance_ids = set(kwargs['instance_ids'])
            spot_id = kwargs['spot_id']
            image_type = kwargs['image_type']
            true_categories = kwargs['true_categories']

            df: pd.DataFrame = self._map_segments_to_pandas(
                segments_ds, segs_client, image_type, instance_ids, spot_id, true_categories
            )

        else:
            df = kwargs['dataset']

        self.dataset = df
        self.target = 'label'

        return df

    def transform_input(self, signals_completed: dict) -> pd.DataFrame:
        vector = []

        for key_edge_logical_id, value_perceptions in self.schema.items():
            for key_percept, sch_values in value_perceptions.items():
                for table_id in sch_values:
                    if table_id:
                        image = [
                            int(x) for x in
                            signals_completed[key_edge_logical_id][key_percept][table_id][0]["data"][0]
                        ]
                        img_np_array = self._get_image_array(image)
                        log.info(f"{self.__class__.__name__} Prediction "
                                 f"with image shape: {img_np_array.shape}")
                        print(f"{self.__class__.__name__} Prediction "
                                 f"with image shape: {img_np_array.shape}")
                        vector = self._get_slic_vector(img_np_array, key_percept, vector)

        dataset = pd.DataFrame()
        dataset = dataset.append([vector], ignore_index=True)
        return dataset

    def _map_segments_to_pandas(
        self,
        segments_ds: SegmentsDataset,
        segments_client: SegmentsClient,
        image_type: str,
        instances_ids: Set[str],
        spot_id: str,
        true_categories: Tuple
    ) -> pd.DataFrame:
        """This method allows to parse a Segments.ai dataset into a Pandas
        Dataframe that can be consumed by the Task object model.

        Note: For our first usage of Segments.ai, we labelled all the images on the same
            Dataset. In consequence, we needed to add descriptive information at labeling time
            that allowed us to know which spot and instance IDs was being processed.

        TODO: we should revisit that conceptual labeling values, and this code, If we decide
            to move forward using Segments.ai

        Args:
            segments_ds: The segments dataset object.
                https://docs.segments.ai/reference/python-sdk#datasets

            segments_client: A SegmentsClient completely authenticated.
                https://docs.segments.ai/reference/python-sdk#setup

            image_type (str): The image type to process. { 'image', 'thermographic' }

            instances_ids (List[str]): The list of instances ids to recognize.

            spot_id(str): The value of the spot ID to train.

            true_categories: The categories IDs present in an labeled image that
                indicates the presence of the object.
        """
        df_dicts = []
        normal_res = (self._image_shape[0], self._image_shape[1])
        thermographic_res = (self._thermal_image_shape[0], self._thermal_image_shape[1])
        patch_to_use = self._patch_x_y_image if image_type == 'image' else self._patch_x_y_thermal
        for sample in segments_ds:
            if image_type == 'image':
                if sample['image'].size != normal_res:
                    continue

            else:
                if sample['image'].size != thermographic_res:
                    continue

            label = segments_client.get_label(sample['uuid'])

            image_attributes = label['attributes']['image_attributes']

            if image_attributes.get('spot_id', None) != spot_id:
                continue

            sample_cats = (set(map(
                lambda ann: ann['category_id'],
                label['attributes']['annotations']
            )))

            has_category = not sample_cats.isdisjoint(true_categories)

            # compute beer instance
            beer_instance = None
            for ann in label['attributes']['annotations']:
                if ann.get('attributes', None) is not None:
                    if ann['attributes'].get('instance_id', None) in instances_ids:
                        beer_instance = ann['id']
                        has_category = True
                        break
                    else:
                        beer_instance = -1
                        has_category = False

            bitmap_label = np.asarray(sample['segmentation_bitmap'].convert('L'))
            if beer_instance and beer_instance > 0:
                x, y, w, h = self._get_patch_coordinates_to_sample(bitmap_label, beer_instance)
            else:
                x, y, w, h = 0, 0, 0, 0

            df_dicts.append(
                {
                    self._pandas_cols[0]: self._slic_processor.process_image_patches(
                        np.asarray(sample['image']),
                        patch_to_use[0],
                        patch_to_use[1]
                    ),
                    self._pandas_cols[1]: np.asarray(sample['segmentation_bitmap'].convert('L')),
                    self._pandas_cols[2]: (w, h),
                    self._pandas_cols[3]: beer_instance,
                    self._pandas_cols[4]: int(has_category)
                }
            )

            df = pd.DataFrame(df_dicts, columns=self._pandas_cols)

        return df

    def _get_slic_vector(self, img_array: np.ndarray, key_percept: str, carry_array: List) -> List[float]:
        """
            TODO: Why are we using `extend` ? Ask.
        """
        if key_percept == "Image":
            if len(carry_array) > 0:
                carry_array.extend(self._slic_processor.process_image_patches(
                    img_array,
                    self._patch_x_y_image[0],
                    self._patch_x_y_image[1]
                ))
            else:
                carry_array = self._slic_processor.process_image_patches(
                    img_array,
                    self._patch_x_y_image[0],
                    self._patch_x_y_image[1]
                )
        elif key_percept == "ThermalImage":
            if len(carry_array) > 0:
                carry_array.extend(
                    self._slic_processor.process_image_patches(
                        img_array,
                        self._patch_x_y_image[0],
                        self._patch_x_y_image[1]
                    )
                )
            else:
                carry_array = self._slic_processor.process_image_patches(
                    img_array,
                    self._patch_x_y_image[0],
                    self._patch_x_y_image[1]
                )

        return carry_array

    @staticmethod
    def _get_image_array(image_data: List) -> np.ndarray:
        image = np.frombuffer(bytes(image_data), dtype=np.uint8)
        image_b = bytes(image)
        image_pil = Image.open(io.BytesIO(image_b))
        img_np_array = np.array(image_pil)
        return img_np_array

    # ======================== build_training_dataset section =======================
    @staticmethod
    def _get_segments_client(api_key) -> SegmentsClient:
        client = SegmentsClient(api_key)
        return client

    @staticmethod
    def _get_segments_dataset(dataset_id, dataset_release, client) -> SegmentsDataset:
        release = client.get_release(dataset_id, dataset_release)
        dataset = SegmentsDataset(release, filter_by=["reviewed"])  # Always filter reviewed images
        return dataset

    @staticmethod
    def _get_instance_bitmap_mask(semantic_label_bitmap, instance_id: id) -> np.ndarray:
        """Receives a labeled semantic image bitmap, and mask all the pixels
        that don't belong to the instance_id"""
        mask = np.copy(semantic_label_bitmap)

        mask[mask != instance_id] = 0
        mask[mask == instance_id] = 255

        return mask

    @staticmethod
    def _get_patch_coordinates_to_sample(semantic_label_bitmap, instance_id, error=10) -> Tuple:
        """given a semantic_label image, obtains the rectangle coordinates to patch on
        based on the labels"""
        bitmap_interest_mask = SlicPatchRecognitionEncoder._get_instance_bitmap_mask(
            semantic_label_bitmap, instance_id
        )
        x, y, w, h = cv2.boundingRect(bitmap_interest_mask)
        return x, y, w, h


class SlicPatchRecognitionDecisionTreePolicy(Policy):
    def __init__(self, policy_file: str = None):
        super().__init__(policy_file)
        if self.clf is None:
            self.clf = DecisionTreeClassifier()

    def name(self):
        return self.__class__.name()

    def train(
            self,
            dataset: pd.DataFrame,
            target: str = 'label',
            test_size: float = 0.3,
    ):
        """
        Args:
            dataset: the training dataset MUST have the columns:
                `image`: The features vector of the sample.
                `target`: The label value for the sample (1 or 0)

            target (str): The column name for the targets
            test_size ( float ): The percentage of test data to perform the dataframe split
        """
        x = dataset['image'].values.tolist()
        y = dataset[target].values.tolist()
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=0)

        self.clf = self.clf.fit(x_train, y_train)
        y_prediction = self.clf.predict(x_test)

        self.accuracy = metrics.accuracy_score(y_test, y_prediction)
        self.trained = True

    def predict(self, tensor):
        if self.is_trained():
            return self.clf.predict(tensor)
        else:
            return None


class SlicPatchRecognitionTask(Task):
    """General definition for all the task implementations
    that uses the SlicPatch object recognition algorithm.
    """
    def __init__(
        self,
        task_definition=None,
        credentials_str=None,
    ):
        super().__init__(
            self._build_encoder(task_definition.schema_, task_definition.parameters),
            self._build_policy(),
            task_definition,
            credentials_str
        )

        if self.task_definition.task_data and credentials_str is not None:
            self.load_from_bucket(self.task_definition.task_data)

            if task_definition.schema_:
                self.encoder.set_schema(task_definition.schema_)

        self.ready = True

        log.info(f"{self.__class__.__name__} instance is ready with file: {self.task_definition.task_data}")
        print(f"{self.__class__.__name__} instance is ready with file: {self.task_definition.task_data}")

    def _build_encoder(
        self, schema: Dict, parameters: Dict
    ) -> SlicPatchRecognitionEncoder:
        """Return a new instance reference to a SlicPatchRecognitionEncoder."""
        return SlicPatchRecognitionEncoder(
            parameters['number_of_segments'],
            parameters['image_shape'],
            parameters['thermal_image_shape'],
            parameters['patch_x_y_image'],
            parameters['patch_x_y_thermal'],
            parameters['pandas_cols'],
            schema
        )

    def _build_policy(self) -> Policy:
        """Returns the instance reference to the appropriated Policy type."""
        return SlicPatchRecognitionDecisionTreePolicy()

    def predict(self, sampling_window_rows) -> str:
        """Returns the prediction results for the given sampling windows
        generated input vectors.

        Args:
            sampling_window_rows: filled Firestore dictionary, this dict
                contains all the rows present in bigquery tables.

        Returns:
            Appropriate enumerated label.
        """
        print(f"{self.__class__.__name__} prediction request.")
        prediction_dataset = self.encoder.transform_input(sampling_window_rows)
        return self.task_definition.label_def.int_to_label[
            self.policy.predict(prediction_dataset)[0]
        ]

    def train(self, dataset: pd.DataFrame) -> None:
        self.policy.train(dataset, self.encoder.target)
