from classifier_model.config.core import config


def test_model_config_fields():

    target = config.model_config.target
    n_features = len(config.model_config.features)

    assert target == "Transported"
    assert n_features == 11


def test_app_config_fields():

    assert config.app_config.package_name == "spaceship_titanic_model"
    assert (
        config.app_config.pipeline_save_file
        == "spaceship_titanic_pipeline_model_output_v"
    )
