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
import json
import logging
import pickle
import time
from pathlib import Path
from typing import Collection, Dict
from warnings import simplefilter

import numpy
from document_tracking.miranda.learning import (
    AggregatorOfDenseCorpusWithTrueLabels,
    AggregatorOfSparseCorpusWithTrueLabels,
    grid_search_logistic_regression_from_similarities,
    subsample_dataset_by_reducing_number_of_negative_samples,
)
from document_tracking.resources.models import LogisticModel
from document_tracking_resources import ISO6393LanguageCode
from document_tracking_resources.corpus import (
    SUPPORTED_ISO_639_3_LANGUAGES,
    NewsCorpusWithDenseFeatures,
    NewsCorpusWithSparseFeatures,
    TwitterCorpusWithDenseFeatures,
    TwitterCorpusWithSparseFeatures,
)
from matplotlib import pyplot
from pandas import DataFrame, read_hdf
from sklearn.decomposition import PCA
from sklearn.exceptions import ConvergenceWarning
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    classification_report,
    confusion_matrix,
)
from sklearn.utils import compute_sample_weight
from tqdm import tqdm

simplefilter("ignore", category=ConvergenceWarning)

logger = logging.getLogger(__name__)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s in %(module)s − %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


def get_model_coefficients(logistic_model: LogisticRegression, similarities: DataFrame):
    feature_weights = dict(
        zip(
            [feature_name for feature_name in similarities.columns if feature_name.startswith("f_")],
            *logistic_model.coef_,
        )
    )
    feature_weights["intercept"] = logistic_model.intercept_[0]
    feature_weights["sum_coefficients"] = sum(*logistic_model.coef_)
    return feature_weights


def convert_sklearn_logistic_model_to_document_tracking_logistic_model(
    sklearn_model: LogisticRegression, similarities: DataFrame
) -> LogisticModel:
    model_coefficients = get_model_coefficients(sklearn_model, similarities)
    return LogisticModel(
        weights={key: value for key, value in model_coefficients.items() if key.startswith("f_")},
        intercept=model_coefficients.get("intercept"),
    )


def compute_similarity_scores_in_language(
    language: ISO6393LanguageCode, similarities: DataFrame, model: LogisticModel
) -> DataFrame:
    scores = {}
    for idx, row in tqdm(similarities.iterrows(), total=len(similarities), desc=f"Computing scores in {language}"):
        scores[idx] = {
            "score": model.score(row.to_dict()),
            "same_cluster": row["same_cluster"],
        }

    return DataFrame.from_dict(scores, orient="index")


def get_all_scores_with_moving_threshold(scores: DataFrame, thresholds: Collection) -> Dict[float, Dict[str, float]]:
    """
    Get the precision, recall and F1 value for different kind of thresholds in order to get the most performant one.
    """
    precision_recall_f1_scores = {}

    for i in tqdm(thresholds, desc="Finding the most optimal threshold to maximize F1"):
        below_threshold = scores[scores.score <= i]
        above_threshold = scores[scores.score > i]
        tp = len(above_threshold[above_threshold.same_cluster])
        fn = len(above_threshold[~above_threshold.same_cluster])
        fp = len(below_threshold[below_threshold.same_cluster])
        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2 * ((precision * recall) / (precision + recall))
        precision_recall_f1_scores[i] = {"Precision": precision, "Recall": recall, "F1": f1}
    return precision_recall_f1_scores


def plot_true_false_ratio_of_similarities(
    similarities: DataFrame, export_path: Path, language: ISO6393LanguageCode, title: str
):
    nb_of_true = len(similarities[similarities.same_cluster])
    nb_of_false = len(similarities[~similarities.same_cluster])
    true_ratio = round(nb_of_true / len(similarities) * 100, 2)
    false_ratio = round(nb_of_false / len(similarities) * 100, 2)

    figure = pyplot.figure(constrained_layout=True)
    ax = figure.add_subplot()
    ax.title.set_text(f"Ratio of True/False for ‘{title}’ corpus in ‘{language}’")

    pyplot.bar(
        "True",
        nb_of_true,
        color="blue",
        label=f"Nb. True ({nb_of_true} - {true_ratio}%)",
    )
    pyplot.bar(
        "False",
        nb_of_false,
        color="purple",
        label=f"Nb. False ({nb_of_false} - {false_ratio}%)",
    )
    pyplot.legend()
    pyplot.plot()
    figure.savefig(export_path / f"{title}_true_false_ratio_in_{language}.png", format="png")


