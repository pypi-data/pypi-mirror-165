#!/usr/bin/env python3
#
# This file is part of the compute_dense_vectors package

# Copyright (c) 2022 − Present Guillaume Bernard <contact@guillaume-bernard.fr>
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

import argparse
import logging
from pathlib import Path

from document_tracking_resources.corpus import (
    Corpus,
    NewsCorpusWithDenseFeatures,
    TwitterCorpusWithDenseFeatures,
)
from pandas import DataFrame
from sentence_transformers import SentenceTransformer
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


def main():
    parser = argparse.ArgumentParser(
        description="Take a document corpus (in pickle format) and compute dense vectors for every feature"
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
        "‘twitter’ will use the ’TwitterCorpus’ class, the ‘Corpus’ class otherwise",
    )
    parser.add_argument(
        "--model-name",
        required=False,
        default="distiluse-base-multilingual-cased-v2",
        type=str,
        help="The name of the model that can be used to encode sentences using the S-BERT library",
    )
    parser.add_argument(
        "--output-corpus",
        type=str,
        required=True,
        help="Path where to export the new corpus with computed TF-IDF vectors.",
    )

    args = parser.parse_args()

    corpus_classes = {
        "news": NewsCorpusWithDenseFeatures,
        "twitter": TwitterCorpusWithDenseFeatures,
    }

    logger.info("Loading corpus from ’%s’ (type: ‘%s’)", args.corpus, args.dataset_type)
    corpus: Corpus = corpus_classes.get(args.dataset_type).from_pickle_file(args.corpus)

    logger.info("Loading model ‘%s’", args.model_name)
    model = SentenceTransformer(args.model_name)

    logger.info("Extracting document features")
    document_features = DataFrame(index=corpus.documents.index)
    for part_of_the_document in corpus.DOCUMENT_TEXT_CONTENT:
        document_features[f"f_{part_of_the_document}"] = corpus.documents[
            part_of_the_document
        ]

    # This is slower than a sum(axis=1) but the only way to add space between values of each column.
    if len(corpus.DOCUMENT_TEXT_CONTENT) > 1:
        document_features["f_all"] = document_features.apply(" ".join, axis=1)
        document_features = document_features.fillna("")

    logger.info("Computing features model ‘%s’", args.model_name)
    for feature_name in document_features.columns:
        features = []
        for _, document in tqdm(
            document_features.iterrows(),
            total=len(corpus),
            desc=f"Computing dense vectors for ‘{feature_name}’",
        ):
            features.append(model.encode(document[feature_name]))
        corpus.features[feature_name] = features

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
