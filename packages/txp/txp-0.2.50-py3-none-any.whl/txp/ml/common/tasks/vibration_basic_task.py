import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.model_selection import train_test_split
import xgboost as xgb
from txp.ml.common.tasks.policy import Policy
from txp.ml.common.tasks.task import Task, Encoder
import pandas as pd


class VibrationBasicTask(Task):

    def __init__(self, task_definition=None, credentials_str=None, decision_tree_policy=False):

        schema = None
        task_file = None
        if task_definition is not None:
            schema = task_definition.schema_
            task_file = task_definition.task_data

        policy = VibrationDecisionTreePolicy()
        if not decision_tree_policy:
            parameters = None
            if task_definition is not None:
                parameters = task_definition.parameters
            policy = VibrationGradientBoostPolicy(parameters)

        super().__init__(VibrationEncoder(schema), policy, task_definition, credentials_str)

        if task_file is not None and credentials_str is not None:
            self.load_from_bucket(task_file)

            if schema is not None:
                self.encoder.set_schema(schema)

        self.ready = True
        print("VibrationBasicTask is ready.")

    def predict(self, sampling_window_rows) -> str:
        """
            Args:
                sampling_window_rows: filled firestore dictionary, this dict contains all the rows present
                                   in bigquery tables.
            Returns:
                Predicted VibrationBasicEvent.
        """
        print(f"VibrationBasicTask prediction request.")
        prediction_dataset = self.encoder.transform_input(sampling_window_rows)
        return self.task_definition.label_def.int_to_label[int(self.policy.predict(prediction_dataset)[0])]

    def train(self, dataset):
        self.policy.train(dataset, self.encoder.target)


