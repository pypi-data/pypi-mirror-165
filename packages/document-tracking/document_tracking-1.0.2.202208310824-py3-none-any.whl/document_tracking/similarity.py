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

import math
from abc import ABC
from typing import Dict

from document_tracking_resources.documents import DenseFeatures, Features, SparseFeatures
from sentence_transformers.util import cos_sim


class SimilarityBetweenFeatures(ABC):
    """
    Compute the similarity between two features. The implementation (whether cosine similarity, adapted to the Features
    themselves is an implementation detail provided by its subclasses.
    """

    @staticmethod
    def similarity(first_document_features: Features, second_document_features: Features) -> Dict[str, float]:
        """
        Get the similarity, for each dimension of the Features (‘keys’, for instance f_entities_all, f_entities_text)
        and associate, for each dimension, the similarity between the two features givens in parameter.
        :return: the similarities between each feature of both documents
        """
        raise NotImplementedError()


class SimilaritySparseFeatures(SimilarityBetweenFeatures):
    @staticmethod
    def similarity(
        first_document_features: SparseFeatures, second_document_features: SparseFeatures
    ) -> Dict[str, float]:
        cosine_bag_of_features_vector: Dict[str, float] = {}
        for feature_name, first_document_feature_vector in first_document_features.items():
            if feature_name in second_document_features:
                second_document_feature_vector = second_document_features.get(feature_name)
                cosine_bag_of_features_vector[
                    feature_name
                ] = SimilaritySparseFeatures.__get_cosine_similarity_between_two_features(
                    first_document_feature_vector, second_document_feature_vector
                )
        return cosine_bag_of_features_vector

    @staticmethod
    def __get_cosine_similarity_between_two_features(
        first_feature: Dict[str, float], second_feature: Dict[str, float]
    ) -> float:
        """
        Get the cosine similarity between two sparse features. Both features are dictionaries, with, a
        s the key the name of the n-grams and the weight value associated with it. For instance, we can have:

        first_feature: {"paris": 0.65456, "eiffel": 0.5694}
        second_feature: {"paris": 0.943, "montparnasse": 0.6964}

        The cosine similarity will have to take into account the n-grams "eiffel" and "montparnasse" do not exist
        in both vector, and as such should consider getting the dot product of these values with 0.
        """
        return SimilaritySparseFeatures.dot_product_of_sparse_vectors(first_feature, second_feature) / math.sqrt(
            SimilaritySparseFeatures.dot_product_of_sparse_vectors(first_feature, first_feature)
            * SimilaritySparseFeatures.dot_product_of_sparse_vectors(second_feature, second_feature)
        )

    @staticmethod
    def dot_product_of_sparse_vectors(
        first_sparse_feature: Dict[str, float], second_sparse_feature: Dict[str, float]
    ) -> float:
        dot_product = 0.0
        for first_feature_id, first_feature_value in first_sparse_feature.items():
            if first_feature_id in second_sparse_feature:
                second_feature_value = second_sparse_feature.get(first_feature_id)
                dot_product += first_feature_value * second_feature_value
        return dot_product


class SimilarityDenseFeatures(SimilarityBetweenFeatures):
    @staticmethod
    def similarity(
        first_document_features: DenseFeatures, second_document_features: DenseFeatures
    ) -> Dict[str, float]:
        cosine_bag_of_features_vector: Dict[str, float] = {}
        for feature_name, first_document_feature_vector in first_document_features.items():
            if feature_name in second_document_features:
                second_document_feature_vector = second_document_features.get(feature_name)
                cosine_bag_of_features_vector[feature_name] = cos_sim(
                    first_document_feature_vector, second_document_feature_vector
                )
        return cosine_bag_of_features_vector
