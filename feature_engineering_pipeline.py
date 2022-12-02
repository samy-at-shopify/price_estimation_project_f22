# standard library dependencies
import functools
from datetime import datetime
from collections import namedtuple
from typing import Iterable, List, Any, Mapping, Union, Tuple, Callable

# external dependencies
import dill
import numpy as np
import pandas as pd
import shopify_merlin.trino as trino

from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

import spacy

@functools.lru_cache
def load_raw_dataset( trino_query: str = None,
                      columns_to_keep: List[str] = None,
                      columns_to_drop: List[str] = None,
                      deduplicate_using: Iterable[str] = None,
                      replace_missing_values_with: Any = " ",
                      concatenate_options_columns: bool = True,
                      add_topmost_product_class: bool = True) -> pd.DataFrame:
  if trino_query is None:
    trino_query = """SELECT preds.confidence, taxonomy.category_string, sample_dataset.*
      FROM hive.product_classification.predictions AS preds
      JOIN hive.insights.google_product_taxonomy AS taxonomy
        ON preds.predicted_category_id = taxonomy.category_id
      JOIN hive.scratch.fair_price_pred_US as sample_dataset
        ON preds.product_id = sample_dataset.product_id
      ORDER BY sample_dataset.product_id
      """
  raw_dataset: pd.DataFrame = trino.trino_query(trino_query)
  if columns_to_keep is not None:
    raw_dataset = raw_dataset[columns_to_keep]
  if concatenate_options_columns:
    raw_dataset["options"] = raw_dataset[["option1", "option2", "option3"]].fillna(
      replace_missing_values_with
    ).astype(
      str
    ).agg(
      " ".join,
      axis = 1
    )
  if add_topmost_product_class:
    raw_dataset["root_product_category"] = [ first for first, *rest in
                                            raw_dataset["category_string"].str.split(" > ") ]
  if columns_to_drop is None:
    columns_to_drop = [
      "compare_at_price",
      "inventory_management",
      "option1",
      "option2",
      "option3",
      "body_html",
      "product_type",
      "custom_product_type",
      "handle",
      "shop_id",
    ]
  if columns_to_drop is not None:
    raw_dataset = raw_dataset.drop(
      columns_to_drop,
      axis="columns"
    )
  if deduplicate_using is None:
    deduplicate_using = ["product_id", "product_variant_id"]
  raw_dataset = raw_dataset.drop_duplicates(
    subset = deduplicate_using,
    keep = "first"
  ).reset_index(drop = True)
  raw_dataset.fillna(
    replace_missing_values_with,
    inplace = True
  )
  return raw_dataset.sort_values("product_id")


def preprocess_text_data(data: Union[Mapping[str, Any], pd.DataFrame],
                         text_features: List[str] = None,
                         nlp_model = None,
                         stopwords: Iterable[str] = None,
                         preprocessing_steps_to_skip: List[str] = None,
                         verbose: bool = True) -> Mapping[str,List[str]]:
  if text_features is None:
    text_features = [ 'category_string', 'product_title', 'variant_title', 'tag_string', 'options' ]
  assert all([text_column in data for text_column in text_features])
  text_features = sorted(text_features)
  if nlp_model is None:
    nlp_model = spacy.load("en_core_web_sm")
  if stopwords is None:
    stopwords = nlp_model.Defaults.stop_words
  if preprocessing_steps_to_skip is None:
    preprocessing_steps_to_skip = [
      "tagger",
      "parser",
      "ner",
      "entity_linker",
      "textcat",
      "textcat_multilabel ",
      "trainable_lemmatizer",
      "morphologizer",
      "attribute_ruler senter ",
      "sentencizer ",
      "tok2vec",
      "transformer",
    ]

  processed_text_data = dict()
  for text_feature_to_process in text_features:
    if verbose:
      iterator = tqdm(
          nlp_model.pipe(data[text_feature_to_process], disable=preprocessing_steps_to_skip),
          total = len(data),
          leave = False,
          desc = f"processing {text_feature_to_process}... "
      )
    else:
      iterator = nlp_model.pipe(data[text_feature_to_process], disable=preprocessing_steps_to_skip)
    processed_column_data = []
    for doc in iterator:
      processed_column_data.append([  token.lemma_ for token in doc
                                      if (not token.is_punct) and (token.lemma_ not in stopwords) and (not token.is_space)])
    processed_text_data[text_feature_to_process] = processed_column_data
    print(f"processed {text_feature_to_process}.")

  return processed_text_data

def vectorize_text_data(processed_text_column_data: Mapping[str,List[List[str]]],
                        vectorizer_class: Callable = CountVectorizer,
                        verbose: bool = True,
                        **kwargs) -> Tuple[Mapping[str,Union[CountVectorizer, TfidfVectorizer]], Mapping[str,np.ndarray]]:
  text_column_vectorizers = dict()
  vectorized_text_column_arrays = dict()
  if verbose:
    iterator = tqdm(processed_text_column_data.items())
  else:
    iterator = processed_text_column_data.items()
  for text_column_name, text_column_token_lists in iterator:
    vectorizer = vectorizer_class(
      lowercase = False,
      preprocessor = None,
      tokenizer = lambda list_of_tokens: [ token.lower() for token in list_of_tokens ],
      **kwargs
    )
    vectorized_document_tokens: np.ndarray =  vectorizer.fit_transform(text_column_token_lists)
    text_column_vectorizers[text_column_name] = vectorizer
    vectorized_text_column_arrays[text_column_name] = vectorized_document_tokens
  return text_column_vectorizers, vectorized_text_column_arrays

