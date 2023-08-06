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
# WARNING: some parts of this file originally come from the Priberam source code published on Github at:
# https://archive.softwareheritage.org/swh:1:dir:2b5a159195789c76ecb01692b70bdd3a9e63dbf2
# and the parts mentioned below where first published under the ‘The 3-Clause BSD License’ distributed in this
# repository, for Priberam Clustering Software Copyright 2018 by PRIBERAM INFORMÁTICA, S.A. ("PRIBERAM")
# (www.priberam.com). Their modifications are released under the same conditions.
# These parts are:
# - the `Aggregator.process_document() function, its logic and behaviour.


import time
from abc import ABC
from typing import Type

from document_tracking.clustering import (
    Aggregator,
    ClusterOfDocumentWithDenseFeatures,
    ClusterOfDocumentWithSparseFeatures,
)
from document_tracking.third_party import Cluster, process_document
from document_tracking.resources.models import ScoringModel
from document_tracking.similarity import SimilarityBetweenFeatures, SimilarityDenseFeatures, SimilaritySparseFeatures
from document_tracking_resources.corpus import Corpus
from document_tracking_resources.documents import Document, DocumentWithDenseFeatures, DocumentWithSparseFeatures
from pandas import Series
from tqdm import tqdm


class StreamingAggregator(Aggregator, ABC):
    DOCUMENT_CLASS: Type[Document] = None
    CLUSTER_CLASS: Type[Cluster] = None
    SIMILARITY_CLASS: Type[SimilarityBetweenFeatures] = None

    @property
    def time_spent_in_seconds(self) -> float:
        return self.time_elapsed_for_clustering.sum()

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        corpus: Corpus,
        model: ScoringModel,
        threshold: float,
        merge_model: ScoringModel = None,
        number_of_days_window: float = 3.0,
    ):
        super().__init__(corpus)
        self.model = model
        self.merge_model = merge_model
        self.threshold = threshold
        self.number_of_days_window = number_of_days_window
        self.time_elapsed_for_clustering = Series(index=corpus.index, name="time_elapsed")

    def cluster_corpus(self):
        """
        Aggregate the whole corpus into cluster of significant stories.
        """
        progress_bar = tqdm(self._corpus.documents.index, desc="Clustering corpus")
        for index, document in enumerate(progress_bar):
            # Keep track of time to process each document
            start = time.process_time()
            # pylint: disable=not-callable
            self.process_document(
                self.DOCUMENT_CLASS(self._corpus.documents.loc[document], self._corpus.features.loc[document])
            )
            progress_bar.set_description(desc=f"Clustering corpus ({self.nb_clusters} clusters)", refresh=True)
            self.time_elapsed_for_clustering.iat[index] = time.process_time() - start

    def get_clustering_results(self) -> Series:
        return Series(
            {
                document_id: cluster_id
                for cluster_id, cluster in enumerate(self.clusters)
                for document_id in cluster.document_ids
            },
            name="clusters",
        ).sort_index()

    def process_document(self, document: "DOCUMENT_CLASS"):
        self._clusters = process_document(
            self._clusters,
            self.number_of_days_window,
            self.SIMILARITY_CLASS,
            self.model,
            self.threshold,
            self.merge_model,
            self.CLUSTER_CLASS,
            document
        )


class AggregatorOfSparseCorpus(StreamingAggregator):
    DOCUMENT_CLASS = DocumentWithSparseFeatures
    CLUSTER_CLASS = ClusterOfDocumentWithSparseFeatures
    SIMILARITY_CLASS = SimilaritySparseFeatures


class AggregatorOfDenseCorpus(StreamingAggregator):
    DOCUMENT_CLASS = DocumentWithDenseFeatures
    CLUSTER_CLASS = ClusterOfDocumentWithDenseFeatures
    SIMILARITY_CLASS = SimilarityDenseFeatures
