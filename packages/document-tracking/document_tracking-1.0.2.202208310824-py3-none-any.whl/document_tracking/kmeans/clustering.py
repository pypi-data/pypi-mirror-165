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
import time
from abc import ABC
from enum import Enum
from functools import lru_cache
from typing import Dict, List, Set

import numpy
from document_tracking import logger
from document_tracking.clustering import Aggregator
from document_tracking_resources.corpus import Corpus
from document_tracking_resources.documents import Document
from pandas import DataFrame, Series
from scipy.sparse import csr_matrix, hstack
from sklearn.cluster import KMeans
from sklearn.preprocessing import Normalizer
from yellowbrick.cluster import KElbowVisualizer


class KMeansMetric(Enum):

    ELBOW = ("elbow", 1, "distortion")
    SILHOUETTE = ("silhouette", 2, "silhouette")
    GOLD = ("gold", 1, "gold")

    def __init__(self, name: str, minimal_number_of_clusters: int, kmeans_visualizer_metric: str):
        self.method_name = name
        self.minimal_number_of_clusters = minimal_number_of_clusters
        self.kmeans_visualizer_metric = kmeans_visualizer_metric


class KMeansAggregator(Aggregator, ABC):
    @property
    def time_spent_in_seconds(self) -> float:
        return self._time_spent

    def process_document(self, document: Document):
        raise NotImplementedError("Bucket Aggregator does not process documents individually.")

    def __init__(self, corpus: Corpus, metric: KMeansMetric, *kmeans_args, **kmeans_kwargs):
        super().__init__(corpus)
        self._metric = metric
        self._kmeans_args = kmeans_args
        self._kmeans_kwargs = kmeans_kwargs
        self._kmeans_kwargs.update({"random_state": 0})
        self._time_spent = 0.0

    @lru_cache(maxsize=None)
    @abc.abstractmethod
    def _matrix_of_features(self):
        pass

    def __optimal_number_of_clusters_according_to_elbow_method(self) -> int:
        optimal_number_of_clusters = 1
        half_corpus_length = len(self._corpus) // 2
        step = len(self._corpus) // max(25, min(150, half_corpus_length)) or 1
        values_of_k = list(range(self._metric.minimal_number_of_clusters, half_corpus_length, step))
        if len(values_of_k) > 2:
            kmeans = KMeans(**self._kmeans_kwargs)
            visualiser = KElbowVisualizer(kmeans, k=values_of_k, metric=self._metric.kmeans_visualizer_metric)
            visualiser.fit(self._matrix_of_features())
            # This is a very strong assumption, in case there is no elbow, KMeans could be unable to cluster the data
            # and we consider (which can be untrue) that there is no cluster at all.
            optimal_number_of_clusters = visualiser.elbow_value_ or 1
        return optimal_number_of_clusters

    def cluster_corpus(self):
        start_time = time.process_time()
        if not self._metric == KMeansMetric.GOLD:
            k = self.__optimal_number_of_clusters_according_to_elbow_method()
        else:
            k = self._corpus.nb_unique_gold_clusters
        logger.info(
            "Clustering %s with %d clusters; %d real.",
            self._corpus,
            k,
            self._corpus.nb_unique_gold_clusters,
        )
        kmeans = KMeans(n_clusters=k, **self._kmeans_kwargs)
        kmeans.fit(self._matrix_of_features())
        self._time_spent = time.process_time() - start_time
        self._clusters = kmeans.labels_.tolist()

    @staticmethod
    def merge_multiple_non_overlapping_clustering_results(
        clustering_results: List[Series],
    ) -> Series:
        clusters, current_cluster_id = Series(), 0
        for clustering_result in clustering_results:
            clustering_result += current_cluster_id
            current_cluster_id = clustering_result.max() + 1
            clusters = clusters.append(clustering_result)
        return clusters.sort_index()


class KMeansAggregatorOfSparseCorpus(KMeansAggregator):
    @lru_cache(maxsize=None)
    def __collect_corpus_vocabulary(self) -> Dict[str, Set[str]]:
        vocabularies = {}

        for feature in self._corpus.features.columns:
            vocabulary = set()
            for item in self._corpus.features[feature].items():
                item_weights = item[1]
                if item_weights is not None:
                    vocabulary.update(item_weights.keys())
            vocabularies[feature] = vocabulary

        return vocabularies

    @lru_cache(maxsize=None)
    def _matrix_of_features(self) -> csr_matrix:
        vocabularies = self.__collect_corpus_vocabulary()

        matrices = []
        for feature_name in self._corpus.features.columns:
            df = DataFrame(index=self._corpus.index, columns=vocabularies.get(feature_name))

            for item_id, item_weights in self._corpus.features[feature_name].items():
                if item_weights is not None:
                    current_series = Series(item_weights).reindex(vocabularies.get(feature_name))
                    df.at[item_id] = current_series

            matrices.append(csr_matrix(df.astype(float).fillna(0)))

        return Normalizer().fit_transform(hstack(matrices, format="csr"))


class KMeansAggregatorOfDenseCorpus(KMeansAggregator):
    @lru_cache(maxsize=None)
    def _matrix_of_features(self):
        return Normalizer().fit_transform(
            numpy.array(
                [
                    document_features.tolist()
                    for document_id, document_features in self._corpus.features.sum(axis=1).items()
                ]
            )
        )
