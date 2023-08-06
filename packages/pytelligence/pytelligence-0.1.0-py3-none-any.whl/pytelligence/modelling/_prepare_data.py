import logging
from typing import List, Tuple

import pandas as pd
import yaml
from sklearn.preprocessing import LabelEncoder

from . import _internals

logger = logging.getLogger(f"stream.{__name__}")


def prepare_data(
    train_data: pd.DataFrame,
    config_path: str,
) -> Tuple[_internals.Setup, pd.DataFrame, pd.Series]:
    """Prepares data by
      1) One-Hot-Encoding remaining categorical features
      2) Encoding labels of classification target - if required

    Parameters
    ----------
    train_data : pd.DataFrame
        Dataframe provided by user. Must contain columns specified in config.
    config_path : dict
        Path to config containing input features and preparational options.

    Returns
    -------
    Tuple
        Setup, which will be handed to function compare_algorithms
        for further processing.
        X_sample & y_sample showing what the data looks like after
        preparation.
    """
    logger.info("%%% PREPARING DATA")
    # Loading config
    config = _init_config(path=config_path)

    # Checking input
    _check_clf_target(train_data, config["modelling"]["target_clf"])
    _check_numeric_cols(train_data, config["modelling"]["numeric_cols"])
    _check_categorical_cols(train_data, config["modelling"]["categorical_cols"])

    # Get features and targets from config
    original_features = _get_original_features(config)
    target_clf = config["modelling"]["target_clf"]

    ###################
    ### Preparation ###

    # Assembling preprocessing pipeline
    prep_pipe = _internals.get_prep_pipeline()

    # Composing X_train
    X_train = prep_pipe.fit_transform(train_data[original_features])
    logger.info("Applied preprocessing transformations")

    # Encoding target_clf
    y_train, y_clf_encoder = _encode_y_train(train_data[target_clf])

    return (
        _internals.Setup(
            X_train=X_train,
            y_clf_train=y_train,
            y_clf_encoder=y_clf_encoder,
            feature_scaling=config["modelling"]["feature_scaling"],
            prep_pipe=prep_pipe,
        ),
        X_train.head(),
        y_train.head(),
    )


def _init_config(path: str):
    with open(path, "r") as stream:
        try:
            config = yaml.safe_load(stream)
            logger.info(f"Read {path}: \n {config}")
            return config
        except yaml.YAMLError as exc:
            print(exc)


def _check_clf_target(train_data: pd.DataFrame, clf_col: str = None) -> None:
    """Raises LookupError if clf target column not in
    train_data dataframe.

    Parameters
    ----------
    train_data : pd.DataFrame
        Lookuperror

    clf_col : str
    """
    if clf_col:
        if clf_col not in train_data:
            raise LookupError(
                f"{clf_col}, which was provided as 'target_clf', is not in\
                    train_data dataframe. Check existence and spelling."
            )


def _check_numeric_cols(
    train_data: pd.DataFrame, numeric_cols: List[str] = None
) -> None:
    """Raises LookupError if one or more of the numeric
    columns listed in config are missing.

    Parameters
    ----------
    train_data : pd.DataFrame

    numeric_cols : List[str]
    """
    if numeric_cols:
        for col in numeric_cols:
            if col not in train_data:
                raise LookupError(
                    f"{col}, which was provided in 'numeric_cols', is not in\
                        train_data dataframe. Check existence and spelling."
                )


def _check_categorical_cols(
    train_data: pd.DataFrame, categorical_cols: List[str]
) -> None:
    """Raises LookupError if one or more of the categorical
    columns listed in config are missing.

    Parameters
    ----------
    train_data : pd.DataFrame

    categorical_cols : List[str]
    """
    if categorical_cols:
        for col in categorical_cols:
            if col not in train_data:
                raise LookupError(
                    f"{col}, which was provided in 'categorical_cols', is not in\
                        train_data dataframe. Check existence and spelling."
                )


def _encode_y_train(y: pd.Series) -> Tuple[pd.Series, LabelEncoder]:
    """Encodes target column of classification problems if required.
    Regardless of encoding, downcasts target column to save memory.

    Parameters
    ----------
    y : pd.Series
        Column to encode

    Returns
    -------
    Tuple[pd.Series, LabelEncoder]
        Encoded column and fitted LabelEncoder containing class labels.
    """
    if not _check_encoding_necessity(y):
        return pd.to_numeric(y, downcast="integer"), LabelEncoder()
    else:
        le = LabelEncoder().fit(y)
        y_trans = pd.Series(le.transform(y), name=y.name)
        logger.info(
            f"Encoded target variable using classes: {[(i, class_) for i, class_ in enumerate(le.classes_)]}"
        )
        return pd.to_numeric(y_trans, downcast="integer"), le


def _check_encoding_necessity(y: pd.Series) -> bool:
    """Checks column for dtype integer.

    Parameters
    ----------
    y : pd.Series
        Target column of classification problem.

    Returns
    -------
    bool
        Boolean flag used for encoding
    """
    return True if (y.dtype == "O") else False


def _get_original_features(config: dict) -> List[str]:
    """Returns list of features passed to prepare_data function.

    Parameters
    ----------
    config : dict

    Returns
    -------
    List[str]
        Combination of numeric, categorical and date features listed
        in config.yml.
    """
    numeric_features = (
        config["modelling"]["numeric_cols"]
        if config["modelling"]["numeric_cols"]
        else []
    )
    categorical_features = (
        config["modelling"]["categorical_cols"]
        if config["modelling"]["categorical_cols"]
        else []
    )

    return [*numeric_features, *categorical_features]
