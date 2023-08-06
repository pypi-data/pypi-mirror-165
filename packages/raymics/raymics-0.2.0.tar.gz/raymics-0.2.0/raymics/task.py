import os
import joblib

from radiomics.featureextractor import RadiomicsFeatureExtractor
from raymics.extract_radiomics_features import RadiomicsUtility, DatasetType

PKL_RADIOMICS_UTILITY_NAME = "extractor.pkl"
PKL_TASK_INFO_NAME = "task_info.pkl"
PKL_FE_NAME = "fe.pkl"
PKL_DATASET_NAME = "dataset.pkl"
PKL_MODEL_NAME = "model.pkl"
RADIOMICS_CONFIG_NAME = "radiomics.yaml"
REPORT_NB_NAME = "report.ipynb"
REPORT_HTML_NAME = "report.html"


class Task:

    def __init__(self, task_dir: str):
        self.task_dir = task_dir
        if not os.path.exists(self.task_dir):
            os.makedirs(self.task_dir)

        if not os.path.exists(self._task_info_path()):
            self.task_info = dict()
        else:
            self.task_info = joblib.load(self._task_info_path())

    def set_params(self, params: dict):
        assert "params" not in self.task_info
        self.task_info["params"] = params
        self._dump_task_info()

    def _task_info_path(self):
        return os.path.join(self.task_dir, PKL_TASK_INFO_NAME)

    def _dump_task_info(self):
        joblib.dump(self.task_info, self._task_info_path())

    @property
    def data_type(self):
        csv_paths = []
        for name in os.listdir(self.train_processed_feature_dataset_dir):
            if name.startswith(".") or not name.endswith(".csv"):
                continue
            path = os.path.join(self.train_processed_feature_dataset_dir, name)
            if os.path.isdir(path):
                continue
            csv_paths.append(path)

        assert len(csv_paths) > 0

        if os.path.exists(os.path.join(self.train_processed_feature_dataset_dir,
                                       "features.csv")):
            return DatasetType.NON_TS
        else:
            return DatasetType.TS

    @property
    def task_type(self):
        return self.task_info["params"]["experiment__task_type"]

    @property
    def task_name(self):
        return self.task_info["params"]["experiment__name"]

    @property
    def algorithm(self):
        return self.task_info["params"]["experiment__algorithm"]

    @staticmethod
    def _mkdir(dir_path: str) -> str:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path

    @property
    def report_dir(self):
        return self._mkdir(os.path.join(self.task_dir, "report"))

    @property
    def report_nb_path(self):
        return os.path.join(self.task_dir, "report", REPORT_NB_NAME)

    @property
    def report_html_path(self):
        return os.path.join(self.task_dir, "report", REPORT_HTML_NAME)

    @property
    def pickle_dir(self):
        dir_path = os.path.join(self.task_dir, "pickle")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return dir_path

    def pickle_data(self, key: str, data):
        path = os.path.join(self.pickle_dir, key)
        joblib.dump(data, path)

    def unpickle_data(self, key: str):
        path = os.path.join(self.pickle_dir, key)
        return joblib.load(path)

    @property
    def dataset_dir(self):
        return self._mkdir(os.path.join(self.task_dir, "dataset"))

    @property
    def train_dir(self):
        return self._mkdir(os.path.join(self.dataset_dir, "train"))

    @property
    def test_dir(self):
        return self._mkdir(os.path.join(self.dataset_dir, "test"))

    @property
    def train_feature_dataset_dir(self):
        return self._mkdir(os.path.join(self.train_dir, "feature_data"))

    @property
    def test_feature_dataset_dir(self):
        return self._mkdir(os.path.join(self.test_dir, "feature_data"))

    @property
    def train_processed_feature_dataset_dir(self):
        return self._mkdir(os.path.join(self.train_dir, "processed_feature_data"))

    @property
    def test_processed_feature_dataset_dir(self):
        return self._mkdir(os.path.join(self.test_dir, "processed_feature_data"))

    def load_radiomics_utility(self) -> RadiomicsUtility:
        # read from pkl file
        util_path = os.path.join(self.train_dir, PKL_RADIOMICS_UTILITY_NAME)
        if os.path.exists(util_path):
            return joblib.load(util_path)

        # create instance from yaml config file
        yaml_path = os.path.join(self.train_dir, RADIOMICS_CONFIG_NAME)
        assert os.path.exists(yaml_path), f"Found no config file: {yaml_path}"
        extractor = RadiomicsFeatureExtractor(yaml_path)
        return RadiomicsUtility(extractor=extractor, data_type=self.data_type)

    @property
    def radiomics_config_path(self):
        return os.path.join(self.train_dir, RADIOMICS_CONFIG_NAME)

    @property
    def fe_dir(self):
        return self._mkdir(os.path.join(self.task_dir, "fe"))

    @property
    def fe_path(self):
        return os.path.join(self.fe_dir, PKL_FE_NAME)

    def load_fe(self):
        return joblib.load(self.fe_path)

    def dump_fe(self, fe):
        joblib.dump(fe, self.fe_path)

    @property
    def model_dir(self):
        return self._mkdir(os.path.join(self.task_dir, "model"))

    @property
    def model_path(self):
        return os.path.join(self.model_dir, PKL_MODEL_NAME)

    def load_model(self):
        return joblib.load(self.model_path)

    def dump_model(self, model):
        joblib.dump(model, self.model_path)

    @property
    def dataset_instance_path(self):
        return os.path.join(self.dataset_dir, PKL_DATASET_NAME)

    def load_dataset_instance(self):
        return joblib.load(self.dataset_instance_path)

    def dump_dataset_instance(self, dataset):
        joblib.dump(dataset, self.dataset_instance_path)
