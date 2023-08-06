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

import pandas
from document_tracking.evaluation import ClusteringScores
from document_tracking_resources import ISO6393LanguageCode
from document_tracking_resources.corpus import (
    SUPPORTED_ISO_639_3_LANGUAGES,
    Corpus,
    NewsCorpusWithSparseFeatures,
    SparseCorpusMixin,
    TwitterCorpusWithSparseFeatures,
)
from pandas import DataFrame, Series

pandas.set_option("display.max_rows", 500)
pandas.set_option("display.max_columns", 500)
pandas.set_option("display.width", 1000)


def get_evaluation_statistics_and_difference_with_gold(
    language: str, processed_corpus: Corpus, custom_clusters: Series, ground_truth_clusters: Series
):
    clustering_scores = ClusteringScores(processed_corpus.labels, custom_clusters)
    miranda_clustering_scores = ClusteringScores(processed_corpus.labels, ground_truth_clusters)

    # Compute differences
    miranda_metrics = miranda_clustering_scores.get_clustering_scores_dict().get("metrics")
    clustering_metrics = clustering_scores.get_clustering_scores_dict().get("metrics")
    differences_with_gold = {
        x: round(clustering_metrics[x] - miranda_metrics[x], 3)
        for x in miranda_metrics
        if x in clustering_metrics
        if isinstance(miranda_metrics[x], float)
    }

    clustering_scores = {
        language: clustering_scores.get_scores(),
        f"{language}_gold": miranda_clustering_scores.get_scores(),
    }

    return clustering_scores, differences_with_gold


def evaluate_clusters_and_output_result(
    corpus: Corpus,
    language: ISO6393LanguageCode,
    clusters: Series,
    output_results_file: str,
    ground_truth_clusters_file: str,
    **kwargs,
):
    output_path = Path(output_results_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if ground_truth_clusters_file:
        gold_clusters = pandas.read_csv(ground_truth_clusters_file, index_col=0, header=None, squeeze=True)
        evaluation_metrics, _ = get_evaluation_statistics_and_difference_with_gold(
            language, corpus, clusters, gold_clusters
        )

        print(f" Clustering results in {language} ".center(80, "#"))
        df = DataFrame.from_dict(evaluation_metrics, orient="index")
        print(df)

        print(f" Difference with gold labeling in {language} ".center(80, "#"))
        print(df.diff(axis=0).drop(language))

    else:
        print(f" Clustering results in {language} ".center(80, "#"))
        df = DataFrame.from_dict({language: ClusteringScores(corpus.labels, clusters).get_scores()}, orient="index")
        for kwarg_name, kwarg_value in kwargs.items():
            df.at[language, kwarg_name] = kwarg_value
        print(df)

    df.to_csv(output_path, mode="w", index=True, header=True)


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate a clustering output and possibly compare it with a ground truth."
    )

    # Input arguments
    parser.add_argument(
        "--corpus", type=str, required=True, help="Path to the .pickle file containing the corpus to process."
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
        help="The ISO-639-1 Language code of the language to process.",
        choices=SUPPORTED_ISO_639_3_LANGUAGES,
    )
    parser.add_argument(
        "--clusters-file", type=str, required=True, help="Path to the clustering output cluster file in CSV."
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

    corpus_classes = {"news": NewsCorpusWithSparseFeatures, "twitter": TwitterCorpusWithSparseFeatures}
    corpus: SparseCorpusMixin = corpus_classes.get(args.dataset_type).from_pickle_file(args.corpus, args.language)

    clusters = pandas.read_csv(args.clusters_file, index_col=0, header=None, squeeze=True)
    evaluate_clusters_and_output_result(
        corpus, args.language, clusters, args.output_results, args.ground_truth_clusters_file
    )


if __name__ == "__main__":
    main()
