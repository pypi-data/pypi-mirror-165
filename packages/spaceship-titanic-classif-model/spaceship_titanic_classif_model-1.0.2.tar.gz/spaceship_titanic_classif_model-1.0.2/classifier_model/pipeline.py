from feature_engine.encoding import WoEEncoder
from feature_engine.imputation import CategoricalImputer, MeanMedianImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from classifier_model.config.core import config
from classifier_model.preprocessing.features import CabinPreprocess

spaceship_titanic_pipeline = Pipeline(
    [
        (
            "CatMissingImputer",
            CategoricalImputer(
                fill_value="NA",
                variables=config.model_config.cat_missing_impute_vars,
            ),
        ),
        (
            "CatMissingArbitraryImputer",
            CategoricalImputer(
                variables=config.model_config.cat_arbitrary_impute_vars,
                fill_value=False,
            ),
        ),
        ("CabinPreprocess", CabinPreprocess()),
        (
            "NumMeanImputer",
            MeanMedianImputer(variables=config.model_config.num_mean_impute_vars),
        ),
        (
            "CatWOEEncoder",
            WoEEncoder(variables=config.model_config.cat_woe_encoding),
        ),
        ("StandardScaler", StandardScaler()),
        ("LogisticRegression", LogisticRegression()),
    ]
)
