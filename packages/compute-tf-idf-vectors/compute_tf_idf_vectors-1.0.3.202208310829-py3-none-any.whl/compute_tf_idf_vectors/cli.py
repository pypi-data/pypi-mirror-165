#!/usr/bin/env python3
#
# This file is part of the event_in_news_dataset project

# Copyright (c) 2021 Guillaume Bernard <contact@guillaume-bernard.fr>
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
import abc
import argparse
import logging
import multiprocessing
from ast import literal_eval
from functools import cached_property
from pathlib import Path
from typing import List

import numpy as np
import pandas
import scipy.sparse as sp
from document_processing import (
    get_tokens_lemmas_entities_from_document,
    preprocess_list_of_tweets,
    process_documents,
)
from document_tracking_resources.corpus import (
    Corpus,
    ISO6393LanguageCode,
    NewsCorpusWithSparseFeatures,
    SparseCorpusMixin,
    TwitterCorpusWithSparseFeatures,
)
from pandas import DataFrame, Series
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm

logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s in %(module)s − %(message)s"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

num_cores = multiprocessing.cpu_count()
num_partitions = num_cores - 2


def return_parameter(x):
    # It is not possible to pickle lambda functions
    return x


class CorpusFeaturesExtractor:
    model_names = {
        "deu": "de_core_news_md",
        "spa": "es_core_news_md",
        "eng": "en_core_web_md",
    }

    @abc.abstractmethod
    def compute_document_features(self, corpus: Corpus) -> DataFrame:
        pass


class NewsCorpusFeaturesExtractor(CorpusFeaturesExtractor):
    def compute_document_features(self, corpus: Corpus) -> DataFrame:
        document_features = DataFrame(
            index=corpus.documents.index,
            columns=NewsCorpusWithSparseFeatures.FEATURE_COLUMNS,
        )

        for language in corpus.languages:
            for (
                part_of_the_document
            ) in NewsCorpusWithSparseFeatures.DOCUMENT_TEXT_CONTENT:
                corpus_in_lang = corpus.documents[corpus.documents.lang == language]
                for document_index, document in tqdm(
                    process_documents(
                        corpus_in_lang[part_of_the_document],
                        self.model_names.get(language),
                    ),
                    total=len(corpus_in_lang),
                    desc=f"Extraction of document features from ‘{part_of_the_document}’ in ‘{language}’",
                ):
                    tokens, lemmas, entities = get_tokens_lemmas_entities_from_document(
                        document
                    )
                    document_features.at[
                        document_index, f"f_tokens_{part_of_the_document}"
                    ] = tokens
                    document_features.at[
                        document_index, f"f_lemmas_{part_of_the_document}"
                    ] = lemmas
                    document_features.at[
                        document_index, f"f_entities_{part_of_the_document}"
                    ] = entities

        document_features["f_tokens_all"] = (
            document_features.f_tokens_title + document_features.f_tokens_text
        )
        document_features["f_lemmas_all"] = (
            document_features.f_lemmas_title + document_features.f_lemmas_text
        )
        document_features["f_entities_all"] = (
            document_features.f_entities_title + document_features.f_entities_text
        )

        document_features.dropna(how="all", axis=0, inplace=True)
        assert sorted(NewsCorpusWithSparseFeatures.FEATURE_COLUMNS) == sorted(
            document_features.columns.to_list()
        )
        return document_features


class TwitterCorpusFeaturesExtractor(CorpusFeaturesExtractor):
    def compute_document_features(
        self, corpus: TwitterCorpusWithSparseFeatures
    ) -> DataFrame:
        features = {}

        for language in corpus.languages:
            for (
                part_of_the_document
            ) in TwitterCorpusWithSparseFeatures.DOCUMENT_TEXT_CONTENT:
                corpus_in_lang = corpus.documents[corpus.documents.lang == language]
                for document_index, document in tqdm(
                    process_documents(
                        corpus_in_lang[part_of_the_document],
                        self.model_names.get(language),
                    ),
                    total=len(corpus_in_lang),
                    desc=f"Extraction of document features from ‘{part_of_the_document}’ in ‘{language}’",
                ):
                    tokens, lemmas, entities = get_tokens_lemmas_entities_from_document(
                        document, preprocessor=preprocess_list_of_tweets
                    )
                    features[corpus_in_lang.loc[document_index].name] = {
                        "f_tokens_text": tokens,
                        "f_lemmas_text": lemmas,
                        "f_entities_text": entities,
                    }

        document_features = DataFrame.from_dict(features, orient="index")
        document_features.dropna(how="all", axis=0, inplace=True)
        assert sorted(TwitterCorpusWithSparseFeatures.FEATURE_COLUMNS) == sorted(
            document_features.columns.to_list()
        )
        return document_features


