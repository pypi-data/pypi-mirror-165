#!/usr/bin/env python3
#
# This file is part of the document_processing project.
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
import multiprocessing
import string
import unicodedata
from math import floor
from typing import Callable, Generator, List, Tuple

import spacy
from pandas import Series
from spacy.tokens import Doc


unicode_punctuation_table = str.maketrans("", "", string.punctuation)


def preprocess_list_of_texts(texts: List[str]):
    normalized_tokens = [
        unicodedata.normalize("NFKD", text.lower().translate(unicode_punctuation_table))
        .encode("ASCII", "ignore")
        .decode("utf-8")
        for text in texts
    ]
    tokens_without_number_except_year = [
        token
        for token in normalized_tokens
        if token.isnumeric() and len(token) == 4 and 2000 < int(token) < 2020 or not token.isnumeric()
    ]
    return [token for token in tokens_without_number_except_year if len(token) > 1]


def preprocess_list_of_tweets(tweets: List[str]):
    """Preprocess a list of tokens, in order to apply changes on token string."""
    tokens = preprocess_list_of_texts(tweets)
    tokens_without_http_link = [token for token in tokens if "https" not in token]
    return tokens_without_http_link


def get_tokens_lemmas_entities_from_document(document: Doc, preprocessor: Callable = preprocess_list_of_texts):

    # We select only tokens which are relevant and which are NOT entities
    # (because entities can be represented by multiple tokens)
    tokens_to_select = [
        token
        for token in document
        if not any(
            [
                token.is_stop,
                token.is_punct,
                token.is_quote,
                token.is_space,
                token.is_bracket,
            ]
        )
        and token.ent_iob_ == "O"
        and len(token.text) > 1
    ]

    tokens = preprocessor([token.text for token in tokens_to_select])
    lemmas = preprocessor([token.lemma_ for token in tokens_to_select])
    entities = preprocessor(
        [entity.text for entity in document.ents if len(entity.text) > 1 and entity.label_ in ["GPE", "ORG", "PER"]]
    )
    all_entities = preprocessor(
        [entity.text for entity in document.ents if len(entity.text) > 1]
    )

    # Then, we add entities to the title and lemmas
    return tokens + all_entities, lemmas + all_entities, entities


def process_documents(documents: Series, spacy_model_name: str) -> Generator[Tuple[int, Doc], None, None]:
    documents_index = list(documents.index)
    language = spacy.load(spacy_model_name)
    for document_index, document in enumerate(
        language.pipe(
            documents,
            n_process=floor(0.75 * multiprocessing.cpu_count()),
        ),
    ):
        yield documents_index[document_index], document