def categorize_data(data: Union[Mapping[str, Any],pd.DataFrame],
                    encoder: Callable = LabelEncoder,
                    categorical_features: List[str] = None) -> Tuple[Mapping[str,Callable],Mapping[str,np.ndarray]]:
  if categorical_features is None:
    categorical_features = ['fulfillment_service', 'vendor']
  assert all([categorical_column in data for categorical_column in categorical_features])
  categorical_column_encoders = dict()
  categorical_column_labels = dict()
  for categorical_column_name in tqdm(categorical_features):
    e = encoder()
    labels = e.fit_transform(data[categorical_column_name])
    categorical_column_encoders[categorical_column_name] = e
    categorical_column_labels[categorical_column_name] = labels
  return categorical_column_encoders, categorical_column_labels

ProductCategoryAssets = namedtuple(
  "ProductCategoryAssets",
  "processed_dataset text_preprocessor text_vectorizers categorical_encoders"
)

def feature_engineering_pipeline(
  # load_data
  trino_query: str = None,
  columns_to_keep: List[str] = None,
  columns_to_drop: List[str] = None,
  deduplicate_using: Iterable[str] = None,
  replace_missing_values_with: Any = " ",
  concatenate_options_columns: bool = True,
  # preprocess text data
  text_features: List[str] = None,
  nlp_model = None,
  stopwords: Iterable[str] = None,
  preprocessing_steps_to_skip: List[str] = None,
  verbose: bool = True,
  # vectorize text data
  vectorizer_class: Callable = CountVectorizer,
  vectorizer_kwargs: Mapping = None,
  # encode categorical data
  categorical_features: List[str] = None,
  categorical_encoder: Callable = LabelEncoder,
  save: bool = True) -> Mapping[str, ProductCategoryAssets]:

  raw_dataset: pd.DataFrame = load_raw_dataset(
    trino_query = trino_query,
    columns_to_keep = columns_to_keep,
    columns_to_drop = columns_to_drop,
    deduplicate_using = deduplicate_using,
    replace_missing_values_with = replace_missing_values_with,
    concatenate_options_columns = concatenate_options_columns,
  )

  preprocessed_categorical_data: Tuple[Mapping[str,Callable],Mapping[str,np.ndarray]] = categorize_data(
    raw_dataset,
    categorical_features = categorical_features,
    encoder = categorical_encoder,
  )
  categorical_column_encoders, categorical_column_labels = preprocessed_categorical_data
  categorical_column_labels = pd.DataFrame(categorical_column_labels)

  preprocessed_text_data: Mapping[str,List[str]] = preprocess_text_data(
    raw_dataset,
    text_features = text_features,
    nlp_model = nlp_model,
    stopwords = stopwords,
    preprocessing_steps_to_skip = preprocessing_steps_to_skip,
    verbose = verbose,
  )
  preprocessed_text_data = pd.DataFrame(preprocessed_text_data)

  if vectorizer_kwargs is None:
    vectorizer_kwargs = {"min_df": 0.01}

  all_product_category_assets: Mapping[str, ProductCategoryAssets] = dict()
  if verbose:
    iterator = tqdm(raw_dataset.groupby("root_product_category"))
  else:
    iterator = raw_dataset.groupby("root_product_category")
  for root_product_category, subdf in iterator:
    row_indices = subdf.index
    preprocessed_text_data_in_root_product_category: pd.DataFrame = preprocessed_text_data.loc[row_indices]
    text_vectorization_output: Tuple[Mapping[str,Union[CountVectorizer, TfidfVectorizer]], Mapping[str,np.ndarray]] = vectorize_text_data(
      preprocessed_text_data_in_root_product_category,
      vectorizer_class = vectorizer_class,
      **vectorizer_kwargs
    )
    text_column_vectorizers, vectorized_text_column_arrays = text_vectorization_output
    vectorized_text_column_df = pd.DataFrame(
      np.hstack([ vectorized_text_column_arrays[feature_column].toarray()
                  for feature_column in sorted(vectorized_text_column_arrays.keys()) ]),
      columns = [ f"{feature_column}[{token}]"
                  for feature_column in sorted(vectorized_text_column_arrays.keys())
                  for token in text_column_vectorizers[feature_column].get_feature_names() ]
    )
    processed_subdf = subdf[['confidence', 'price', 'product_id', 'product_variant_id']].copy(deep = True)
    processed_subdf = processed_subdf.join(categorical_column_labels.loc[row_indices]).reset_index(drop = True)
    processed_subdf = pd.concat([processed_subdf, vectorized_text_column_df], axis = 1)
    all_product_category_assets[root_product_category] = ProductCategoryAssets(
      processed_dataset = processed_subdf.copy(deep = True),
      text_preprocessor = preprocess_text_data,
      text_vectorizers = text_column_vectorizers,
      categorical_encoders = categorical_column_encoders
    )
  if save:
    with open(f"./app/{datetime.now().strftime('%Y%m%d%H%M%S')}_all_product_category_assets.pkl", "wb") as handle:
      dill.dump(
          all_product_category_assets,
          handle,
          protocol = dill.HIGHEST_PROTOCOL
      )
    with open(f"./app/{datetime.now().strftime('%Y%m%d%H%M%S')}_all_product_category_assets_backup.pkl", "wb") as handle:
      dill.dump(
          all_product_category_assets,
          handle,
          protocol = dill.HIGHEST_PROTOCOL
      )

  return all_product_category_assets
