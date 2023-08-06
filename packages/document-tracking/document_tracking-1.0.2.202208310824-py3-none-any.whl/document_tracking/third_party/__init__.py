# The 3-Clause BSD License
#
# For Priberam Clustering Software Copyright 2018 by PRIBERAM INFORMÁTICA, S.A. ("PRIBERAM") (www.priberam.com)
# Additions, cleaning, documentation by Guillaume Bernard <contact@guillaume-bernard.fr>, 2021 − Present
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
# disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder (PRIBERAM) nor the names of its contributors may be used to endorse or
# promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import abc
import math
from datetime import datetime, timezone
from statistics import mean
from typing import Type, Dict, Set, List

from document_tracking.resources.models import ScoringModel
from document_tracking.similarity import SimilarityBetweenFeatures
from document_tracking_resources.documents import Document, Features


def get_similarity_between_document_and_cluster(
    document: Document,
    cluster: "Cluster",
    number_of_days_window: float,
    similarity_class: Type[SimilarityBetweenFeatures],
):
    bag_of_features = similarity_class.similarity(document.features, cluster.features)
    bag_of_features = add_time_similarities_into_the_bag_of_features(
        bag_of_features, document, cluster, number_of_days_window
    )
    bag_of_features = add_cluster_size_similarity_into_the_bag_of_features(bag_of_features, cluster)
    return bag_of_features


def add_time_similarities_into_the_bag_of_features(
    bag_of_features: Dict[str, float], document: "Document", cluster: "Cluster", number_of_days_window: float
):
    bag_of_features["f_newest_ts"] = get_similarity_between_two_timestamps(
        document.timestamp.timestamp(),
        cluster.lowest_timestamp.timestamp(),
        number_of_days_window,
    )
    bag_of_features["f_oldest_ts"] = get_similarity_between_two_timestamps(
        document.timestamp.timestamp(),
        cluster.highest_timestamp.timestamp(),
        number_of_days_window,
    )
    return bag_of_features


def add_cluster_size_similarity_into_the_bag_of_features(bag_of_features: Dict[str, float], cluster: "Cluster"):
    bag_of_features["f_zzinvcluster_size"] = 1.0 / float(
        100 if cluster.number_of_documents > 100 else cluster.number_of_documents
    )
    return bag_of_features


def get_similarity_between_two_timestamps(
    first_timestamp: float, second_timestamp: float, number_of_days_window: float
) -> float:
    """
    Get the similarity between two dates, depending on the number of days. This relies on the Gaussian curve. If there
    is only a little difference between the two timestamps, the similarity score will be higher. Otherwise, this will
    decrease according to the Gaussian curve.

    See the `timestamp_similarity` Jupyter notebook in the `docs` directory.
    """
    number_of_seconds_in_a_day = 60 * 60 * 24
    number_of_days_between_two_timestamp = (first_timestamp - second_timestamp) / number_of_seconds_in_a_day
    return __gaussian_function(0, number_of_days_window, number_of_days_between_two_timestamp)


def __gaussian_function(root_mean_square: float, standard_deviation: float, x: float):
    """
    Equation of the Gaussian function, as described here: https://en.wikipedia.org/wiki/Gaussian_function

    :return: the image of x in the Gaussian function.
    """
    return math.exp(-((x - root_mean_square) ** 2) / (2 * (standard_deviation ** 2)))


class Cluster(abc.ABC):
    """
    A Cluster is a group of documents of a certain type. Is reflects the characteristics of the group of documents and
    its features are made from the features of all aggregated documents the cluster contains.
    """
    DOCUMENT_CLASS: Type[Document] = None

    @property
    def document_ids(self) -> Set[int]:
        """
        The ids of every document the cluster contains.
        """
        return {document.id for document in self.documents}

    @property
    def number_of_documents(self) -> int:
        return len(self.document_ids)

    def average_timestamp(self) -> float:
        return mean(self.timestamps)

    def __init__(self, document: Document):
        self.documents: Set[Document] = set()
        self.features: Features = Features()
        self.lowest_timestamp: datetime = datetime(1000, 1, 1, tzinfo=timezone.utc)
        self.highest_timestamp: datetime = datetime(3000, 1, 1, tzinfo=timezone.utc)
        self.timestamps: List[float] = []
        self.add_document_into_cluster(document)

    def add_document_into_cluster(self, document: Document):
        self.documents.add(document)
        self._add_document_features_into_cluster(document.features)
        self.lowest_timestamp = max(self.lowest_timestamp, document.timestamp)
        self.highest_timestamp = min(self.highest_timestamp, document.timestamp)
        self.timestamps.append(document.timestamp.timestamp())

    @abc.abstractmethod
    def _add_document_features_into_cluster(self, features: Features):
        """
        Merge the incoming Features with already existing Cluster Features.
        """

    def __eq__(self, other):
        return self.document_ids == other.document_ids

    def __hash__(self):
        return hash(tuple(sorted(self.document_ids)))

    @classmethod
    def from_documents(cls, documents: List[Document]) -> "Cluster":
        cluster = cls(documents[0])
        for document in documents[1:]:
            cluster.add_document_into_cluster(document)
        return cluster


# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
def process_document(
    clusters: List[Cluster],
    number_of_days_window: float,
    similarity_class: Type["SimilarityBetweenFeatures"],
    model: "ScoringModel",
    threshold: float,
    merge_model: "ScoringModel",
    cluster_class: Type["Cluster"],
    document: "Document"
):
    """
    This piece of code is a rewrite of the PutDocument function in the Aggregator class from the original authors.
    See: https://github.com/Priberam/news-clustering/blob/master/clustering.py#L112

    Parameters were added in order to extract the function out of the Aggregator class.
    """
    best_candidate_cluster_index = -1  # out of range by default
    best_candidate_cluster_score = 0.0
    similarities_between_document_and_all_clusters = []
    for cluster_index, cluster in enumerate(clusters):

        # Compute the similarity between the document and the candidate cluster
        similarity_document_cluster = get_similarity_between_document_and_cluster(
            document, cluster, number_of_days_window, similarity_class
        )
        score = model.score(similarity_document_cluster)
        similarities_between_document_and_all_clusters.append(similarity_document_cluster)

        # Find the best of all candidate clusters.
        if score > best_candidate_cluster_score and (score > threshold or merge_model):
            best_candidate_cluster_score = score
            best_candidate_cluster_index = cluster_index

    # A candidate cluster exists, as well as a merge model
    if best_candidate_cluster_index >= 0 and merge_model:
        merge_score = merge_model.score(
            similarities_between_document_and_all_clusters[best_candidate_cluster_index]
        )
        # A merge score below zero means the document cannot be merged with any cluster, a new one is created
        if merge_score <= 0:
            best_candidate_cluster_index = -1

    if best_candidate_cluster_index == -1:
        clusters.append(cluster_class(document))
    else:
        clusters[best_candidate_cluster_index].add_document_into_cluster(document)

    return clusters
