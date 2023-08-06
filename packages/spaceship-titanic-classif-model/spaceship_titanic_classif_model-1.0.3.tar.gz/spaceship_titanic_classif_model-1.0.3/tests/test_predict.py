import numpy as np
from sklearn.metrics import accuracy_score

from classifier_model.predict import make_prediction


def test_predict_model(sample_input_data):

    dt_X, dt_y = sample_input_data
    result = make_prediction(input_data=dt_X)

    test_size = 626
    assert result.get("predictions").shape[0] == test_size
    assert isinstance(result.get("predictions"), np.ndarray)
    assert isinstance(result.get("predictions")[0], np.int64)
    assert not result.get("errors")
    assert accuracy_score(dt_y, result.get("predictions")) > 0.7
