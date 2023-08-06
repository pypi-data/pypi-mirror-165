from typing import Any, Union

import numpy as np
import pandas as pd

from classifier_model import __version__ as _version
from classifier_model.config.core import config
from classifier_model.preprocessing.data_manager import load_pipeline
from classifier_model.preprocessing.data_validation import validate_inputs


def make_prediction(*, input_data: Union[pd.DataFrame, dict]) -> dict[str, Any]:

    validated_data, errors = validate_inputs(input_data=input_data)

    pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    pipeline = load_pipeline(file_name=pipeline_file_name)

    results = {"predictions": None, "version": _version, "errors": errors}

    if not errors:
        results["predictions"] = pipeline.predict(
            validated_data[config.model_config.features]
        ).astype(np.int64)

    return results