class TFIDFVectoriser:
    @cached_property
    @abc.abstractmethod
    def feature_names(self):
        pass

    @cached_property
    @abc.abstractmethod
    def languages(self):
        pass

    def __get_models_from_feature_name(
        self, model_feature_name: str, iso_639_3_language_code: ISO6393LanguageCode
    ) -> TfidfVectorizer:
        for feature_name in self.feature_names:
            if feature_name in model_feature_name:
                return self.__getattribute__(
                    f"{feature_name}_{iso_639_3_language_code}_model"
                )
        raise ValueError(
            f"No model found for the feature name {model_feature_name} in {iso_639_3_language_code}."
        )

    @staticmethod
    def parallelize_dataframe(dataframe, function_to_parallelise):
        a = np.array_split(dataframe, num_partitions)
        # pylint: disable=consider-using-with
        pool = multiprocessing.Pool(num_cores)
        dataframe = sp.vstack(pool.map(function_to_parallelise, a), format="csr")
        pool.close()
        pool.join()
        return dataframe

    def compute_weights_for_corpus(
        self, corpus: SparseCorpusMixin, document_features: DataFrame
    ):
        document_weights = DataFrame(
            index=document_features.index,
            columns=document_features.columns,
        )
        for language in corpus.languages:
            features_in_lang = document_features[
                document_features.index.isin(
                    corpus.documents[corpus.documents.lang == language].index
                )
            ]

            # Iterate over each dimension: f_entities_title, f_entities_body, etc
            for feature_name in features_in_lang.columns:

                model = self.__get_models_from_feature_name(feature_name, language)

                # Save word id and its string representation
                id_to_word = {value: key for key, value in model.vocabulary_.items()}

                # Then, transform the current dimension (f_entities_title for instance) with the model
                for index_vector, tfidf_vector in tqdm(
                    enumerate(
                        self.parallelize_dataframe(
                            features_in_lang[feature_name], model.transform
                        )
                    ),
                    total=len(features_in_lang[feature_name]),
                    desc=f"Computing TF-IDF weights ‘{feature_name}’ in ‘{language}’",
                ):
                    document_id = features_in_lang.iloc[index_vector].name
                    # Then, we build a dictionary of features with the corresponding weight. We keep only
                    # features with score higher to 0, to avoid sparse dictionaries
                    sparse_document_features = {
                        id_to_word[index]: tf_idf_weight
                        for index, tf_idf_weight in enumerate(tfidf_vector.toarray()[0])
                        if tf_idf_weight > 0
                    }
                    document_weights.at[
                        document_id, feature_name
                    ] = sparse_document_features

        return document_weights.applymap(lambda x: {} if isinstance(x, float) else x)

    @staticmethod
    def _create_tf_idf_vectoriser_and_fit_data(data: Series):
        return TfidfVectorizer(
            tokenizer=return_parameter,
            preprocessor=return_parameter,
            token_pattern=None,
        ).fit(data)


