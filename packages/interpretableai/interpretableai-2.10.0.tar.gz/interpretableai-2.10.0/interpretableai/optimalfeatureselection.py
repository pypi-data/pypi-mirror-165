from .iai import _IAI, _requires_iai_version
from .iaibase import (SupervisedLearner, ClassificationLearner,
                      RegressionLearner, Questionnaire)


class OptimalFeatureSelectionLearner(SupervisedLearner):
    """Abstract type encompassing all Optimal Feature Selection learners.

    Julia Equivalent:
    `IAI.OptimalFeatureSelectionLearner <https://docs.interpretable.ai/v3.1.0/OptimalFeatureSelection/reference/#IAI.OptimalFeatureSelectionLearner>`
    """

    def get_prediction_constant(self, **kwargs):
        """Return the constant term in the prediction in the trained learner.

        Julia Equivalent:
        `IAI.get_prediction_constant <https://docs.interpretable.ai/v3.1.0/OptimalFeatureSelection/reference/#IAI.get_prediction_constant-Tuple%7BOptimalFeatureSelectionLearner%7D>`

        Examples
        --------
        Return the constant term in the prediction

        >>> lnr.get_prediction_constant()

        Return the constant term in the prediction for cluster `fit_index`

        >>> lnr.get_prediction_constant(fit_index=fit_index)

        Compatibility
        -------------
        Requires IAI version 1.1 or higher.
        """
        _requires_iai_version("1.1.0", "get_prediction_constant")
        return _IAI.get_prediction_constant_convert(self._jl_obj, **kwargs)

    def get_prediction_weights(self, **kwargs):
        """Return the weights for numeric and categoric features used for
        prediction in the trained learner.

        Julia Equivalent:
        `IAI.get_prediction_weights <https://docs.interpretable.ai/v3.1.0/OptimalFeatureSelection/reference/#IAI.get_prediction_weights-Tuple%7BOptimalFeatureSelectionLearner%7D>`

        Examples
        --------
        Return the weights in the prediction

        >>> lnr.get_prediction_weights()

        Return the weights in the prediction for cluster `fit_index`

        >>> lnr.get_prediction_weights(fit_index=fit_index)

        Compatibility
        -------------
        Requires IAI version 1.1 or higher.
        """
        _requires_iai_version("1.1.0", "get_prediction_weights")
        return _IAI.get_prediction_weights_convert(self._jl_obj, **kwargs)

    def get_num_fits(self):
        """Return the number of fits stored in the learner.

        Julia Equivalent:
        `IAI.get_num_fits <https://docs.interpretable.ai/v3.1.0/OptimalFeatureSelection/reference/#IAI.get_num_fits-Tuple%7BOptimalFeatureSelectionLearner%7D>`

        Examples
        --------
        >>> lnr.get_num_fits()

        Compatibility
        -------------
        Requires IAI version 3.0 or higher.
        """
        _requires_iai_version("3.0.0", "get_num_fits")
        return _IAI.get_num_fits_convert(self._jl_obj)

    def fit(self, *args, **kwargs):
        """Fit a model using the parameters in learner and the data `X` and `y`
        (see :meth:`interpretableai.iai.Learner.fit`).

        When the `coordinated_sparsity` parameter of the learner is `True`,
        additional keyword arguments are required - please refer to the Julia
        documentation.

        Julia Equivalent:
        `IAI.fit! <https://docs.interpretable.ai/v3.1.0/OptimalFeatureSelection/reference/#IAI.fit%21-Tuple%7BOptimalFeatureSelectionLearner%7D>`

        Examples
        --------
        >>> lnr.fit(X, *y, sample_weight=None, **kwargs)

        Compatibility
        -------------
        Requires IAI version 1.1 or higher.
        """
        _requires_iai_version("1.1.0", "fit")
        return super().fit(*args, **kwargs)

    def predict(self, *args, **kwargs):
        """Return the prediction made by the learner for each point in the data
        `X` (see :meth:`interpretableai.iai.SupervisedLearner.predict`).

        Julia Equivalent:
        `IAI.predict <https://docs.interpretable.ai/v3.1.0/OptimalFeatureSelection/reference/#IAI.predict-Tuple%7BOptimalFeatureSelectionLearner%2C%20Union%7BDataFrames.AbstractDataFrame%2C%20AbstractMatrix%7B%3C%3AReal%7D%7D%7D>`

        Examples
        --------
        Return the prediction made by the learner.

        >>> lnr.predict(X)

        Return the prediction made by cluster `fit_index` in the learner.

        >>> lnr.predict(X, fit_index=fit_index)

        Compatibility
        -------------
        Requires IAI version 1.1 or higher.
        """
        _requires_iai_version("1.1.0", "predict")
        return super().predict(*args, **kwargs)

    def score(self, *args, **kwargs):
        """Calculates the score for the learner on data `X` and `y` (see
        :meth:`interpretableai.iai.Learner.score`).

        Julia Equivalent:
        `IAI.score <https://docs.interpretable.ai/v3.1.0/OptimalFeatureSelection/reference/#IAI.score-Tuple%7BOptimalFeatureSelectionLearner%7D>`

        Examples
        --------
        Calculates the score for the learner.

        >>> lnr.score(X, *y, **kwargs)

        Calculates the score for cluster `fit_index` in the learner.

        >>> lnr.score(X, *y, **kwargs, fit_index=fit_index)

        Compatibility
        -------------
        Requires IAI version 1.1 or higher.
        """
        _requires_iai_version("1.1.0", "score")
        return super().score(*args, **kwargs)

    def variable_importance(self, *args, **kwargs):
        """Calculates the variable importance for the learner (see
        :meth:`interpretableai.iai.Learner.variable_importance`).

        Julia Equivalent:
        `IAI.variable_importance <https://docs.interpretable.ai/v3.1.0/OptimalFeatureSelection/reference/#IAI.variable_importance-Tuple%7BOptimalFeatureSelectionLearner%7D>`

        Examples
        --------
        Return the variable_importance for the learner.

        >>> lnr.variable_importance()

        Return the variable_importance for cluster `fit_index` in the learner.

        >>> lnr.variable_importance(fit_index=fit_index)

        Compatibility
        -------------
        Requires IAI version 1.1 or higher.
        """
        _requires_iai_version("1.1.0", "variable_importance")
        return super().variable_importance(*args, **kwargs)

    def Questionnaire(self, **kwargs):
        """Construct a
        :meth:`interpretableai.iai.Questionnaire`
        based on the trained learner.

        Julia Equivalent:
        `IAI.Questionnaire <https://docs.interpretable.ai/v3.1.0/OptimalFeatureSelection/reference/#IAI.Questionnaire-Tuple%7BOptimalFeatureSelectionLearner%7D>`

        Examples
        --------
        >>> iai.Questionnaire(lnr, **kwargs)

        Compatibility
        -------------
        Requires IAI version 2.1 or higher.
        """
        _requires_iai_version("2.1.0", "Questionnaire")
        return Questionnaire(self._jl_obj, **kwargs)

    def write_questionnaire(self, filename, **kwargs):
        """Write interactive questionnaire based on learner to `filename` as
        HTML.

        Julia Equivalent:
        `IAI.write_questionnaire <https://docs.interpretable.ai/v3.1.0/OptimalFeatureSelection/reference/#IAI.write_questionnaire-Tuple%7BAny%2C%20OptimalFeatureSelectionLearner%7D>`

        Examples
        --------
        >>> lnr.write_questionnaire(filename, **kwargs)

        Compatibility
        -------------
        Requires IAI version 2.1 or higher.
        """
        _requires_iai_version("2.1.0", "write_questionnaire")
        return _IAI.write_questionnaire_convert(filename, self._jl_obj,
                                                **kwargs)

    def show_questionnaire(self, **kwargs):  # pragma: no cover
        """Show interactive questionnaire based on learner in default browser.

        Julia Equivalent:
        `IAI.show_questionnaire <https://docs.interpretable.ai/v3.1.0/OptimalFeatureSelection/reference/#IAI.show_questionnaire-Tuple%7BOptimalFeatureSelectionLearner%7D>`

        Examples
        --------
        >>> lnr.show_questionnaire(**kwargs)

        Compatibility
        -------------
        Requires IAI version 2.1 or higher.
        """
        _requires_iai_version("2.1.0", "show_questionnaire")
        return _IAI.show_questionnaire_convert(self._jl_obj, **kwargs)


