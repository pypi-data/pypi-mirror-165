#
# This file is part of the document_tracking_resources project.

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

import json
from abc import ABC
from collections import defaultdict
from copy import deepcopy
from datetime import date, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from functools import cached_property, lru_cache, reduce
from statistics import mean, stdev
from typing import Dict, Iterator, List, Tuple

import numpy
import pandas
from pandas import DataFrame, Index, Series, merge

from document_tracking_resources import ISO6393LanguageCode

SUPPORTED_ISO_639_3_LANGUAGES = [ISO6393LanguageCode("eng"), ISO6393LanguageCode("spa"), ISO6393LanguageCode("deu")]


class Corpus(ABC):
    """
    A Corpus of documents.

    It has a specific range of allowed languages, some columns used to describe the content of each document,
    as well as feature columns (could be vectors of any time, on text, dates, etc.). It may also have labels, in case
    the labels of the documents are known before running any clustering algorithm.
    """

    AVAILABLE_LANGUAGES = []
    DOCUMENT_COLUMNS: List[str] = []
    DOCUMENT_TEXT_CONTENT: List[str] = []
    FEATURE_COLUMNS: List[str] = []
    GROUND_TRUTH_COLUMNS: List[str] = []

    @property
    def index(self) -> Index:
        return self.documents.index

    @property
    def beginning(self) -> datetime:
        """
        Date of the first document published in the Corpus (the lowest date)
        """
        return self.documents.date.min()

    @property
    def end(self) -> datetime:
        """
        Date of the last document published in the Corpus (the highest date)
        """
        return self.documents.date.max()

    @property
    def nb_unique_gold_clusters(self) -> int:
        """
        The number of unique clusters
        """
        return self.labels.nunique()

    @cached_property
    def languages(self) -> List[ISO6393LanguageCode]:
        """
        The different languages in which the documents are written in.
        """
        return [ISO6393LanguageCode(language) for language in self.documents.lang.unique().tolist()]

    def __init__(
        self,
        documents: DataFrame,
        features: DataFrame,
        labels: DataFrame,
        iso_639_3_language_code: ISO6393LanguageCode = None,
    ):
        assert documents.index.equals(features.index) and documents.index.equals(labels.index)

        # Sub-select according to the language given as parameter.
        if iso_639_3_language_code is not None:
            self.documents: DataFrame = documents[documents.lang == iso_639_3_language_code]
            self.features: DataFrame = features[documents.lang == iso_639_3_language_code]
            self.labels: DataFrame = labels[documents.lang == iso_639_3_language_code]
        else:
            self.documents: DataFrame = documents
            self.features: DataFrame = features
            self.labels: DataFrame = labels

        # If the size of the corpus is only one, do squeeze() the series
        # to prevent from multiple failures with pandas
        if len(self.labels) > 1:
            self.labels: Series = self.labels.squeeze()

        # Convert indexes to integers, there are generally raw objects
        self.documents.index = self.documents.index.astype(int)
        self.features.index = self.features.index.astype(int)
        self.labels.index = self.labels.index.astype(int)
        self.labels = self.labels.astype(int)

        # Reorder documents according to date
        self.documents = self.documents.sort_values("date")
        self.features = self.features.reindex(self.documents.index)
        self.labels = self.labels.reindex(self.documents.index)

    @classmethod
    def from_pickle_file(
        cls, corpus_pickle_file: str, iso_639_3_language_code: ISO6393LanguageCode = None
    ) -> "Corpus":
        """
        Load a corpus from a DataFrame pickle file.

        :param corpus_pickle_file:  path to the pickle file containing the DataFrame.
        :param iso_639_3_language_code: the language used to sub-select the corpus documents. Can be left None to
        keep all the documents.
        :return: a Corpus instance made from the DataFrame file.
        """
        dataset: DataFrame = pandas.read_pickle(corpus_pickle_file)
        return cls.from_dataframe(dataset, iso_639_3_language_code)

    @classmethod
    def from_dataframe(cls, dataframe: DataFrame, iso_639_3_language_code: ISO6393LanguageCode = None) -> "Corpus":
        """
        Convert a pandas.DataFrame corpus into a Corpus object. The columns of the DataFrame must match the expected
        columns of the Corpus itself. Please read the class constant variables to know which columns are expected.

        :param dataframe: the dataframe to convert into Corpus
        :param iso_639_3_language_code: the language used to sub-select the corpus documents. Can be left None to
        keep all the documents.
        :return: a Corpus instance made from the DataFrame.
        """
        documents = dataframe[cls.DOCUMENT_COLUMNS]
        labels = dataframe[cls.GROUND_TRUTH_COLUMNS]

        # It may happen that no feature is provided with the corpus, if it’s a corpus without features
        if len(dataframe.columns.intersection(cls.FEATURE_COLUMNS)) == len(cls.FEATURE_COLUMNS):
            features = dataframe[cls.FEATURE_COLUMNS].reindex(
                sorted(dataframe[cls.FEATURE_COLUMNS].columns), axis=1
            )  # sort columns by name
        else:
            features = DataFrame(index=documents.index, columns=cls.FEATURE_COLUMNS)
        features = features.applymap(
            lambda x: {} if x is None else x
        ).applymap(  # replace all None with empty dictionaries
            lambda x: {} if isinstance(x, float) else x
        )  # if it’s a NaN as well

        return cls(documents, features, labels, iso_639_3_language_code)

    def sample(self, frac: float = 0.5, random_state: int = 0) -> Tuple["Corpus", "Corpus"]:
        """
        Subsample the Corpus into two parts, which are copies of this corpus, splitting with a fraction. The dataset
        is split into two according to this fraction and both resulting corpora are returned.

        :param frac: the fraction of the corpus to split the original corpus. The first Corpus will be the part below
        the fraction, the other corpus will be the other part.
        :param random_state: the random state to use in random sample operations.
        :return: the two sub-sampled corpus, split according to the frac parameter.
        """
        if not 0 < frac < 1:
            raise ValueError("The fraction can only be comprised between 0 and 1.")

        first, second = deepcopy(self), deepcopy(self)

        index_for_first_sample = self.documents.sample(frac=frac, random_state=random_state).index
        first.documents = self.documents[self.documents.index.isin(index_for_first_sample)]
        first.features = self.features[self.features.index.isin(index_for_first_sample)]
        first.labels = self.labels[self.labels.index.isin(index_for_first_sample)]

        index_for_second_sample = self.documents.index.difference(index_for_first_sample)
        second.documents = self.documents[self.documents.index.isin(index_for_second_sample)]
        second.features = self.features[self.features.index.isin(index_for_second_sample)]
        second.labels = self.labels[self.labels.index.isin(index_for_second_sample)]

        return first, second

    def sample_with_dates(self, day_begin: date, day_end: date) -> "Corpus":
        """
        Sub-sample the Corpus in multiple Corpus windows, comprised between two dates.

        :param day_begin: the first day (including it) of the sub-Corpus window.
        :param day_end: the last day (including it) of the sub-Corpus window.
        :return: a sub-sample corpus, with documents released between (including them) the two dates.
        """
        index_of_subset = self.documents[
            (self.documents.date.dt.date >= day_begin) & (self.documents.date.dt.date <= day_end)
        ].index
        documents = self.documents[self.documents.index.isin(index_of_subset)]
        features = self.features[self.features.index.isin(index_of_subset)]
        labels = self.labels[self.labels.index.isin(index_of_subset)]
        return self.__class__(documents, features, labels)

    def as_dataframe(self) -> DataFrame:
        """
        Convert the Corpus object into a pandas.DataFrame instance. This merges the Corpus document, features and
        labels columns into one DataFrame.
        """
        return reduce(
            lambda left, right: merge(left, right, left_index=True, right_index=True),
            [self.documents, self.features, self.labels],
        )

    def iterate_over_windows(self, bucket_size_in_days: int, bucket_overlap_ratio: float) -> Iterator["Corpus"]:
        """
        Iterate over the Corpus according to time windows. Given a window size and a percentage of allowed overlapping,
        splits the original Corpus in multiple sub-Corpora. For instance, splits the Corpus in windows of size = 6 days
        with 25% (0.25) of every window covering its previous one.

        :param bucket_size_in_days: the number of days that last the size of the window
        :param bucket_overlap_ratio: the ratio of overlap over the windows.
        :return: an iterator over the Corpus, giving sub-Corpora split into windows.
        """
        for first_day, last_day in Corpus.__generate_time_windows_with_boundaries(
            self.documents.date.min(), self.documents.date.max(), bucket_size_in_days, bucket_overlap_ratio
        ):
            yield self.sample_with_dates(first_day, last_day)

    @lru_cache(maxsize=None)
    def nb_over_time_windows(self, bucket_size_in_days: int, bucket_overlap_ratio: float) -> int:
        """
        The number of windows computed by the iterate_over_windows function. Parameters are the same.
        """
        return len(
            Corpus.__generate_time_windows_with_boundaries(
                self.documents.date.min(), self.documents.date.max(), bucket_size_in_days, bucket_overlap_ratio
            )
        )

    def split_according_to_labels(self, frac: float = 0.3) -> Tuple["Corpus", "Corpus"]:
        """
        Splits the Corpus into two sub-corpus, with a split made on a fraction of labels. This allows to split the
        data with full clusters of documents, instead of randomly splitting on documents.
        """
        if not 0 < frac < 1:
            raise ValueError("The fraction can only be comprised between 0 and 1.")

        existing_labels = self.labels.unique().tolist()
        split_index = len(existing_labels) // Fraction(Decimal(frac)).limit_denominator(1000).denominator
        labels_first_part, labels_second_part = existing_labels[split_index:], existing_labels[:split_index]

        # Save indexes of both parts
        index_first_part = self.labels[self.labels.isin(labels_first_part)].index
        index_second_part = self.labels[self.labels.isin(labels_second_part)].index

        first, second = deepcopy(self), deepcopy(self)
        first.documents = self.documents[self.documents.index.isin(index_first_part)]
        first.features = self.features[self.features.index.isin(index_first_part)]
        first.labels = self.labels[self.labels.index.isin(index_first_part)]
        second.documents = self.documents[self.documents.index.isin(index_second_part)]
        second.features = self.features[self.features.index.isin(index_second_part)]
        second.labels = self.labels[self.labels.index.isin(index_second_part)]

        return first, second

    @staticmethod
    @lru_cache(maxsize=None)
    def __generate_time_windows_with_boundaries(
        day_begin: datetime, day_end: datetime, bucket_size: int, bucket_overlap_ratio: float
    ) -> List[Tuple[date, date]]:
        """
        From one date, to another, get the list of all the time windows, in days, comprised between
        the two dates. The size of the window as well as overlapping can be tweaked to adjust the
        window sizes.

        :param day_begin: the starting day of the time windows generation
        :param day_end: the ending day of the time windows generation
        :param bucket_size: the number of days that will be included in every time window (except the last if shorter)
        :param bucket_overlap_ratio: the ratio, comprised between 0 and 1 (as a percentage) to indicate how windows
        will overlap. 1 means windows will fully overlap (which will produce an infinite loop), 0 means no overlapping
        at all so distinct windows without any day in common.
        """

        # All the days between two dates (+ 2 to include the starting and ending days)
        days = [(day_begin + timedelta(days=x)).date() for x in range((day_end - day_begin).days + 2)]

        # Generate all the windows
        windows = []
        for index in range(0, len(days), int(bucket_size * (1 - bucket_overlap_ratio))):
            if index + bucket_size < len(days):
                windows.append((days[index], days[index + bucket_size - 1]))
            else:
                windows.append((days[index], max(days)))
                break  # This turn is the last

        return windows

    def __iter__(self):
        for index in self.documents.index:
            yield self.documents.loc[index], self.features.loc[index], self.labels.loc[index]

    def __len__(self):
        return len(self.documents)

    def __str__(self):
        return f"Corpus ({len(self)}) from {self.beginning.strftime('%Y-%m-%d')} to {self.end.strftime('%Y-%m-%d')}"


