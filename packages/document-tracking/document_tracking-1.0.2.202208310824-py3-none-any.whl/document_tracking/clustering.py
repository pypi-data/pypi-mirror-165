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

import abc
from functools import cached_property
from typing import List

import numpy
from document_tracking_resources.corpus import Corpus
from document_tracking_resources.documents import (
    DenseFeatures,
    Document,
    DocumentWithDenseFeatures,
    DocumentWithSparseFeatures,
    SparseFeatures,
)
from pandas import DataFrame, Series, concat

from document_tracking.evaluation import ClusteringScores
from document_tracking.third_party import Cluster


class Aggregator(abc.ABC):

    SIMILARITY_CLASS = None

    @property
    def clusters(self) -> Series:
        return Series(
            {self._corpus.index[document_id]: cluster_id for document_id, cluster_id in enumerate(self._clusters)},
            name="clusters",
        )

    @property
    def nb_clusters(self) -> int:
        return len(self._clusters)

    @property
    def time_spent_in_seconds(self) -> float:
        raise NotImplementedError

    def __init__(self, corpus: Corpus):
        """
        :raises ValueError when the corpus is empty
        """
        if len(corpus) <= 0:
            raise ValueError("The corpus is empty: no document inside this corpus.")

        self._corpus = corpus
        self._clusters = []

    @abc.abstractmethod
    def process_document(self, document: Document):
        """
        Process and cluster a unique document.
        """

    @abc.abstractmethod
    def cluster_corpus(self):
        """
        Cluster the corpus given to the Aggregator.
        """

    @cached_property
    def clustering_scores(self) -> Series:
        """
        TODO: this function should move to a Visitor that is in charge of displaying or collecting the results.
        """
        clustering_scores_table = ClusteringScores(self._corpus.labels, self.clusters).get_scores()
        clustering_scores_table.name = (
            f"{self._corpus.documents.date.min().strftime('%Y-%m-%d')}"
            f" - {self._corpus.documents.date.max().strftime('%Y-%m-%d')}"
        )
        clustering_scores_table["time_in_seconds"] = self.time_spent_in_seconds
        clustering_scores_table["nb_documents"] = len(self._corpus)
        return clustering_scores_table

    @staticmethod
    def summarize_clustering_scores(clustering_scores: List[Series]) -> DataFrame:
        """
        TODO: this function should move to a Visitor that is in charge of displaying or collecting the results.
        """
        results_df = concat(clustering_scores, axis=1).T
        results_df_final = (
            results_df[["f1", "precision", "recall", "f1_bcubed", "precision_bcubed", "recall_bcubed"]]
            .mean()
            .to_frame()
            .T
        )
        results_df_final["number_labels_predicted"] = results_df["number_labels_predicted"].sum()
        results_df_final["time_in_seconds"] = results_df["time_in_seconds"].sum()
        return results_df_final.round(3)


class ClusterOfDocumentWithSparseFeatures(Cluster):

    DOCUMENT_CLASS = DocumentWithSparseFeatures

    def _add_document_features_into_cluster(self, features: SparseFeatures):
        for feature_name, feature_vector_to_add in features.items():
            if feature_name in self.features:
                for word, word_tf_idf_weight in feature_vector_to_add.items():
                    if word in self.features[feature_name]:
                        self.features[feature_name][word] += word_tf_idf_weight
                    else:
                        self.features[feature_name][word] = word_tf_idf_weight
            else:
                self.features[feature_name] = feature_vector_to_add


class ClusterOfDocumentWithDenseFeatures(Cluster):

    DOCUMENT_CLASS = DocumentWithDenseFeatures

    def _add_document_features_into_cluster(self, features: DenseFeatures):
        for feature_name, feature_vector_to_add in features.items():
            if feature_name in self.features:
                current_cluster_logits_on_that_feature = self.features.get(feature_name)
                logits_to_add_on_that_feature = features.get(feature_name)
                self.features[feature_name] = numpy.mean(
                    [current_cluster_logits_on_that_feature, logits_to_add_on_that_feature], axis=0
                )
            else:
                self.features[feature_name] = feature_vector_to_add
