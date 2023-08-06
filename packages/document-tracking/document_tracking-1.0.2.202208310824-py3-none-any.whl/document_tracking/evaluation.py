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

from functools import cached_property
from typing import Any, Dict, Tuple

import bcubed
from pandas import Series
from sklearn.metrics import (
    adjusted_mutual_info_score,
    adjusted_rand_score,
    homogeneity_completeness_v_measure,
    normalized_mutual_info_score,
    pair_confusion_matrix,
    rand_score,
)


class ClusteringScores:
    """
    Evaluate one clustering output compared to a ground truth in order to evaluate clustering algorithms.
    This provides access to standard metrics as well as BCube analysis which is another suitable metrics for
    clustering.

    .. seealso::
        Amigó, Enrique, Julio Gonzalo, Javier Artiles and M. Felisa Verdejo. “A comparison of extrinsic clustering
        evaluation metrics based on formal constraints.” Information Retrieval 12 (2009): 613.
        https://dl.acm.org/doi/abs/10.1007/s10791-008-9066-8
    """

    # pylint: disable=too-many-instance-attributes

    @cached_property
    def f1(self) -> float:
        return (
            2.0 * self.precision * self.recall / (self.precision + self.recall)
            if self.precision + self.recall > 0
            else 0
        )

    @cached_property
    def precision(self) -> float:
        return (
            1.0 * self.true_positive / (self.true_positive + self.false_positive)
            if self.true_positive + self.false_positive > 0
            else 0
        )

    @cached_property
    def recall(self) -> float:
        return (
            1.0 * self.true_positive / (self.true_positive + self.false_negative)
            if self.true_positive + self.false_negative > 0
            else 0
        )

    @cached_property
    def accuracy(self) -> float:
        return (
            1.0
            * (self.true_positive + self.true_negative)
            / (self.true_positive + self.true_negative + self.false_positive + self.false_negative)
            if self.true_positive + self.true_negative + self.false_positive + self.false_negative > 0
            else 0
        )

    @cached_property
    def rand_score(self) -> float:
        return rand_score(self.true_labels, self.predicted_labels)

    @cached_property
    def adjusted_rand_score(self) -> float:
        return adjusted_rand_score(self.true_labels, self.predicted_labels)

    @cached_property
    def normalized_mutual_info_score(self) -> float:
        return normalized_mutual_info_score(self.true_labels, self.predicted_labels)

    @cached_property
    def adjusted_mutual_info_score(self) -> float:
        return adjusted_mutual_info_score(self.true_labels, self.predicted_labels)

    @cached_property
    def homogeneity_completeness_v_measure(self) -> Tuple[float, float, float]:
        return homogeneity_completeness_v_measure(self.true_labels, self.predicted_labels)

    @cached_property
    def number_of_true_labels(self):
        return len(set(self.true_labels))

    @cached_property
    def number_of_predicted_labels(self):
        return len(set(self.predicted_labels))

    @cached_property
    def b_cubed_precision(self):
        return bcubed.precision(self.b_cubed_predicted, self.b_cubed_gold)

    @cached_property
    def b_cubed_recall(self):
        return bcubed.recall(self.b_cubed_predicted, self.b_cubed_gold)

    @cached_property
    def b_cubed_f1(self):
        return bcubed.fscore(self.b_cubed_precision, self.b_cubed_recall)

    def __init__(self, true_labels: Series, predicted_labels: Series):
        """
        :raises ValueError when both label series have different lengths.
        """
        if len(true_labels) != len(predicted_labels):
            raise ValueError("Series of labels (both predicted and true ones) should be equal in length.")

        self.true_labels, self.predicted_labels = (
            true_labels.sort_index().tolist(),
            predicted_labels.sort_index().tolist(),
        )

        confusion_matrix = pair_confusion_matrix(self.true_labels, self.predicted_labels)
        self.true_negative, self.true_positive = confusion_matrix[0, 0], confusion_matrix[1, 1]
        self.false_negative, self.false_positive = confusion_matrix[1, 0], confusion_matrix[0, 1]

        self.b_cubed_gold = self.__get_b_cubed_clustering_dict(true_labels)
        self.b_cubed_predicted = self.__get_b_cubed_clustering_dict(predicted_labels)

    @staticmethod
    def __get_b_cubed_clustering_dict(labels: Series):
        return {int(document_id): {cluster_id} for document_id, cluster_id in labels.to_dict().items()}

    def get_clustering_scores_dict(self) -> Dict[str, Any]:
        """
        TODO: this function should move to a Visitor that is in charge of displaying the results.
        """
        return {
            "metrics": {
                "standard": {"f1": self.f1, "precision": self.precision, "recall": self.recall},
                "bcubed": {
                    "f1": self.b_cubed_f1,
                    "precision": self.b_cubed_precision,
                    "recall": self.b_cubed_recall,
                },
                "accuracy": self.accuracy,
                "rand_index": self.rand_score,
                "adjusted_rand_score": self.adjusted_rand_score,
                "normalized_mutual_info_score": self.normalized_mutual_info_score,
                "adjusted_mutual_info_score": self.adjusted_mutual_info_score,
                "homogeneity_completeness_v_measure": self.homogeneity_completeness_v_measure,
            },
            "classification": {
                "tp": self.true_positive,
                "tn": self.true_negative,
                "fp": self.false_positive,
                "fn": self.false_negative,
            },
            "number_labels_true": self.number_of_true_labels,
            "number_labels_predicted": self.number_of_predicted_labels,
        }

    def get_scores(self) -> Series:
        """
        TODO: this function should move to a Visitor that is in charge of displaying the results.
        """
        data = {
            "F1": self.f1,
            "Precision": self.precision,
            "Recall": self.recall,
            "F1 B3": self.b_cubed_f1,
            "Precision B3": self.b_cubed_precision,
            "Recall B3": self.b_cubed_recall,
            "Real nb. clusters": self.number_of_true_labels,
            "Predicted nb. clusters": self.number_of_predicted_labels,
            "Support": len(self.true_labels),
        }
        return Series(data, name="scores").round(3)