class VibrationEncoder(Encoder):

    def __init__(self, schema):
        super().__init__(schema)

    def transform_input(self, signals_completed) -> pd.DataFrame:
        dataframe_row = {}
        for edge_logical_id in signals_completed:
            for perception_name in signals_completed[edge_logical_id]:
                for table_id in signals_completed[edge_logical_id][perception_name]:
                    rows = signals_completed[edge_logical_id][perception_name][table_id]
                    if table_id in ["time_metrics", "fft_metrics", "psd_metrics"]:
                        for row in rows:
                            for metric in self.schema[edge_logical_id][perception_name][table_id]:
                                dataframe_row[
                                    f'{metric}_{table_id}_{perception_name}_{edge_logical_id}_{row["dimension"]}'] \
                                    = row[metric]
                    else:
                        row = rows[0]
                        if table_id == "fft":
                            row["fft"] = [[np.complex128(complex(z["real"], z["imag"]))
                                           for z in dimension["values"]] for dimension in row["fft"]]
                        else:
                            row["psd"] = [dimension["psd"] for dimension in row["data"]]
                        for dimension in range(len(row[table_id])):
                            for i in range(len(row[table_id][dimension])):
                                dataframe_row[f"{table_id}_{perception_name}_{edge_logical_id}_{dimension}_{i}"] = \
                                    row[table_id][dimension][i].real

        dataset = pd.DataFrame()
        dataset = dataset.append(dataframe_row, ignore_index=True)
        columns = list(self.dataset.columns)
        columns.remove(self.target)

        return dataset[columns]

    def build_training_dataset(self, tables, target):
        self.target = target
        groups_time_df = tables['time_df'].groupby("observation_timestamp")
        groups_fft_df = tables['fft_df'].groupby(["observation_timestamp", "edge_logical_id", "perception_name"])
        groups_psd_df = tables['psd_df'].groupby(["observation_timestamp", "edge_logical_id", "perception_name"])
        groups_time_metrics_df = tables['time_metrics_df'].groupby(
            ["observation_timestamp", "edge_logical_id", "perception_name"])
        groups_fft_metrics_df = tables['fft_metrics_df'].groupby(["observation_timestamp", "edge_logical_id",
                                                                  "perception_name"])
        groups_psd_metrics_df = tables['psd_metrics_df'].groupby(["observation_timestamp", "edge_logical_id",
                                                                  "perception_name"])
        dataset = pd.DataFrame()

        for observation_timestamp, group_time_df in groups_time_df:
            row = self.__get_row(groups_time_metrics_df, groups_psd_metrics_df, groups_fft_metrics_df,
                                 observation_timestamp, groups_fft_df, groups_psd_df)
            if row:
                row[target] = group_time_df.iloc[0][target]
                dataset = dataset.append(row, ignore_index=True)

        self.dataset = dataset.replace(np.nan, 0)

        return self.dataset

    @staticmethod
    def __get_metrics(observation_timestamp, perception, group_dataframe, name, df_metrics, edge_logical_id):

        if (observation_timestamp, edge_logical_id, perception) not in group_dataframe.groups:
            return {}
        window_df = group_dataframe.get_group((observation_timestamp, edge_logical_id, perception))
        if len(window_df) < 3:
            return {}
        res = {}
        for _, signal in window_df.iterrows():
            for metric in df_metrics:
                res[f'{metric}_{name}_{perception}_{edge_logical_id}_{signal["dimension"]}'] = signal[metric]
        return res

    @staticmethod
    def __get_vector_magnitude(observation_timestamp, perception, group_dataframe, name, edge_logical_id):
        if (observation_timestamp, edge_logical_id, perception) not in group_dataframe.groups:
            return {}
        window_df = group_dataframe.get_group((observation_timestamp, edge_logical_id, perception))
        if len(window_df) != 1:
            return {}
        res = {}
        signal = window_df.iloc[0]
        for dimension in range(len(signal[name])):
            for i in range(len(signal[name][dimension])):
                res[f"{name}_{perception}_{edge_logical_id}_{dimension}_{i}"] = signal[name][dimension][i].real
        return res

    def __get_row(self, groups_time_metrics_df, groups_psd_metrics_df, groups_fft_metrics_df, observation_timestamp,
                  groups_fft_df, groups_psd_df):
        row = {}
        for edge_logical_id in self.schema:
            for perception in self.schema[edge_logical_id]:

                if "time_metrics" in self.schema[edge_logical_id][perception]:
                    row_metrics = self.__get_metrics(observation_timestamp, perception, groups_time_metrics_df,
                                                     "time_metrics",
                                                     self.schema[edge_logical_id][perception]["time_metrics"],
                                                     edge_logical_id)
                    if not row_metrics:
                        return {}
                    row = {**row, **row_metrics}

                if "psd_metrics" in self.schema[edge_logical_id][perception]:
                    row_metrics = self.__get_metrics(observation_timestamp, perception, groups_psd_metrics_df,
                                                     "psd_metrics",
                                                     self.schema[edge_logical_id][perception]["psd_metrics"],
                                                     edge_logical_id)
                    if not row_metrics:
                        return {}
                    row = {**row, **row_metrics}

                if "fft_metrics" in self.schema[edge_logical_id][perception]:
                    row_metrics = self.__get_metrics(observation_timestamp, perception, groups_fft_metrics_df,
                                                     "fft_metrics",
                                                     self.schema[edge_logical_id][perception]["fft_metrics"],
                                                     edge_logical_id)
                    if not row_metrics:
                        return {}
                    row = {**row, **row_metrics}

                if "fft" in self.schema[edge_logical_id][perception] and \
                        self.schema[edge_logical_id][perception]["fft"]:
                    vector_magnitude = self.__get_vector_magnitude(observation_timestamp, perception, groups_fft_df,
                                                                   "fft", edge_logical_id)
                    if not vector_magnitude:
                        return {}
                    row = {**row, **vector_magnitude}

                if "psd" in self.schema[edge_logical_id][perception] and \
                        self.schema[edge_logical_id][perception]["psd"]:
                    vector_magnitude = self.__get_vector_magnitude(observation_timestamp, perception, groups_psd_df,
                                                                   "psd", edge_logical_id)
                    if not vector_magnitude:
                        return {}
                    row = {**row, **vector_magnitude}

        return row


class VibrationDecisionTreePolicy(Policy):

    def __init__(self, policy_file: str = None):
        super().__init__(policy_file)
        if self.clf is None:
            self.clf = DecisionTreeClassifier()

    def name(self):
        return "VibrationDecisionTreePolicy"

    def train(self, dataset, target, test_size=0.3):
        features_col = list(dataset.columns)
        features_col.remove(target)
        x = dataset[features_col]
        y = dataset[target]
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


class VibrationGradientBoostPolicy(Policy):

    def __init__(self, parameters=None):
        if parameters is None:
            self.param = {
                'max_depth': 1000,
                'eta': 1,
                'objective': 'multi:softmax',
                'num_class': 4,
                'num_round': 10
            }
        else:
            self.param = parameters
        super().__init__()

    def name(self):
        return "VibrationGradientBoostPolicy"

    def train(self, dataset, target, test_size=0.3):
        features_col = list(dataset.columns)
        features_col.remove(target)
        x = dataset[features_col]
        y = dataset[target]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=0)

        train_matrix = xgb.DMatrix(x_train.values, y_train.values)
        test_matrix = xgb.DMatrix(x_test.values)

        params = self.param.copy()
        params.pop("num_round", None)

        self.clf = xgb.train(params, train_matrix, self.param["num_round"])
        y_prediction = self.clf.predict(test_matrix)

        self.accuracy = metrics.accuracy_score(y_test, y_prediction)
        self.trained = True

    def predict(self, tensor):
        if self.is_trained():
            matrix_to_predict = xgb.DMatrix(tensor.values)
            return self.clf.predict(matrix_to_predict)
        else:
            return None
