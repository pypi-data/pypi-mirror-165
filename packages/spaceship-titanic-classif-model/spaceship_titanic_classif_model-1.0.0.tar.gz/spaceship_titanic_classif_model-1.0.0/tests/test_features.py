import pandas as pd

from classifier_model.preprocessing.features import CabinPreprocess


def test_cabin_process():
    cabin_pipe = CabinPreprocess()

    X = pd.DataFrame({"Cabin": ["A/B/C"]})
    result = cabin_pipe.fit_transform(X=X).values[0]
    assert result[0] == "A"
    assert result[-1] == "C"