def plot_mean_median_std(similarities: DataFrame, export_path: Path, language: ISO6393LanguageCode, dataset_name: str):
    figure = pyplot.figure(constrained_layout=True)
    ax = figure.add_subplot()

    sorted_similarities = similarities[sorted(similarities.columns.tolist())]
    true_corpus = sorted_similarities[sorted_similarities["same_cluster"]].drop("same_cluster", axis=1)
    false_corpus = sorted_similarities[~sorted_similarities["same_cluster"]].drop("same_cluster", axis=1)

    ax.title.set_text(f"Mean and Std for ‘{dataset_name}’ corpus in ‘{language}’")
    ax.set_ylim(-0.1, 1.0)

    mean = true_corpus.mean()
    std = true_corpus.std()
    median = true_corpus.median()
    ax.errorbar(x=mean.index, y=mean, yerr=std, linestyle="None", marker="^", ecolor="g", label="Same cluster")
    ax.plot(median.index, median, marker="o", color="purple", linestyle="None", label="Mean same cluster")

    mean = false_corpus.mean()
    std = false_corpus.std()
    median = false_corpus.median()
    ax.errorbar(x=mean.index, y=mean, yerr=std, linestyle="None", marker="^", ecolor="r", label="Different cluster")
    ax.plot(median.index, median, marker="o", color="yellow", linestyle="None", label="Mean different cluster")

    ax.tick_params(axis="x", rotation=90)
    ax.legend(loc=1)

    figure.savefig(
        export_path / "mean_std_median_analysis_of_similarities_corpora.png",
        dpi=200,
        facecolor="w",
        edgecolor="w",
        orientation="portrait",
    )


def plot_quartile_median_mean(
    similarities: DataFrame, export_path: Path, language: ISO6393LanguageCode, dataset_name: str
):
    figure = pyplot.figure(constrained_layout=True)
    ax = figure.add_subplot()

    sorted_similarities = similarities[sorted(similarities.columns.tolist())]
    true_corpus = sorted_similarities[sorted_similarities["same_cluster"]].drop("same_cluster", axis=1)
    false_corpus = sorted_similarities[~sorted_similarities["same_cluster"]].drop("same_cluster", axis=1)

    ax.title.set_text(f"Q1, Q2, Q3 for ‘{dataset_name}’ corpus in ‘{language}’")
    ax.set_ylim(-0.1, 1.0)

    first_quantile = true_corpus.quantile(0.25)
    median = true_corpus.median()
    third_quantile = true_corpus.quantile(0.75)

    ax.plot(first_quantile.index, first_quantile, marker="^", color="blue", linestyle="None", label="Q1 true")
    ax.plot(median.index, median, marker="o", color="purple", linestyle="None", label="Q2 true")
    ax.plot(third_quantile.index, third_quantile, marker="v", color="green", linestyle="None", label="Q3 true")

    first_quantile = false_corpus.quantile(0.25)
    median = false_corpus.median()
    third_quantile = false_corpus.quantile(0.75)

    ax.plot(first_quantile.index, first_quantile, marker="^", color="yellow", linestyle="None", label="Q1 true")
    ax.plot(median.index, median, marker="o", color="red", linestyle="None", label="Q2 true")
    ax.plot(third_quantile.index, third_quantile, marker="v", color="orange", linestyle="None", label="Q3 true")

    ax.tick_params(axis="x", rotation=90)
    ax.legend(loc=1)

    figure.savefig(
        export_path / "q1_q2_q3_analysis_of_similarities_corpora.png",
        dpi=200,
        facecolor="w",
        edgecolor="w",
        orientation="portrait",
    )


def plot_pca_2d(similarities: DataFrame, export_path: Path, language: ISO6393LanguageCode, dataset_name: str):
    figure = pyplot.figure(constrained_layout=True)
    ax = figure.add_subplot()

    sampled_similarities = similarities
    if len(similarities) > 25_000:
        sampled_similarities = similarities.replace(numpy.nan, 0.0).sample(n=25_000)

    pca_2d = PCA(n_components=2)
    pcs_2c = DataFrame(
        pca_2d.fit_transform(sampled_similarities.drop(["same_cluster"], axis=1)),
        columns=["First Component", "Second Component"],
    )
    pcs_2c["truth"] = sampled_similarities["same_cluster"].to_list()
    ax.title.set_text(f"2D PCA for ‘{dataset_name}’ corpus in ‘{language}’")
    colors = ("r", "g")
    for same_cluster, label in zip(
        *[(True, False), ("Documents in the same cluster", "Documents in different clusters")]
    ):
        pca_2c_same_cluster_or_no = pcs_2c[pcs_2c["truth"] == same_cluster]
        ax.scatter(
            pca_2c_same_cluster_or_no["First Component"],
            pca_2c_same_cluster_or_no["Second Component"],
            c=[colors[int(same_cluster)]] * len(pca_2c_same_cluster_or_no),
            label=label,
        )

    ax.set_xlabel("First Component")
    ax.set_ylabel("Second Component")
    ax.legend(loc=2)

    figure.figure.savefig(
        export_path / "pca2d_of_similarities_corpora.png",
        dpi=200,
        facecolor="w",
        edgecolor="w",
        orientation="portrait",
    )