class SparseCorpusMixin(Corpus, ABC):
    pass


class DenseCorpusMixin(Corpus, ABC):
    pass


class NewsCorpus(Corpus, ABC):
    """
    A Corpus of news/press article documents, with at least a publication date, an article title, content and language.
    The source of the document is usually a URL where the document can be found.
    """

    DOCUMENT_COLUMNS: List[str] = [
        "date",
        "lang",
        "title",
        "text",
        "source",
    ]
    DOCUMENT_TEXT_CONTENT: List[str] = ["title", "text"]
    GROUND_TRUTH_COLUMNS: List[str] = ["cluster"]


class NewsCorpusWithSparseFeatures(NewsCorpus, SparseCorpusMixin):
    """
    A NewsCorpusWithSparseFeatures is a kind of Corpus which has 9 dimensions for its features. They are sparse
    TF-IDF matrices, on the title of the document, its content and the concatenation of the title and the content.
    For each, TF-IDF weights are expected to be computed on entities, lemmas and tokens.

        Miranda, Sebastião, Artūrs Znotiņš, Shay B. Cohen, et Guntis Barzdins. 2018.
        ‘Multilingual Clustering of Streaming News’. In 2018 Conference on Empirical Methods in Natural
        Language Processing, 4535‑44. Brussels, Belgium: Association for Computational Linguistics.
        https://www.aclweb.org/anthology/D18-1483/.
    """

    AVAILABLE_LANGUAGES = SUPPORTED_ISO_639_3_LANGUAGES

    FEATURE_COLUMNS: List[str] = [
        "f_entities_all",
        "f_entities_text",
        "f_entities_title",
        "f_lemmas_all",
        "f_lemmas_text",
        "f_lemmas_title",
        "f_tokens_all",
        "f_tokens_text",
        "f_tokens_title",
    ]

    @classmethod
    def from_json_files(
        cls, dataset_filename: str, document_weights_filename: str, iso_639_3_language_code: ISO6393LanguageCode = None
    ) -> "NewsCorpusWithSparseFeatures":
        """
        Load a corpus from JSON flat files. The JSON files that are mentioned here are the one provided by Miranda
        et al. in their original paper and coming from the Priberam servers.
        """
        loaded_corpus = cls.__get_corpus_from_dataset_file(dataset_filename)
        loaded_features = cls.__get_corpus_features_from_dataset_file(document_weights_filename)

        features = DataFrame.from_dict(
            {
                document_id: features
                for document_id, features in loaded_features.items()
                if document_id in loaded_corpus.index
            },
            orient="index",
        )

        # Remove NaN values
        features = features.replace({numpy.nan: None})

        # Rename the columns
        updated_feature_names = [f"f_{original_feature_name.lower()}" for original_feature_name in features.columns]
        assert sorted(updated_feature_names) == sorted(cls.FEATURE_COLUMNS)
        features = features.rename(columns=dict(zip(sorted(features.columns), sorted(cls.FEATURE_COLUMNS))))

        documents = loaded_corpus[cls.DOCUMENT_COLUMNS].sort_index()
        features = features.sort_index()
        labels = loaded_corpus[cls.GROUND_TRUTH_COLUMNS].sort_index()

        return cls(documents, features, labels, iso_639_3_language_code)

    @staticmethod
    def __get_corpus_from_dataset_file(dataset_filename: str) -> DataFrame:
        """
        Load the corpus from a filename. The input corpus is one of the files provided by Miranda et al. from their
        servers, as ‘dataset.dev.json’ or ‘dataset.test.json’.
        """
        with open(dataset_filename, encoding="utf-8") as dataset_file:
            dataset_json = json.load(dataset_file)
            corpus = DataFrame.from_dict(dataset_json)
            corpus = corpus.set_index("id")
            # We drop all the documents which are not in the list of ‘Authorised languages’.
            corpus.drop(
                corpus[~corpus.lang.isin(NewsCorpusWithSparseFeatures.AVAILABLE_LANGUAGES)].index, inplace=True
            )
            corpus = corpus.reindex(
                columns=NewsCorpusWithSparseFeatures.DOCUMENT_COLUMNS
                + NewsCorpusWithSparseFeatures.GROUND_TRUTH_COLUMNS
            )
            corpus.date = pandas.to_datetime(corpus.date)
            return corpus

    @staticmethod
    def __get_corpus_features_from_dataset_file(clustering_filename: str) -> Dict[str, Dict[str, float]]:
        """
        Load the model TF-IDF weights from a filename. The input corpus is one of the files provided by Miranda et al.
        from their servers, as ‘clustering.dev.json’ or ‘clustering.test.json’.
        """
        corpus_features = defaultdict(dict)
        with open(clustering_filename, errors="ignore", mode="r", encoding="utf-8") as data_file:
            for line in data_file:
                tok_ner_document = json.loads(line)
                # Some features are empty for some documents, we do not add them
                for tok_ner_feature_name, tok_ner_feature_vector in tok_ner_document["features"].items():
                    if tok_ner_feature_vector is not None:
                        corpus_features[tok_ner_document.get("id")][tok_ner_feature_name] = tok_ner_feature_vector
            return corpus_features


