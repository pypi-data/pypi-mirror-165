# from Scikit-learn
from feature_engine.creation import MathematicalCombination
from feature_engine.datetime import DatetimeFeatures
from feature_engine.encoding import OrdinalEncoder, RareLabelEncoder

# from feature-engine
from feature_engine.imputation import ArbitraryNumberImputer, CategoricalImputer
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline

from model.config.core import config

# set up the pipeline
mortgage_pipe = Pipeline(
    [
        # ===== IMPUTATION =====
        # transform datetime variables
        (
            "datetime_transformer",
            DatetimeFeatures(
                variables=config.model_config.datetime_vars,
                features_to_extract=["year", "month", "day_of_week", "day_of_month"],
                drop_original=True,
                missing_values="ignore",
            ),
        ),
        # Create Features based on domain knowledge
        (
            "math_combinator_1",
            MathematicalCombination(
                variables_to_combine=config.model_config.feature_creation_1,
                math_operations=["sum", "prod"],
                missing_values="ignore",
            ),
        ),
        (
            "math_combinator_2",
            MathematicalCombination(
                variables_to_combine=config.model_config.feature_creation_2,
                math_operations=["sum", "prod"],
                missing_values="ignore",
            ),
        ),
        (
            "math_combinator_3",
            MathematicalCombination(
                variables_to_combine=config.model_config.feature_creation_3,
                math_operations=["sum", "prod"],
                missing_values="ignore",
            ),
        ),
        (
            "math_combinator_4",
            MathematicalCombination(
                variables_to_combine=config.model_config.feature_creation_4,
                math_operations=["sum", "prod"],
                missing_values="ignore",
            ),
        ),
        (
            "math_combinator_5",
            MathematicalCombination(
                variables_to_combine=config.model_config.feature_creation_5,
                math_operations=["sum", "prod"],
                missing_values="ignore",
            ),
        ),
        # impute categorical variables with string missing
        (
            "missing_imputation",
            CategoricalImputer(
                imputation_method="missing",
                variables=config.model_config.categorical_vars,
                ignore_format=True,
            ),
        ),
        (
            "arbitrary_imputation",
            ArbitraryNumberImputer(
                arbitrary_number=-999, variables=config.model_config.numerical_vars
            ),
        ),
        # == CATEGORICAL ENCODING
        (
            "rare_encoder",
            RareLabelEncoder(
                tol=0.05,
                n_categories=15,
                variables=config.model_config.categorical_vars,
                replace_with="Rare",
                ignore_format=True,
            ),
        ),
        (
            "categorical_encoder",
            OrdinalEncoder(
                encoding_method="arbitrary",
                variables=config.model_config.categorical_vars,
                ignore_format=True,
            ),
        ),
        ("gbm", GradientBoostingClassifier(random_state=23)),
    ]
)
