# *****************************************************************
#
# Licensed Materials - Property of IBM
#
# (C) Copyright IBM Corp. 2018, 2020. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
#
# *****************************************************************

from snapml.Model import Model

from snapml.BoostingMachine import BoostingMachine
from snapml.BoostingMachineRegressor import BoostingMachineRegressor
from snapml.BoostingMachineClassifier import BoostingMachineClassifier
from snapml.RandomForestRegressor import RandomForestRegressor
from snapml.RandomForestClassifier import RandomForestClassifier

from snapml._import import import_libsnapml

libsnapml = import_libsnapml(False)


def import_model(
    input_file,
    input_type="pmml",
    tree_format="compress_trees",
    X=None,
    remap_feature_indices=False,
):
    """
    Import a pre-trained tree ensemble model and optimize the trees for fast inference.

    This function will detect the ensemble type (e.g. boosting or forest) and task type
    (classification or regression) from the model file and return the correct Snap ML class.

    Currently only models stored as PMML are supported.

    Depending on the how the tree_format argument is set, this function will return a different
    optimized model format. This format determines which inference engine is used for subsequent
    calls to 'predict' or 'predict_proba'.

    If tree_format is set to 'compress_trees', the model will be optimized for execution on the CPU, using our
    compressed decision trees approach. Note: if this option is selected, an optional dataset X can be provided,
    which will be used to predict node access characteristics during node clustering.

    If tree_format is set to 'zdnn_tensors', the model will be optimized for execution on the IBM z16 AI accelerator,
    using a matrix-based inference algorithm leveraging the zDNN library.  Note: if this option is selected,
    the maximum batch size that can be scored by subsequent calls to 'predict' or 'predict_proba' will be 2^15 since
    this is the maximum tensor dimension supported by zDNN library.

    Note: If the input file contains features that are not supported by the import function, then an exception is thrown
    indicating the feature and the line number within the input file containing the feature.

    Parameters
    ----------
    input_file : str
        Input filename

    input_type : {'pmml'}
        Input file type

    tree_format : {'compress_trees', 'zdnn_tensors'}
        Tree format

    X : dense matrix (ndarray)
        Optional input dataset used for compressing trees

    remap_feature_indices : bool
        If enabled, predict and predict_proba functions will expect numpy arrays containing only the (ordered) features
        that are listed in the model file. This can often be a subset of the full set of feature that were provided during
        training. These features are stored in the `used_features_` attribute in the imported model.

    Returns
    -------
    self : Snap ML object ready for scoring
    """

    if input_type != "pmml":
        raise ValueError(
            "Generic model import currently supports only 'pmml' as the input type. "
            + "Model-specific import functions (e.g., the import_model member function of BoostingMachineClassifer) support additional formats such as 'onnx', 'xgb_json' and 'lightgbm'."
        )

    model_ptr = Model()

    task_type, model_type, classes, n_classes, used_features = libsnapml.generic_import(
        input_file, input_type, remap_feature_indices, model_ptr.get()
    )

    if classes is not None:
        ind2class = {}
        for i, c in enumerate(classes):
            ind2class[i] = c
    else:
        ind2class = None

    if model_type == "forest":
        out = (
            RandomForestClassifier()
            if task_type == "classification"
            else RandomForestRegressor()
        )
        out.used_features_ = used_features
        out.model_ptr_ = model_ptr
        out.classes_ = classes
        out.n_classes_ = n_classes
        out.ind2class_ = ind2class
        out.optimize_trees(tree_format, X)
    else:
        out = (
            BoostingMachineClassifier()
            if task_type == "classification"
            else BoostingMachineRegressor()
        )
        out.used_features_ = used_features
        out.booster_ = BoostingMachine(out.make_boosting_params())
        out.booster_.model_ptr_ = model_ptr
        out.booster_.classes_ = classes
        out.booster_.n_classes_ = n_classes
        out.booster_.ind2class_ = ind2class
        out.booster_.optimize_trees(tree_format, X)

    return out
