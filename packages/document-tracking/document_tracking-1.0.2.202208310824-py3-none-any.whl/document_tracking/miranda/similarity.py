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


import math
from typing import Dict, Type

from document_tracking.clustering import Cluster
from document_tracking_resources.documents import Document
from document_tracking.similarity import SimilarityBetweenFeatures


def get_similarity_between_document_and_cluster(
    document: Document,
    cluster: Cluster,
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
