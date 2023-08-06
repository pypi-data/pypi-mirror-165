"""
Contains logic for hyperparameter tuning.

Example
-------
>>> import pycarrot as pc
>>> from sklearn.datasets import load_breast_cancer

>>> bc = load_breast_cancer()
>>> X = pd.DataFrame(bc.data, columns=bc.feature_names)
>>> y = pd.Series(bc.target, name="class")
>>> df = pd.concat([X, y], axis=1)

>>> config = pt.init_config("./config_bc.yml")

>>> setup, X_sample, y_sample = pt.modelling.prepare_data(
        train_data=df,
        config=config,
    )

>>> compare_df, algo_list, model_list = (
            pt.modelling.tune_hyperparams(
                   setup=setup,
                   include=["lr", "knn"],
                   optimize="f1",
                   n_trials=50,
                   return_models=True,
            )
    )
"""
import logging
from typing import List, Optional, Tuple

import numpy as np
import optuna
import pandas as pd
from sklearn.model_selection import cross_val_score

from . import _internals

logger = logging.getLogger(f"stream.{__name__}")

# Turning off logging information during tuning
optuna.logging.set_verbosity(optuna.logging.WARNING)


def tune_hyperparams(
    setup: _internals.Setup,
    include: List[str],
    optimize: str,
    n_trials: int = 20,
    feature_list: Optional[List[str]] = None,
    return_models: bool = False,
) -> Tuple[pd.DataFrame, list, list]:
    """Tunes the algorithms provided in the `include` parameter.

    Example
    -------
    >>> compare_df, model_list = (
                pt.modelling.tune_hyperparams(
                    setup=setup,
                    include=["lr", "knn"],
                    optimize="f1",
                    n_trials=50,
                    return_models=True,
                )
        )

    Parameters
    ----------
    setup : Setup
        Dataclass containing the prepared data and further
        configurations.

    include : List[str]
        List of identifier strings for algorithms to tune.

    optimize : str
        String identifier of metric to optimize for.

    n_trials : int, optional
        Number of hyperparameter combinations to evaluate,
        by default 20

    feature_list: Optional[List[str]] = None
        If provided, will tune the model with provided
        feature list. Useful after reduce_feature_space()
        has been evaluated.

    return_models : bool, optional
        Flag for training models on the entire dateset using the
        best hyperparameter combinations found, by default False

    Returns
    -------
    Tuple[pd.DataFrame, list, dict]
        compare_df : pd.DataFrame
            sorted overview of algorithm performance

        model_list : list
            List of model instances trained on entire training data
            using best hyperparameter combination found. List is ordered
            by achieved metric. Only runs if return_models == True.
            Otherwise returns list of None.

        opt_history_dict : dict
            Dictionary containing algorithms as keys and figures of the
            optimization history as values.
            Use `opt_history_dict["algorithm"].show()` in a jupyter notebook
            to plot the graph.
    """
    logger.info("%%% TUNING HYPERPARAMETERS")

    # Checking inputs
    _internals.check_include(algo_list=include)
    _internals.check_metric(metric=optimize)
    _internals.check_feature_scaling(
        algo_list=include, feature_scaling=setup.feature_scaling
    )

    # Preparing empty compare_df and model_dict
    # with populating occuring later
    compare_df = pd.DataFrame({}, columns=["algorithm", "metric", "hyperparams"])
    model_dict = {}
    opt_history_dict = {}

    logger.info(f"Algorithms: {include}")
    logger.info(f"Metric: {optimize}")
    logger.info(f"Trials per algorithm: {n_trials}")

    for algorithm in include:
        # Preparation of tuning
        objective = _get_objective_function(
            algorithm=algorithm,
            optimize=optimize,
            X=setup.X_train[feature_list] if feature_list else setup.X_train,
            y=setup.y_clf_train,
        )
        study = optuna.create_study(
            study_name=f"study_{algorithm}", direction="maximize"
        )

        # Tuning
        logging_callback = TrialLoggingCallback()
        study.optimize(objective, n_trials=n_trials, callbacks=[logging_callback])

        # Aggreration of results
        metric, hyperparams = _get_best_result(study)
        compare_df.loc[len(compare_df)] = [
            algorithm,
            metric,
            hyperparams,
        ]
        opt_history_dict[algorithm] = optuna.visualization.plot_optimization_history(
            study
        )

        # Training model on entire dataset
        if return_models:
            model_dict[algorithm] = (
                _internals.get_model_instance(algorithm=algorithm)
                .set_params(**hyperparams)
                .fit(setup.X_train, setup.y_clf_train)
            )

    compare_df = compare_df.sort_values(by="metric", ascending=False).reset_index(
        drop=True
    )
    model_list = [model_dict[key] for key in compare_df["algorithm"]]
    logger.info(f"\n {compare_df[['algorithm', 'metric']]}")

    return compare_df, model_list, opt_history_dict


def _get_objective_function(
    algorithm: str, optimize: str, X: pd.DataFrame, y: pd.Series
) -> object:
    """Returns model specific objective function for usage in optuna's
    stduy.optimize() function.

    Parameters
    ----------
    algorithm : str
        Model algorithm to use in objective function.

    optimize : str
        Metric to optimize for.

    X : pd.DataFrame
        Dataframe containing training features.

    y : pd.Series
        Series containing target variable.

    Returns
    -------
    object
        `objective function` object
    """

    def objective_fn(trial: optuna.Trial) -> np.float64:
        """Objective function for usage within optuna's study.optimize().

        Parameters
        ----------
        trial : optuna.Trial
            Handled automatically by study.optimize()

        Returns
        -------
        np.float64
            Mean metric of all folds.
        """
        model = _internals.get_model_instance(algorithm=algorithm, trial=trial)
        trial.set_user_attr("hyperparams", model.get_params())
        cv_scores = cross_val_score(
            model,
            X,
            y,
            scoring=optimize,
            n_jobs=-1,
            error_score="raise",
        )

        return cv_scores.mean()

    return objective_fn


def _get_best_result(study: optuna.Study) -> Tuple[float, dict]:
    """Returns metric and hyperparameters of best model found
    during study run.

    Parameters
    ----------
    study : optuna.Study

    Returns
    -------
    Tuple[float, dict]
        metric : float
        hyperparams : dict
    """
    return study.best_trial.values[0], study.best_trial.user_attrs["hyperparams"]


class TrialLoggingCallback:
    def __call__(
        self, study: optuna.study.Study, trial: optuna.trial.FrozenTrial
    ) -> None:
        logger.info(
            f"Trial {trial.number} finished with value: {study.trials[trial.number].value:.4f} and parameters: {trial.params}. "
            f"Best is trial {study.best_trial.number} with value: {study.best_value:.4f}"
        )