class NewsCorpusWithDenseFeatures(NewsCorpus, DenseCorpusMixin):
    """
    A NewsCorpusWithDenseFeatures is a NewsCorpus with features that are logits, so dense vectors that represent each
    document or each part of the document. It is expected to have three vectors, one for the title of the document,
    one for the text and one for the concatenation of them both.
    """

    AVAILABLE_LANGUAGES = SUPPORTED_ISO_639_3_LANGUAGES

    FEATURE_COLUMNS: List[str] = [
        "f_title",
        "f_text",
        "f_all",
    ]


class TwitterCorpus(Corpus, ABC):
    """
    A Corpus for Tweets, short messages from Twitter. Each document (so Tweet) has at least a publication date,
    a language in which the Tweet is written in, a source and the Tweet text itself.
    """

    DOCUMENT_COLUMNS: List[str] = [
        "date",
        "lang",
        "text",
        "source",
    ]
    DOCUMENT_TEXT_CONTENT: List[str] = ["text"]
    GROUND_TRUTH_COLUMNS: List[str] = ["cluster"]


class TwitterCorpusWithSparseFeatures(TwitterCorpus, SparseCorpusMixin):
    """
    A Twitter Corpus with sparse columns only has a single field of text, the Tweet content. It then only has
    three dimensions (similarly as in the NewsCorpusWithSparseFeatures), TF-IDF vectors for entities, lemmas and
    tokens.
    """

    FEATURE_COLUMNS: List[str] = [
        "f_entities_text",
        "f_lemmas_text",
        "f_tokens_text",
    ]


