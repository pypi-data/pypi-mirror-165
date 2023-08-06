import pytest
from sklearn.model_selection import train_test_split

from classifier_model.config.core import config
from classifier_model.preprocessing.data_manager import load_dataset


@pytest.fixture
def sample_input_data():
    data = load_dataset(file_name=config.app_config.train_data)

    X_, X, y_, y = train_test_split(
        data[config.model_config.features],
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        random_state=config.model_config.random_state,
    )

    return X, y
