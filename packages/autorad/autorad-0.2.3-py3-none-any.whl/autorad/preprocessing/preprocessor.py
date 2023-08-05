from __future__ import annotations

import dataclasses
import logging

import pandas as pd
from imblearn.over_sampling import ADASYN, SMOTE, BorderlineSMOTE
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from autorad.config import config
from autorad.data.dataset import TrainingData, TrainingInput, TrainingLabels
from autorad.feature_selection.selector import create_feature_selector

log = logging.getLogger(__name__)


def get_not_none_kwargs(**kwargs):
    return {k: v for k, v in kwargs.items() if v is not None}


class Preprocessor:
    def __init__(
        self,
        normalize: bool = True,
        feature_selection_method: str | None = None,
        n_features: int | None = None,
        oversampling_method: str | None = None,
        random_state: int = config.SEED,
    ):
        """Performs preprocessing, including:
        1. normalization
        2. feature selection
        3. oversampling

        Args:
            normalize: whether to normalize to range (0, 1)
            feature_selection_method: algorithm to select key features,
                if None, select all features
            n_features: number of features to select, only applicable to selected
                feature selection methods (see feature_selection.selector)
            oversampling_method: minority class oversampling method,
                if None, no oversampling
            random_state: seed
        """
        self.normalize = normalize
        self.feature_selection_method = feature_selection_method
        self.n_features = n_features
        self.oversampling_method = oversampling_method
        self.random_state = random_state
        self.pipeline = self._build_pipeline()
        self.selected_features = None

    def transform(self, X: pd.DataFrame):
        result_array = self.pipeline.transform(X)
        result_df = pd.DataFrame(result_array, columns=self.selected_features)
        return result_df

    def fit_transform(self, data: TrainingData):
        # copy data
        _data = dataclasses.replace(data)
        X, y = _data.X, _data.y
        result_X = {}
        result_y = {}
        all_features = X.train.columns.tolist()
        X_train_trans, y_train_trans = self.pipeline.fit_transform(
            X.train, y.train
        )
        self.selected_features = self.pipeline["select"].selected_features(
            column_names=all_features
        )
        result_X["train"] = pd.DataFrame(
            X_train_trans, columns=self.selected_features
        )
        result_y["train"] = pd.Series(y_train_trans)
        X_test_trans = self.pipeline.transform(X.test)
        result_X["test"] = pd.DataFrame(
            X_test_trans, columns=self.selected_features
        )
        result_y["test"] = y.test
        if X.val is not None:
            X_val_trans = self.pipeline.transform(X.val)
            result_X["val"] = pd.DataFrame(
                X_val_trans, columns=self.selected_features
            )
            result_y["val"] = y.val
        if X.train_folds is not None and X.val_folds is not None:
            (
                result_X["train_folds"],
                result_y["train_folds"],
                result_X["val_folds"],
                result_y["val_folds"],
            ) = self._fit_transform_cv_folds(_data)
        _data._X_preprocessed = TrainingInput(**result_X)
        _data._y_preprocessed = TrainingLabels(**result_y)
        return _data

    def _fit_transform_cv_folds(
        self, data: TrainingData
    ) -> tuple[
        list[pd.DataFrame],
        list[pd.Series],
        list[pd.DataFrame],
        list[pd.Series],
    ]:
        if (
            data.X.train_folds is None
            or data.y.train_folds is None
            or data.X.val_folds is None
            or data.y.val_folds is None
        ):
            raise AttributeError("Folds are not set")
        (
            result_X_train_folds,
            result_y_train_folds,
            result_X_val_folds,
            result_y_val_folds,
        ) = ([], [], [], [])
        for X_train, y_train, X_val in zip(
            data.X.train_folds,
            data.y.train_folds,
            data.X.val_folds,
        ):
            cv_pipeline = self._build_pipeline()
            all_features = X_train.columns.tolist()
            result_X_train, result_y_train = cv_pipeline.fit_transform(
                X_train, y_train
            )
            selected_features = cv_pipeline["select"].selected_features(
                column_names=all_features
            )
            result_X_val = cv_pipeline.transform(X_val)
            result_df_X_train = pd.DataFrame(
                result_X_train, columns=selected_features
            )
            result_df_X_val = pd.DataFrame(
                result_X_val, columns=selected_features
            )
            result_X_train_folds.append(result_df_X_train)
            result_y_train_folds.append(pd.Series(result_y_train))
            result_X_val_folds.append(result_df_X_val)
        result_y_val_folds = data.y.val_folds
        return (
            result_X_train_folds,
            result_y_train_folds,
            result_X_val_folds,
            result_y_val_folds,
        )

    def _build_pipeline(self):
        steps = []
        if self.normalize:
            steps.append(("normalize", MinMaxWrapper()))
        if self.feature_selection_method is not None:
            steps.append(
                (
                    "select",
                    create_feature_selector(
                        method=self.feature_selection_method,
                        **get_not_none_kwargs(n_features=self.n_features),
                    ),
                )
            )
        if self.oversampling_method is not None:
            steps.append(
                (
                    "balance",
                    create_oversampling_model(
                        method=self.oversampling_method,
                        random_state=self.random_state,
                    ),
                )
            )
        pipeline = Pipeline(steps)
        return pipeline


def create_oversampling_model(method: str, random_state: int = config.SEED):
    if method is None:
        return None
    if method == "ADASYN":
        return ADASYNWrapper(random_state=random_state)
    elif method == "SMOTE":
        return SMOTEWrapper(random_state=random_state)
    elif method == "BorderlineSMOTE":
        return BorderlineSMOTEWrapper(
            random_state=random_state, kind="borderline1"
        )
    raise ValueError(f"Unknown oversampling method: {method}")


class MinMaxWrapper(MinMaxScaler):
    def fit_transform(self, X, y=None):
        self.fit(X)
        return self.transform(X, y)

    def transform(self, X, y=None):
        return super().transform(X)


class ADASYNWrapper(ADASYN):
    def __init__(self, random_state=config.SEED):
        super().__init__(random_state=random_state)

    def fit_transform(self, data, *args):
        return super().fit_resample(*data)

    def transform(self, X):
        log.debug("ADASYN does nothing on .transform()...")
        return X


class SMOTEWrapper(SMOTE):
    def __init__(self, random_state=config.SEED):
        super().__init__(random_state=random_state)

    def fit_transform(self, data, *args):
        return super().fit_resample(*data)

    def transform(self, X):
        log.debug("SMOTE does nothing on .transform()...")
        return X


class BorderlineSMOTEWrapper(BorderlineSMOTE):
    def __init__(self, kind="borderline-1", random_state=config.SEED):
        super().__init__(kind=kind, random_state=random_state)

    def fit_transform(self, data, *args):
        return super().fit_resample(*data)

    def transform(self, X):
        log.debug("BorderlineSMOTE does nothing on .transform()...")
        return X