class TwitterCorpusWithDenseFeatures(TwitterCorpus, DenseCorpusMixin):
    """
    A Twitter Corpus with dense features has only one logit feature, the vectorised representation of the text through
    a dense model.
    """

    FEATURE_COLUMNS: List[str] = [
        "f_text",
    ]


class CorpusStatistics:
    def __init__(self, corpus: "Corpus"):
        self._corpus = corpus

    def info_clusters(self) -> DataFrame:
        languages_in_statistics = self._corpus.languages.copy()

        if len(languages_in_statistics) > 1:
            languages_in_statistics.extend([ISO6393LanguageCode("all")])

        corpus_statistics = DataFrame(index=Index(sorted(languages_in_statistics), name="Language"))

        for language in self._corpus.languages:

            corpus_statistics.at[language, "Nb. of documents"] = len(
                self._corpus.documents[self._corpus.documents.lang == language]
            )
            clusters_in_lang = self._corpus.labels[self._corpus.documents.lang == language]
            clusters_size_in_lang = [len(group) for _, group in clusters_in_lang.groupby(clusters_in_lang)]

            for feature in self._corpus.DOCUMENT_TEXT_CONTENT:
                documents_in_lang = self._corpus.documents[self._corpus.documents.lang == language]
                corpus_statistics.at[language, f"Avg. length for ’{feature}’"] = (
                    documents_in_lang[feature].apply(lambda x: len(x)).mean()
                )
                corpus_statistics.at[language, f"Avg. length for ’{feature}’ (std)"] = (
                    documents_in_lang[feature].apply(lambda x: len(x)).std()
                )

            corpus_statistics.at[language, "Nb. of clusters"] = len(
                self._corpus.labels[self._corpus.documents.lang == language].unique()
            )
            corpus_statistics.at[language, "Avg. cluster size"] = round(mean(clusters_size_in_lang))
            corpus_statistics.at[language, "Avg. cluster size (std)"] = round(stdev(clusters_size_in_lang))

        if len(self._corpus.languages) > 1:
            corpus_statistics.at["all", "Nb. of clusters"] = len(self._corpus.labels.unique())
            corpus_statistics.at["all", "Nb. of documents"] = len(self._corpus)

            # Average cluster size
            clusters_size = [len(group) for _, group in self._corpus.labels.groupby(self._corpus.labels)]
            corpus_statistics.at["all", "Avg. cluster size"] = round(mean(clusters_size))
            corpus_statistics.at["all", "Avg. cluster size (std)"] = round(stdev(clusters_size))

            for feature in self._corpus.DOCUMENT_TEXT_CONTENT:
                corpus_statistics.at["all", f"Avg. length for ’{feature}’"] = (
                    self._corpus.documents[feature].apply(lambda x: len(x)).mean()
                )
                corpus_statistics.at["all", f"Avg. length for ’{feature}’ (std)"] = (
                    self._corpus.documents[feature].apply(lambda x: len(x)).std()
                )

        return corpus_statistics.astype(int)
