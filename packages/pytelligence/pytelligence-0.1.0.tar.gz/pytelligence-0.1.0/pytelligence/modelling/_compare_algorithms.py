import logging
from typing import List, Optional, Tuple

import pandas as pd

from . import _internals
from ._train_model import train_model

logger = logging.getLogger(f"stream.{__name__}")


def compare_algorithms(
    setup: dict,
    include: List[str] = _internals.get_available_algos(),
    sort: Optional[str] = None,
    return_models: bool = False,
    feature_list: Optional[List[str]] = None,
) -> Tuple[pd.DataFrame, List, List]:
    """
    Calculates various metrics for different machine learning
    algorithms.

    Parameters
    ----------
    setup : dict stemming from pt.modelling.prepare_data(...)

    include : optional list of strings
        declares what algorithms to compare

    sort : optional str
        defines how compare_df is sorted

    return_models: bool
        Flag for returning model instances trained on the
        entire training set. By default set to false to
        save on computational time.

    feature_list: Optional[List[str]] = None
        If provided, will compare the algorithms with provided
        feature list. Useful after reduce_feature_space()
        has been evaluated.

    Returns
    -------
    compare_df : pd.DataFrame
        sorted overview of algorithm performance

    algo_list : list
        List of algorithms ordered by sort metric.

    model_list : list
        Trained model instance if return_models == True.
        Otherwise returns list of None.
    """
    logger.info("%%% COMPARING ALGORITHMS")

    # Checking inputs
    _internals.check_include(include)
    _internals.check_metric(metric=sort)
    _internals.check_feature_scaling(
        algo_list=include, feature_scaling=setup.feature_scaling
    )

    # Preparing empty compare_df and model_dict
    # with populating occuring later
    compare_df = _prepare_compare_df()
    model_dict = {}

    # Training models
    for algorithm in include:
        logger.info(f"Evaluating {algorithm}...")
        model, metrics = train_model(
            algorithm=algorithm,
            setup=setup,
            return_models=return_models,
            feature_list=feature_list,
        )
        compare_df = pd.concat([compare_df, metrics])
        model_dict[algorithm] = model

    # Sort compare_df
    if sort:
        compare_df = compare_df.sort_values(
            by=[sort, "Fit time (s)"],
            ascending=[False, True],
        ).reset_index(drop=True)

    algo_list = compare_df["algorithm"].to_list()
    model_list = [model_dict[key] for key in compare_df["algorithm"]]

    return compare_df, algo_list, model_list


def _prepare_compare_df() -> pd.DataFrame:
    """
    Creates compare_df dataframe with required columns,
    but no entries yet.

    Returns
    -------
    compare_df : pd.DataFrame
    """
    return pd.DataFrame(
        columns=[
            "algorithm",
            "accuracy",
            "precision",
            "recall",
            "f1",
            "roc_auc",
            "Fit time (s)",
        ]
    )
