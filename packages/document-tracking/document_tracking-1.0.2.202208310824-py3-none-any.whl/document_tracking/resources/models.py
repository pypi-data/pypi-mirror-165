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

import json
import math
from typing import Dict, Tuple

from document_tracking.similarity import SimilaritySparseFeatures


class ScoringModel:
    """
    The model that is used to compute a similarity score from bags of features. This is a model that computes
    a score by getting the dot product between the input bag of features and the model weights.
    """

    def __init__(self, weights: Dict[str, float], intercept: float):
        self.weights = weights
        self.intercept = intercept

    def score(self, bag_of_features: Dict[str, float]) -> float:
        return self.intercept + SimilaritySparseFeatures.dot_product_of_sparse_vectors(bag_of_features, self.weights)

    def __str__(self) -> str:
        return json.dumps(self.weights)

    @staticmethod
    def _load_data_from_json_file(path_to_json_file: str) -> Tuple[Dict[str, float], float]:
        with open(path_to_json_file, mode="r", encoding="utf-8") as input_file:
            json_document = json.load(input_file)
            weights = {key: value for key, value in json_document.items() if key.startswith("f_")}
            intercept = json_document.get("intercept", 0)
            return weights, intercept

    @classmethod
    def from_json_file(cls, path_to_json_file: str) -> "ScoringModel":
        return ScoringModel(*cls._load_data_from_json_file(path_to_json_file))


class LogisticModel(ScoringModel):
    """
    Model that is similar to a Logistic Regressor, which applies the sigmoid function on computed similarity.
    """

    def score(self, bag_of_features: Dict[str, float]) -> float:
        return self.__sigmoid(ScoringModel.score(self, bag_of_features))

    @staticmethod
    def __sigmoid(x: float) -> float:
        if x >= 0:
            z = math.exp(-x)
            sig = 1 / (1 + z)
            return sig
        z = math.exp(x)
        sig = z / (1 + z)
        return sig

    @classmethod
    def from_json_file(cls, path_to_json_file: str):
        return LogisticModel(*ScoringModel._load_data_from_json_file(path_to_json_file))
