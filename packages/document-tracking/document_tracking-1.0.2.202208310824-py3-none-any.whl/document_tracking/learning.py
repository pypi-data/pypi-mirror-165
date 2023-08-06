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
from collections import defaultdict
from typing import Dict, List

from document_tracking_resources.corpus import Corpus
from document_tracking_resources.documents import Document
from pandas import DataFrame, Series
from tqdm import tqdm

from document_tracking.miranda.clustering import StreamingAggregator
from document_tracking.third_party import get_similarity_between_document_and_cluster


class AggregatorWithTrueLabelsMixin(StreamingAggregator, abc.ABC):
    """
    A StreamingAggregator with perfectly clusters documents using existing ground truth. It is used to collect
    similarities of a perfect clustering in order to train models or analyse the similarities.
    """

    @property
    def aggregated_cluster_similarities(self) -> DataFrame:
        aggregated_results = DataFrame(self._all_document_cluster_similarities)
        aggregated_results = aggregated_results.fillna(0.0)
        aggregated_results = aggregated_results.set_index(["document", "cluster"])
        return aggregated_results

    def __init__(self, corpus: Corpus, true_labels: Series, number_of_days_window: float = 3.0):
        super().__init__(corpus, model=None, threshold=None, number_of_days_window=number_of_days_window)
        self._clusters: Dict[int, AggregatorWithTrueLabelsMixin.CLUSTER_CLASS] = defaultdict()
        self._true_labels: Series = true_labels
        self._all_document_cluster_similarities: List[Dict[str, float]] = []

    def process_document_with_true_label(self, document: Document, document_true_cluster_id: int):
        # start a new cluster
        if document_true_cluster_id not in self._clusters.keys():
            # pylint: disable=not-callable
            self._clusters[document_true_cluster_id] = self.CLUSTER_CLASS(document)
        else:
            # a cluster already exists for this document
            for cluster_id, cluster in self._clusters.items():
                similarity_document_cluster = get_similarity_between_document_and_cluster(
                    document, cluster, self.number_of_days_window, self.SIMILARITY_CLASS
                )
                similarity_document_cluster["document"] = document.id
                similarity_document_cluster["cluster"] = cluster_id
                similarity_document_cluster["same_cluster"] = document_cluster_should_be_together = (
                    cluster_id == self._true_labels.loc[document.id]
                )
                self._all_document_cluster_similarities.append(similarity_document_cluster)

                if document_cluster_should_be_together:
                    cluster.add_document_into_cluster(document)

    def cluster_corpus(self):
        for document_index in tqdm(self._corpus.documents.index, desc="Aggregating corpus"):
            # pylint: disable=not-callable
            self.process_document_with_true_label(
                self.DOCUMENT_CLASS(
                    self._corpus.documents.loc[document_index],
                    self._corpus.features.loc[document_index],
                ),
                self._corpus.labels.loc[document_index],
            )
