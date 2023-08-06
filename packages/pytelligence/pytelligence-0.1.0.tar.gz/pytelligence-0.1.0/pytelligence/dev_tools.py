"""
Contains tools for developing pycarrot.
"""
from typing import Tuple

import numpy as np
import pandas as pd

from .modelling import _prepare_data


def load_dataset(type_: str, name: str) -> Tuple[pd.DataFrame, dict]:
    """Loads specified dataset as a pandas dataframe and a
    pre-generated config file to be used with pycarrot.

    Parameters
    ----------
    type : str
        Specification of type of dataset. Either clf or reg
        for classification and regression respectively.
    name : str
        Identifier for the dataset. Possible values:
        Classification:
            1) numeric_noNAs_binary - based on breast_cancer
               dataset
        Regression:
        -

    Returns
    -------
    Tuple[pd.DataFrame, dict]
        Dataframe and config dictionary for processing with
        pycarrot.
    """
    if type_ == "clf":
        path_stem = f"./dev_datasets/classification/{name}"
    elif type_ == "reg":
        path_stem = f"./dev_datasets/regression/{name}"

    df = pd.read_parquet(f"{path_stem}.parquet")
    config = _prepare_data._init_config(path=f"{path_stem}.yml")
    return df, config


def drop_random_entries(
    df: pd.DataFrame, pct: float = 0.1, keep: str = None
) -> pd.DataFrame:
    """Drops entries from pd.DataFrame at random. Used for creating
    dataframes with missing information.

    Parameters
    ----------
    df : pd.DataFrame
        Original dataframe without missing values.
    pct : float, optional
        Fraction of values to drop, by default 0.1
    keep : str, optional
        Column name of column to leave unmodified (typically target variable),
        by default None

    Returns
    -------
    pd.DataFrame
        Dataframe with randomly dropped values.
    """
    df = df.copy()
    features = [col for col in df.columns if col != keep]
    num_entries_to_drop = int(np.floor(len(features) * len(df) * pct))
    for _ in range(num_entries_to_drop):
        col = np.random.choice(features)
        loc = np.random.randint(len(df))
        df.loc[loc, col] = np.nan
    return df
