"""
Contains utilty functionality used by various modules.
"""
import logging
from typing import List, Optional

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB

logger = logging.getLogger(f"stream.{__name__}")


def get_available_algos() -> List[str]:
    """
    Returns a list of strings where each string is the
    abbreviation of an algorithm.
    """
    return list(get_algo_dict().keys())


def get_algo_dict() -> dict:
    """
    Returns a dictionary with keys being algorithm abbreviations
    (strings) and values being the callables of the algorithms.
    """
    return {
        "lr": LogisticRegression,
        "nb": GaussianNB,
        # "linearsvc",
        # "rbfsvc",
        # "dt",
        # "extratree",
        # "extratrees",
        # "rf",
        # "ridge",
        # "perceptron",
        # "passive-aggressive",
        # "knn",
    }


def check_include(algo_list: List[str]):
    """Checks `algo_list` for correct strings.

    Parameters
    ----------
    algo_list : List[str]
        List of strings referring to implemented model algorithms.

    Raises
    ------
    LookupError
        In case a string is not matched by an implemented algorithm,
        raises a LookupError.
    """
    available_algos = get_available_algos()
    for entry in algo_list:
        if entry not in available_algos:
            raise LookupError(
                f"'{entry}' was provided in the include parameter, but is not among the avaiable algorithms."
            )


def check_metric(metric: Optional[str]):
    """Checks whether `metric` is among the implemented metrics.
    Raises LookupError if `metric` is not implemented and not None.

    Raises
    ------
    LookupError
        In case `metric` is not matched by an implemented algorithm
        or None, raises a LookupError.
    """
    if metric not in [
        None,
        "algorithm",
        "accuracy",
        "precision",
        "recall",
        "f1",
        "roc_auc",
    ]:
        raise LookupError(
            f"'{metric}' was provided as sort parameter, but is not among the avaiable metrics."
        )


def check_feature_scaling(algo_list: List[str], feature_scaling: bool) -> None:
    """Checks for feature_scaling and writes note to logger.INFO if any of
    the utilized algorithms would profit from feature_scaling.

    Parameters
    ----------
    algo_list : List[str]
        List of utilized algorithms.

    feature_scaling : bool
        Option documented in setup object. Specified in config.
    """
    if not feature_scaling:
        affected_algos = [algo for algo in algo_list if algo in ["lr"]]
        if len(affected_algos) > 0:
            logger.warning(
                f"The algorithms {affected_algos} work suboptimally without scaled features. Consider turning it on within the config and rerun pt.modelling.prepare_data()."
            )