def plot_pca_3d(similarities: DataFrame, export_path: Path, language: ISO6393LanguageCode, dataset_name: str):
    figure = pyplot.figure(constrained_layout=True)
    ax = figure.add_subplot(projection="3d")

    sampled_similarities = similarities
    if len(similarities) > 25_000:
        sampled_similarities = similarities.replace(numpy.nan, 0.0).sample(n=25_000)

    pca_3d = PCA(n_components=3)
    pca_3c = DataFrame(
        pca_3d.fit_transform(sampled_similarities.drop(["same_cluster"], axis=1)),
        columns=["First Component", "Second Component", "Third component"],
    )
    pca_3c["truth"] = sampled_similarities["same_cluster"].to_list()
    ax.title.set_text(f"3D PCA for ‘{dataset_name}’ corpus in ‘{language}’")
    colors = ("r", "g")
    for same_cluster, label in zip(
        *[(True, False), ("Documents in the same cluster", "Documents in different clusters")]
    ):
        pca_3c_same_cluster_or_no = pca_3c[pca_3c["truth"] == same_cluster]
        ax.scatter(
            pca_3c_same_cluster_or_no.iloc[:, 0],
            pca_3c_same_cluster_or_no.iloc[:, 1],
            pca_3c_same_cluster_or_no.iloc[:, 2],
            c=[colors[int(same_cluster)]] * len(pca_3c_same_cluster_or_no),
            label=label,
        )
    ax.set_xlabel("First Component")
    ax.set_ylabel("Second Component")
    ax.set_zlabel("Third Component")
    ax.legend(loc=2)

    figure.savefig(
        export_path / "pca3d_of_similarities_corpora.png",
        dpi=200,
        facecolor="w",
        edgecolor="w",
        orientation="portrait",
    )


def plot_similarity_scores_though_model(
    similarity_scores: DataFrame, export_path: Path, language: ISO6393LanguageCode, dataset_name: str
):
    figure = pyplot.figure(constrained_layout=True)
    ax = figure.add_subplot()

    true_scores = similarity_scores[similarity_scores.same_cluster]
    false_scores = similarity_scores[~similarity_scores.same_cluster]

    statistics = {
        "Same Cluster": {
            "Median": true_scores.score.median(),
            "Mean": true_scores.score.mean(),
            "Std": true_scores.score.std(),
        },
        "Different cluster": {
            "Median": false_scores.score.median(),
            "Mean": false_scores.score.mean(),
            "Std": false_scores.score.std(),
        },
    }
    statistics_df = DataFrame.from_dict(statistics, orient="index")

    ax.title.set_text(f"Scores separation for ‘{dataset_name}’ in ’{language}’")
    ax.set_ylim(-0.1, 1.0)

    pyplot.errorbar(
        x=statistics_df.index,
        y=statistics_df["Median"],
        yerr=statistics_df["Std"],
        marker="^",
        color="royalblue",
        ecolor="green",
        linestyle="None",
        label="Median of similarity scores (with std)",
    )

    ax.tick_params(axis="x")
    ax.legend(loc="center")

    figure.savefig(
        export_path / "similarity_scores_though_model.png",
        dpi=200,
        facecolor="w",
        edgecolor="w",
        orientation="portrait",
    )