class OptimalFeatureSelectionClassifier(OptimalFeatureSelectionLearner, ClassificationLearner):
    """Learner for conducting Optimal Feature Selection on classification
    problems.

    Julia Equivalent:
    `IAI.OptimalFeatureSelectionClassifier <https://docs.interpretable.ai/v3.1.0/OptimalFeatureSelection/reference/#IAI.OptimalFeatureSelectionClassifier>`

    Examples
    --------
    >>> iai.OptimalFeatureSelectionClassifier(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.

    Compatibility
    -------------
    Requires IAI version 1.1 or higher.
    """
    def __init__(self, *args, **kwargs):
        _requires_iai_version("1.1.0", "OptimalFeatureSelectionClassifier")
        jl_obj = _IAI.OptimalFeatureSelectionClassifier_convert(*args, **kwargs)
        super().__init__(jl_obj)


class OptimalFeatureSelectionRegressor(OptimalFeatureSelectionLearner, RegressionLearner):
    """Learner for conducting Optimal Feature Selection on regression problems.

    Julia Equivalent:
    `IAI.OptimalFeatureSelectionRegressor <https://docs.interpretable.ai/v3.1.0/OptimalFeatureSelection/reference/#IAI.OptimalFeatureSelectionRegressor>`

    Examples
    --------
    >>> iai.OptimalFeatureSelectionRegressor(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.

    Compatibility
    -------------
    Requires IAI version 1.1 or higher.
    """
    def __init__(self, *args, **kwargs):
        _requires_iai_version("1.1.0", "OptimalFeatureSelectionRegressor")
        jl_obj = _IAI.OptimalFeatureSelectionRegressor_convert(*args, **kwargs)
        super().__init__(jl_obj)
