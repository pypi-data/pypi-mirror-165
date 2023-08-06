from pathlib import Path
from typing import Sequence

from pydantic import BaseModel
from strictyaml import YAML, load

import classifier_model

# Project Directories
PACKAGE_ROOT = Path(classifier_model.__file__).resolve().parent
ROOT = PACKAGE_ROOT.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATASET_DIR = PACKAGE_ROOT / "dataset"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "models"
LOGS_DIR = ROOT / "logs"


class AppConfig(BaseModel):
    """
    The BaseModel help us to automatically verify each
    variable.
    """

    package_name: str
    train_data: str
    test_data: str
    pipeline_save_file: str


class ModelConfig(BaseModel):
    """
    Model configuration class
    """

    target: str
    unused_fields: Sequence[str]
    features: Sequence[str]
    test_size: float
    random_state: int
    numerical_vars: Sequence[str]
    categorical_vars: Sequence[str]
    num_mean_impute_vars: Sequence[str]
    cat_woe_encoding: Sequence[str]
    cat_missing_impute_vars: Sequence[str]
    cat_arbitrary_impute_vars: Sequence[str]


class Config(BaseModel):
    """
    Main config object
    """

    app_config: AppConfig
    model_config: ModelConfig


def find_config_file() -> Path:
    """Locate the configuration file"""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH}")


def fetch_config_from_yaml(cfg_path: Path = None) -> YAML:
    """Parse YAML containing the package configuration"""

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None):
    """Run validation on config values."""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        app_config=AppConfig(**parsed_config.data),
        model_config=ModelConfig(**parsed_config.data),
    )

    return _config


config = create_and_validate_config()