def plot_model_performance_to_disk(
    model: LogisticRegression,
    x: DataFrame,
    y: DataFrame,
    export_path: Path,
    language: ISO6393LanguageCode,
    dataset_name: str,
):
    """
    Export the model and the model metrics to the disk.

    :param model: the model to export and evaluate
    :param x: features of the test part of the original data
    :param y: labels of the test part of the original data
    :param export_path a path to export the content on the disk
    :param language: the language that is currently processed:
    :param dataset_name: the name of the dataset, used in the exported image
    """
    export_path.mkdir(parents=True, exist_ok=True)
    model_type = str(type(model).__name__).lower()

    # Into JSON, to read the model coefficients and intercept
    with open(export_path / f"{model_type}_model_{language}.json", mode="w", encoding="utf-8") as output_json_model:
        json.dump(get_model_coefficients(model, x), output_json_model, indent=2)

    # As a pickle file, to load it directly into scikit-learn
    with open(export_path / f"{model_type}_model_{language}.pickle", mode="wb") as output_sklearn_model:
        pickle.dump(model, output_sklearn_model)

    # Display model estimations
    y_pred = model.predict(x)

    cmd = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_pred, y))
    cmd.plot()
    figure, ax = pyplot.gcf(), pyplot.gca()
    ax.title.set_text(f"Confusion matrix for ‘{dataset_name}’ corpus in ‘{language}’")
    figure.savefig(export_path / f"{model_type}_confusion_matrix_{language}.png", format="png")

    sample_weights = compute_sample_weight(class_weight="balanced", y=y)
    rcd = RocCurveDisplay.from_predictions(y, y_pred, sample_weight=sample_weights)
    rcd.plot()
    figure, ax = pyplot.gcf(), pyplot.gca()
    ax.title.set_text(f"ROC Curve for ‘{dataset_name}’ corpus in ‘{language}’")
    figure.savefig(export_path / f"{model_type}_roc_curve_{language}.png", format="png")

    DataFrame.from_dict(classification_report(y_pred, y, output_dict=True)).to_csv(
        export_path / f"{model_type}_model_performance_in_{language}.csv"
    )


def export_scores_threshold_to_disk(
    performance_by_threshold: Dict[float, Dict[str, float]], export_path: Path, language: ISO6393LanguageCode
):
    """
    Export score threshold results as a figure on to the disk. A red vertical line is show where the F1 score is
    at his maximum.
    """
    df = DataFrame.from_dict(performance_by_threshold, orient="index")
    threshold_maximizes_f1 = df["F1"].idxmax()

    crossing_index = 0
    for idx, row in df.iterrows():
        if row["Precision"] <= row["Recall"]:
            crossing_index = df.iloc[df.index.get_loc(idx) - 1].name
            break

    df.plot(
        xlabel="Threshold",
        ylabel="Score",
        title=f"Precision, Recall, F1 curve depending on threshold in {language}.",
    )
    pyplot.axvline(
        x=threshold_maximizes_f1,
        ymin=0,
        ymax=1,
        c="red",
        label=f"Max F1: x={round(threshold_maximizes_f1, 3)}; y={round(df.loc[threshold_maximizes_f1]['F1'], 3)}",
    )
    if crossing_index > 1:
        pyplot.axvline(
            x=crossing_index,
            ymin=0,
            ymax=1,
            c="purple",
            label=f"Crossing: x={round(crossing_index, 3)}; y={round(df.loc[crossing_index]['F1'], 3)}",
        )
    pyplot.legend()
    figure = pyplot.gcf()
    figure.savefig(export_path / f"precision_recall_f1_curve_depending_on_threshold_in_{language}.png", format="png")

    with open(export_path / f"thresholds_in_{language}.json", mode="w", encoding="utf-8") as threshold_json_file:
        json.dump(
            {
                "precision_recall_intersection": crossing_index,
                "precision_recall_intersection_score": df.loc[crossing_index]["F1"] if crossing_index > 0 else None,
                "maximize_f1": threshold_maximizes_f1,
                "maximize_f1_score": df.loc[threshold_maximizes_f1]["F1"],
            },
            threshold_json_file,
            indent=2,
        )


