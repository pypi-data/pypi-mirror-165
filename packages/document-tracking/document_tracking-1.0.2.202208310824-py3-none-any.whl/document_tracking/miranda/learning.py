#
# This file is part of the learning package for Miranda algorithm.

# Copyright (c) 2021 − Present Guillaume Bernard <contact@guillaume-bernard.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from typing import Tuple

import numpy as np
from document_tracking.learning import AggregatorWithTrueLabelsMixin
from document_tracking.miranda.clustering import AggregatorOfDenseCorpus, AggregatorOfSparseCorpus
from document_tracking_resources.documents import DocumentWithSparseFeatures
from pandas import DataFrame
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from tqdm import tqdm


class AggregatorOfSparseCorpusWithTrueLabels(AggregatorOfSparseCorpus, AggregatorWithTrueLabelsMixin):
    def process_document(self, document: DocumentWithSparseFeatures):
        raise NotImplementedError("This aggregator clusters documents with knowledge of their true labels.")


class AggregatorOfDenseCorpusWithTrueLabels(AggregatorOfDenseCorpus, AggregatorWithTrueLabelsMixin):
    def process_document(self, document: DocumentWithSparseFeatures):
        raise NotImplementedError("This aggregator clusters documents with knowledge of their true labels.")


def __sum_all_features_to_a_new_column(similarities: DataFrame) -> DataFrame:
    """
    Sum all the features (all columns starting with f_) in a new column, sum.
    """
    columns_to_sum = [feature_name for feature_name in similarities.columns if feature_name.startswith("f_")]
    similarities["sum"] = similarities[columns_to_sum].sum(axis=1)
    return similarities


def subsample_dataset_by_reducing_number_of_negative_samples(similarities: DataFrame) -> DataFrame:
    """
    From the input dataset, reduce the number of negative examples. We rank negative examples by descending sum of
    all features. We keep only 20 of them.
    """
    similarities_with_sum = __sum_all_features_to_a_new_column(similarities)

    indexes_to_keep = []
    for _, group in tqdm(similarities_with_sum.groupby("document"), desc="Subsampling similarities"):
        indexes_to_keep.extend(group[group.same_cluster].sort_values("sum", ascending=False).index.to_list())
        indexes_to_keep.extend(
            group[~group.same_cluster]
            .sort_values("sum", ascending=False)
            .iloc[
                :20,
            ]
            .index.to_list()
        )

    similarities_without_sum = similarities_with_sum.drop("sum", axis=1)
    return similarities_without_sum[similarities_without_sum.index.isin(indexes_to_keep)]


def grid_search_logistic_regression_from_similarities(
    similarities: DataFrame, random_state: int = 0
) -> Tuple[LogisticRegression, DataFrame, DataFrame]:
    """
    Perform a Grid Search with a LogisticRegression with the similarities' dataset, get the best estimator.
    """

    # Class distribution is unbalanced: 5% of True, 95% of False (due to subsampling)
    train, test = train_test_split(similarities, random_state=random_state, stratify=similarities["same_cluster"])
    x_train, y_train = train.drop(["same_cluster"], axis=1), train["same_cluster"]
    x_test, y_test = test.drop(["same_cluster"], axis=1), test["same_cluster"]

    grid_parameters = {
        "C": np.arange(1, 25, step=5),
        "penalty": ["l2", "l1", "elasticnet"],
        "solver": ["newton-cg", "lbfgs", "liblinear", "sag", "saga"],
        "class_weight": ["balanced"],
    }

    grid = GridSearchCV(
        LogisticRegression(random_state=random_state), param_grid=grid_parameters, verbose=2, scoring="f1_macro"
    )
    grid.fit(x_train, y_train)

    return grid.best_estimator_, x_test, y_test
