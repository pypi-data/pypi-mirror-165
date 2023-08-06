"""
Logic related to exporting a trained model with a corresponding
preprocessing pipeline.
"""
import abc
import datetime
import logging
from copy import deepcopy
from pathlib import Path
from typing import Optional

import joblib
from sklearn.pipeline import Pipeline

from . import _internals

logger = logging.getLogger(f"stream.{__name__}")


def export_model(setup: _internals.Setup, model, target_dir: str) -> None:
    """Exports provided `model` with preprocessing pipeline stored in
    setup.

    The output file is binarized using joblib and saved to `target_dir`.
    The output filename follows the syntax
      `model_{date}_{algo}_#{number}.joblib`
    where
    - `date` is the current date in format YYYY-MM-DD
    - `algo` is the utilised model algorithm, and
    - `number` is a number assigned when other models with the same
    name already exist.

    Example
    -------
    >>> pt.modelling.export_model(
            setup=setup,
            model=model_list[0],
            target_dir="./",
        )

    Parameters
    ----------
    setup : _internals.Setup
        Setup object containing preprocessing pipeline.

    model :
        Trained model instance.

    target_dir : str
        Target directory for saving the output file to.
    """
    full_pipe = _combine_pipeline_and_model(prep_pipe=setup.prep_pipe, model=model)
    export_name = _get_export_name(target_dir=target_dir, model=model)
    joblib.dump(full_pipe, Path(target_dir) / export_name)
    logger.info(f"Exported modelling pipeline to '{Path(target_dir) / export_name}'")


def _combine_pipeline_and_model(prep_pipe: Pipeline, model) -> Pipeline:
    """Adds `model` as last step to `prep_pipe`."""
    # Making deep copy, so that the model-step is not added to the
    # original pipeline object.
    prep_pipe_copy = deepcopy(prep_pipe)
    prep_pipe_copy.steps.append(("model", model))
    return prep_pipe_copy


def _get_export_name(target_dir: str, model) -> str:
    """Generates filename for `full_pipe`."""
    date = str(datetime.date.today())
    algo = _get_algo_abbreviation(model_type=type(model))
    temp_name = f"model_{date}_{algo}_#"
    new_number = _get_new_number(target_dir=target_dir, temp_name=temp_name)
    return (
        f"model_{date}_{algo}_#{new_number}.joblib"
        if new_number
        else f"model_{date}_{algo}_#1.joblib"
    )


def _get_algo_abbreviation(model_type: abc.ABCMeta) -> str:
    """Returns string abbreviation for provided algorithm."""
    algo_dict = _internals.get_algo_dict()
    return [key for key in algo_dict.keys() if algo_dict[key] == model_type][0]


def _get_new_number(target_dir: str, temp_name: str) -> Optional[int]:
    """Determines the number value for the new file name by
    checking `target_dir` for pre-existing files with matching
    name pattern.

    Parameters
    ----------
    target_dir : str
        Target directory for new file. This is also where for
        pre-existing files of similar name is checked.

    temp_name : str
        Basic name structure for new file.

    Returns
    -------
    Optional[int]
        Integer value of the new number, or None.
        None is returned when no pre-existing file is found.
    """
    files_in_target_dir = [
        str(path.name) for path in Path(target_dir).glob("./*") if path.is_file()
    ]
    files_matching_pattern = [
        filename for filename in files_in_target_dir if temp_name in filename
    ]
    if len(files_matching_pattern) > 0:
        last_entry = sorted(files_matching_pattern)[-1]
        last_number = int(last_entry.rsplit("#")[-1].split(".joblib")[0])
        return last_number + 1
    else:
        return None