class NewsTFIDFVectoriser(TFIDFVectoriser):
    @cached_property
    def feature_names(self):
        return {
            feature.split("_")[1]
            for feature in NewsCorpusWithSparseFeatures.FEATURE_COLUMNS
        }

    def __init__(self, features_file_path: Path, languages: List[ISO6393LanguageCode]):
        features = pandas.read_csv(
            features_file_path,
            converters={
                "tokens_title": literal_eval,
                "lemmas_title": literal_eval,
                "entities_title": literal_eval,
                "tokens_text": literal_eval,
                "lemmas_text": literal_eval,
                "entities_text": literal_eval,
            },
            index_col=0,
        )
        self._languages = languages
        for language in self._languages:
            for feature_name in self.feature_names:
                logger.info(
                    "→ Loading TF-IDF model in ‘%s’ for ‘%s’", language, feature_name
                )
                self.__setattr__(
                    f"{feature_name}_{language}_model",
                    self._create_tf_idf_vectoriser_and_fit_data(
                        features[f"{feature_name}_title"]
                        + features[f"{feature_name}_text"]
                    ),
                )
        del features


class TweetsTFIDFVectoriser(TFIDFVectoriser):
    @cached_property
    def feature_names(self):
        return {
            feature.split("_")[1]
            for feature in TwitterCorpusWithSparseFeatures.FEATURE_COLUMNS
        }

    @cached_property
    def languages(self):
        return self._languages

    def __init__(self, features_file_path: Path, languages: List[ISO6393LanguageCode]):
        features = pandas.read_csv(
            features_file_path,
            converters={
                "tokens_text": literal_eval,
                "lemmas_text": literal_eval,
                "entities_text": literal_eval,
            },
            index_col=0,
        )
        self._languages = languages
        for language in self._languages:
            for feature_name in self.feature_names:
                logger.info(
                    "→ Loading TF-IDF model in ‘%s’ for ‘%s’", language, feature_name
                )
                self.__setattr__(
                    f"{feature_name}_{language}_model",
                    self._create_tf_idf_vectoriser_and_fit_data(
                        features[f"{feature_name}_text"]
                    ),
                )
        del features


def main():
    parser = argparse.ArgumentParser(
        description="Take a document corpus (in pickle format) and perform TF-IDF lookup in "
        "order to extract the feature weights."
    )

    # Input arguments
    parser.add_argument(
        "--corpus",
        type=str,
        required=True,
        help="Path to the pickle file containing the corpus to process.",
    )
    parser.add_argument(
        "--dataset-type",
        choices=["twitter", "news"],
        required=True,
        type=str,
        help="The kind of dataset to process. "
        "‘twitter’ will use the ’TwitterCorpusWithSparseFeatures’ class, the ‘NewsCorpusWithSparseFeatures’ class otherwise",
    )
    parser.add_argument(
        "--features-file",
        type=str,
        required=True,
        help="Path to the CSV file that contains the learning document features in all languages.",
    )
    parser.add_argument(
        "--output-corpus",
        type=str,
        required=True,
        help="Path where to export the new corpus with computed TF-IDF vectors.",
    )

    args = parser.parse_args()

    corpus_classes = {
        "news": NewsCorpusWithSparseFeatures,
        "twitter": TwitterCorpusWithSparseFeatures,
    }
    tfidf_vectoriser = {"news": NewsTFIDFVectoriser, "twitter": TweetsTFIDFVectoriser}
    extractors = {
        "news": NewsCorpusFeaturesExtractor,
        "twitter": TwitterCorpusFeaturesExtractor,
    }

    logger.info("Loading corpus from ’%s’ (type: ‘%s’)", args.corpus, args.dataset_type)
    corpus: SparseCorpusMixin = corpus_classes.get(args.dataset_type).from_pickle_file(
        args.corpus
    )

    logger.info("Loading TF-IDF models")
    vectoriser = tfidf_vectoriser.get(args.dataset_type)(
        args.features_file, corpus.languages
    )

    logger.info("Extracting document features in the languages of the corpus")
    features = extractors.get(args.dataset_type)().compute_document_features(corpus)

    logger.info("Computing the TF-IDF weights for each feature")
    corpus.features = vectoriser.compute_weights_for_corpus(corpus, features)

    logger.info(
        "Export the ‘%s‘ to ‘%s’",
        corpus_classes.get(args.dataset_type).__name__,
        args.output_corpus,
    )
    output_path = Path(args.output_corpus)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    corpus.as_dataframe().to_pickle(str(output_path))


if __name__ == "__main__":
    main()
