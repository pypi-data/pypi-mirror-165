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
from typing import Optional, Tuple, Type

from document_tracking.miranda.clustering import (
    AggregatorOfDenseCorpus,
    AggregatorOfSparseCorpus,
)
from document_tracking.resources.models import LogisticModel, ScoringModel
from document_tracking_resources import ISO6393LanguageCode
from document_tracking_resources.corpus import (
    SUPPORTED_ISO_639_3_LANGUAGES,
    NewsCorpusWithDenseFeatures,
    NewsCorpusWithSparseFeatures,
    TwitterCorpusWithDenseFeatures,
    TwitterCorpusWithSparseFeatures,
)

from news_tracking.news_tracking_evaluation import evaluate_clusters_and_output_result


def _get_models(
    model_path: str, loaded_merge_model_path: Optional[str], model_type: Type[ScoringModel]
) -> Tuple[ScoringModel, Optional[ScoringModel]]:
    loaded_merge_model, loaded_merge_model_path = None, Path(loaded_merge_model_path or "")
    if loaded_merge_model_path.is_file():
        loaded_merge_model = model_type.from_json_file(str(loaded_merge_model_path))
    return model_type.from_json_file(model_path), loaded_merge_model


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
        required=False,
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
        "--threshold",
        type=float,
        required=False,
        default=0.0,
        help="The threshold to decide whether to include the documents or not into the clusters. "
        "This threshold is given by the trained models.",
    )
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Path to the JSON file containing the model to use in order to cluster documents. "
        "It contains each feature name with a corresponding weight, and an intercept. This is loaded by the "
        "Model or LogisticModel classes.",
    )
    parser.add_argument(
        "--merge-model",
        type=str,
        required=False,
        default=None,
        help="Optional path to the JSON file containing the merge model to cluster documents. This is kept only to "
        "be used with the original Miranda model and should not be used in another context.",
    )
    parser.add_argument(
        "--number-of-days-ts-similarity",
        type=float,
        required=False,
        default=3.0,
        help="The number of days, to put into the time similarity function. If below this number of days, similarity "
        "is high and decreases significantly if above this number of days.",
    )

    # Clustering type
    model_types = parser.add_mutually_exclusive_group(required=False)
    model_types.add_argument(
        "--miranda-model",
        action="store_true",
        help="Whether to use the models provided by Miranda (without Logistic Regression). This is kept only to be "
        "used with the original Miranda model and should not be used in another context.",
    )
    model_types.add_argument(
        "--logistic-model",
        action="store_true",
        help="Whether to use a Logistic Regression model, this is the kind "
        "of model that is used by default and the output of the "
        "training script.",
    )

    # Output arguments
    parser.add_argument(
        "--elapsed-time-file",
        type=str,
        required=True,
        help="Path to the CSV file where to store elapsed time information",
    )
    parser.add_argument(
        "--clusters-file",
        type=str,
        required=True,
        help="Path to the CSV file where to store the association between document ids and their clusters ids.",
    )

    # Evaluation
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
    aggregator_classes = {"dense": AggregatorOfDenseCorpus, "sparse": AggregatorOfSparseCorpus}

    language = args.language or "ALL"
    corpus_class = corpus_classes.get(args.vectors_type).get(args.dataset_type)
    if language in SUPPORTED_ISO_639_3_LANGUAGES:
        corpus = corpus_class.from_pickle_file(args.corpus, args.language)
    else:
        corpus = corpus_class.from_pickle_file(args.corpus)

    processing_model_types = {"miranda_model": ScoringModel, "logistic_model": LogisticModel}
    model_to_use = processing_model_types.get(
        args.miranda_model or args.logistic_model, processing_model_types.get("miranda_model")
    )
    clustering_model, merge_model = _get_models(args.model, args.merge_model, model_to_use)
    aggregator = aggregator_classes.get(args.vectors_type)(
        corpus, clustering_model, args.threshold, merge_model, args.number_of_days_ts_similarity
    )

    aggregator.cluster_corpus()

    # Write output
    Path(args.elapsed_time_file).parent.mkdir(exist_ok=True, parents=True)
    if args.elapsed_time_file:
        aggregator.time_elapsed_for_clustering.to_csv(args.elapsed_time_file, header=False)

    Path(args.clusters_file).parent.mkdir(exist_ok=True, parents=True)
    if args.clusters_file:
        aggregator.get_clustering_results().to_csv(args.clusters_file, header=False)

    evaluate_clusters_and_output_result(
        corpus,
        args.language,
        aggregator.get_clustering_results(),
        args.output_results,
        args.ground_truth_clusters_file,
        nb_documents=len(corpus),
        time_spent=aggregator.time_spent_in_seconds,
    )


if __name__ == "__main__":
    main()
