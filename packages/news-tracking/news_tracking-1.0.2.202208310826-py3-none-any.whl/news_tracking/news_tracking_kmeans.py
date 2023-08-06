#!/usr/bin/env python3
#
# This file is part of the news_clustering_in_multiple_languages project.
#
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

import argparse
from pathlib import Path
from warnings import simplefilter

from document_tracking.kmeans.clustering import (
    KMeansAggregator,
    KMeansAggregatorOfDenseCorpus,
    KMeansAggregatorOfSparseCorpus,
    KMeansMetric,
)
from document_tracking_resources import ISO6393LanguageCode
from document_tracking_resources.corpus import (
    SUPPORTED_ISO_639_3_LANGUAGES,
    NewsCorpusWithDenseFeatures,
    NewsCorpusWithSparseFeatures,
    SparseCorpusMixin,
    TwitterCorpusWithDenseFeatures,
    TwitterCorpusWithSparseFeatures,
)
from pandas import concat
from tqdm import tqdm

# YellowBrick, used by the KMeansAggregator has FutureWarning related to scikit-learn
from news_tracking.news_tracking_evaluation import evaluate_clusters_and_output_result

simplefilter(action="ignore", category=FutureWarning)


def main():
    parser = argparse.ArgumentParser()

    # Input arguments
    parser.add_argument(
        "--corpus", type=str, required=True, help="Path to the pickle file containing the corpus to process."
    )
    parser.add_argument(
        "--dataset-type",
        choices=["twitter", "news"],
        required=True,
        type=str,
        help="The kind of dataset to process. "
        "‘twitter’ will use the ’TwitterCorpus’ class, the ‘Corpus’ class otherwise",
    )
    parser.add_argument(
        "--language",
        type=ISO6393LanguageCode,
        required=True,
        help="The ISO-639-1 Language code of the language to process in the corpus.",
        choices=SUPPORTED_ISO_639_3_LANGUAGES,
    )
    parser.add_argument(
        "--vectors-type",
        choices=["sparse", "dense"],
        required=True,
        type=str,
        help="The type of features used to describe the documents. Sparse data are often TF-IDF vectors, while dense"
        "vectors could be word2vec or BERT vectors for instance",
    )
    parser.add_argument(
        "--kmeans-metric",
        type=str,
        choices=[metric.value[0] for metric in KMeansMetric],
        help="The heuristic to use in order to determine a good number of clusters to use. Gold means we will use the "
        "already given labels of the dataset, if they are provided.",
    )
    parser.add_argument(
        "--size-of-time-windows-in-days",
        type=int,
        required=False,
        help="The number of days that last every time bucket of documents. The corpus is split into bucket of same"
        "number of days.",
    )

    parser.add_argument(
        "--clusters-file",
        type=str,
        required=False,
        help="Path to the CSV file where to store the association between document ids and their clusters ids.",
    )
    parser.add_argument(
        "--ground-truth-clusters-file",
        type=str,
        required=False,
        help="Path to the gold clustering output cluster file in CSV.",
    )
    parser.add_argument(
        "--output-results", required=True, type=str, help="Where to put (or append to an existing file) the results."
    )

    args = parser.parse_args()

    corpus_classes = {
        "dense": {"news": NewsCorpusWithDenseFeatures, "twitter": TwitterCorpusWithDenseFeatures},
        "sparse": {"news": NewsCorpusWithSparseFeatures, "twitter": TwitterCorpusWithSparseFeatures},
    }
    aggregator_classes = {"dense": KMeansAggregatorOfDenseCorpus, "sparse": KMeansAggregatorOfSparseCorpus}

    language = args.language or "ALL"
    corpus_class = corpus_classes.get(args.vectors_type).get(args.dataset_type)
    if language in SUPPORTED_ISO_639_3_LANGUAGES:
        corpus = corpus_class.from_pickle_file(args.corpus, args.language)
    else:
        corpus = corpus_class.from_pickle_file(args.corpus)

    if args.size_of_time_windows_in_days is None or args.size_of_time_windows_in_days <= 0:
        windows = [corpus]
        nb_of_windows = 1
    else:
        windows = corpus.iterate_over_windows(args.size_of_time_windows_in_days, 0)
        nb_of_windows = corpus.nb_over_time_windows(args.size_of_time_windows_in_days, 0)

    metric = KMeansMetric[args.kmeans_metric.upper()]

    results, clusters = [], []
    for window in tqdm(windows, total=nb_of_windows, desc="Iterating over windows"):
        if len(window) > 0:
            aggregator = aggregator_classes.get(args.vectors_type)(window, metric)
            aggregator.cluster_corpus()
            results.append(aggregator.clustering_scores)
            clusters.append(aggregator.clusters)

    all_results = concat(results, axis=1).T
    merged_cluster_results = KMeansAggregator.merge_multiple_non_overlapping_clustering_results(clusters)
    Path(args.clusters_file).parent.mkdir(parents=True, exist_ok=True)
    if args.clusters_file and Path(args.clusters_file).parent.exists():
        merged_cluster_results.to_csv(args.clusters_file, header=False)
        all_results.to_csv(Path(args.clusters_file).with_suffix(".windows.csv"), header=True)

    evaluate_clusters_and_output_result(
        corpus,
        args.language,
        merged_cluster_results,
        args.output_results,
        args.ground_truth_clusters_file,
        nb_documents=len(corpus),
        time_spent=all_results.time_in_seconds.sum(),
    )


if __name__ == "__main__":
    main()