def main():
    parser = argparse.ArgumentParser(description="Train a model for the Miranda et a. algorithm.")

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
        "--vectors-type",
        choices=["sparse", "dense"],
        required=True,
        type=str,
        help="The type of features used to describe the documents. Sparse data are often TF-IDF vectors, while dense"
        "vectors could be word2vec or BERT vectors for instance",
    )
    parser.add_argument(
        "--cache-directory",
        required=False,
        type=str,
        help="The directory where to cache the similarities and other material "
        "that is the result of long computations.",
    )
    parser.add_argument(
        "--language",
        type=str,
        required=False,
        help="Language to process in the ISO-639-3 format.",
        choices=SUPPORTED_ISO_639_3_LANGUAGES,
    )
    parser.add_argument(
        "--model-path",
        required=True,
        type=str,
        help="Parent directory of models to export "
        "(the script will organize its own structure inside of that directory",
    )

    args = parser.parse_args()

    start_time = time.process_time()

    dataset_short_name = Path(args.corpus).stem
    language = args.language or "ALL"

    model_destination_path = Path(f"{args.model_path}/{dataset_short_name}_{language}")
    model_destination_path.mkdir(parents=True, exist_ok=True)

    # Add a logging file handler
    logging_file_handler = logging.FileHandler(Path(model_destination_path) / "training_log.txt", mode="w")
    logging_file_handler.setLevel(logging.DEBUG)
    logging_file_handler.setFormatter(formatter)
    logger.addHandler(logging_file_handler)

    # First, compute similarities
    corpus_classes = {
        "dense": {"news": NewsCorpusWithDenseFeatures, "twitter": TwitterCorpusWithDenseFeatures},
        "sparse": {"news": NewsCorpusWithSparseFeatures, "twitter": TwitterCorpusWithSparseFeatures},
    }
    aggregator_classes = {
        "dense": AggregatorOfDenseCorpusWithTrueLabels,
        "sparse": AggregatorOfSparseCorpusWithTrueLabels,
    }

    corpus_class = corpus_classes.get(args.vectors_type).get(args.dataset_type)
    if language in SUPPORTED_ISO_639_3_LANGUAGES:
        corpus = corpus_class.from_pickle_file(args.corpus, args.language)
    else:
        corpus = corpus_class.from_pickle_file(args.corpus)

    if args.cache_directory:
        cache_path = Path(args.cache_directory)
        cache_path.mkdir(parents=True, exist_ok=True)
        similarities_scores_cache_file = cache_path / f"scores_with_model_in_{language}_{dataset_short_name}.hdf"
        similarities_cache_file = cache_path / f"similarity_scores_in_{language}_{dataset_short_name}.hdf"
    else:
        similarities_scores_cache_file = None
        similarities_cache_file = None

    if similarities_scores_cache_file is not None and similarities_scores_cache_file.exists():
        similarity_scores = read_hdf(similarities_scores_cache_file)
    else:
        logger.info("Computing the similarities between documents and clusters (algorithm simulation)")

        if similarities_cache_file is not None and similarities_cache_file.exists():
            logger.warning("Loading EXISTING similarities from a cache file (%s)", similarities_cache_file)
            similarities = read_hdf(similarities_cache_file)
        else:
            aggregator = aggregator_classes.get(args.vectors_type)(corpus, corpus.labels)
            aggregator.cluster_corpus()
            similarities = aggregator.aggregated_cluster_similarities
            if similarities_cache_file is not None:
                similarities.to_hdf(str(similarities_cache_file), key="df")

        # Export the T/F ratio of sub sampled similarities
        plot_true_false_ratio_of_similarities(
            similarities, model_destination_path, language, f"{dataset_short_name}_before_sampling"
        )

        # Sub-sample similarities
        sub_sampled_similarities = subsample_dataset_by_reducing_number_of_negative_samples(similarities)
        plot_true_false_ratio_of_similarities(
            sub_sampled_similarities, model_destination_path, language, f"{dataset_short_name}_before_sampling"
        )
        plot_mean_median_std(sub_sampled_similarities, model_destination_path, language, dataset_short_name)
        plot_quartile_median_mean(sub_sampled_similarities, model_destination_path, language, dataset_short_name)
        plot_pca_2d(sub_sampled_similarities, model_destination_path, language, dataset_short_name)
        plot_pca_3d(sub_sampled_similarities, model_destination_path, language, dataset_short_name)

        # Second, perform a Grid Search to find the most appropriate model
        logger.info("LogisticRegression Grid Search to find the best model for the data.")
        model, x, y = grid_search_logistic_regression_from_similarities(sub_sampled_similarities)
        logger.debug("Best model %s", str(model))

        logger.info("Exporting best model performance information to disk.")
        plot_model_performance_to_disk(model, x, y, model_destination_path, language, dataset_short_name)

        # Third, compute final scores with this model
        logger.info("Computing similarity scores using the best model found")
        similarity_scores = compute_similarity_scores_in_language(
            language,
            similarities,
            convert_sklearn_logistic_model_to_document_tracking_logistic_model(model, sub_sampled_similarities),
        )
        if similarities_scores_cache_file is not None:
            similarity_scores.to_hdf(str(similarities_scores_cache_file), key="df")

    plot_similarity_scores_though_model(similarity_scores, model_destination_path, language, dataset_short_name)

    # Then, compute the optimal threshold to maximise F1 of the model (normally 0.5 by default)
    logger.info("Searching for the best threshold to use in order to maximize the F1 value with the model.")
    threshold_scores = get_all_scores_with_moving_threshold(
        similarity_scores, numpy.arange(similarity_scores.score.min(), similarity_scores.score.max(), step=0.001)
    )
    export_scores_threshold_to_disk(threshold_scores, model_destination_path, language)

    logger.info("Model trained in %f", time.process_time() - start_time)


if __name__ == "__main__":
    main()
