"""
Insert description.

# NOTES
# ----------------------------------------------------------------------------|


Written July 14, 2024
By Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
import os
from os.path import join
import json
import yaml
import pandas as pd
from ucimlrepo import fetch_ucirepo
from openai import OpenAI


def load_txt(filename):
    """Load text data."""
    with open(filename) as fh:
        return fh.read()


def load_json(filename):
    """Load text data."""
    with open(filename) as fh:
        return json.load(fh)


def load_yaml(filename):
    """Load specified yaml file."""
    with open(filename, 'r') as file:
        return yaml.safe_load(file)


def load_data():
    """Load data."""
    data_dir = 'data/bmi'
    prompt_dir = 'templates/prompts/bmi'
    data = dict(
        dfr=load_uci_dataset(),
        meta=load_yaml(join(data_dir, 'meta.yaml')),
        desc=load_json(join(data_dir, 'description.json')),
        cmd_prompt=load_txt(join(prompt_dir, 'cmd.txt')),
        chat_prompt=load_txt(join(prompt_dir, 'chat.txt'))
        )
    data['base_prompt'] = _build_base_prompt(data)

    return data


def load_uci_dataset():
    """Return the dataset as dataframe."""
    dat = fetch_ucirepo(id=462)
    dfr = dat.data.features
    cols = ['date', 'drugName', 'condition', 'rating', 'usefulCount', 'review']
    dfr['dt'] = pd.to_datetime(dfr.date, format="%d-%b-%y")
    dfr = dfr.sort_values('dt', ignore_index=True)
    return dfr[cols]


def _build_base_prompt(data):
    """Return the build prompt string which specifies data context."""
    summary = data['desc']['header'][13:-1]  # Hack
    col_desc = _build_column_description(data['meta'])
    url = data['meta']['url']

    return data['desc']['prompt_template'].format(summary, col_desc, url)


def _build_column_description(meta):
    """Return string describing columns in human language."""
    col_str = ''
    for col, dct in meta['data'].items():
        col_str += f'The "{col}" column describes {dct["desc"]}. '
        if "units" in dct:
            col_str += f'The units are given in {dct["units"]}. '
        col_str += f'It is of type {dct["type"]}. '
        if dct['type'].lower() == 'categorical' and 'categories' in dct:
            cats = ', '.join(dct['categories'])
            col_str += f'The associated data categories are: {cats}. '
        if dct['type'].lower() == 'index' and 'labels' in dct:
            col_str += f'It indexes categories in the {dct["index"]} column. '
            cat_map = [f'{k} = {v}' for k, v in dct["labels"].items()]
            col_str += f'The mapping is given by: {", ".join(cat_map)}.'
        if dct['type'].lower() == 'datetime':
            col_str += 'Please interpret these strings as datetime objects '
            col_str += 'where necessary. '

    return col_str


data = load_data()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
