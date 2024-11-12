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
import pandas as pd
from openai import OpenAI
from sampy.utils import load_yaml


def load_txt(filename):
    """Load text data."""
    with open(filename) as fh:
        return fh.read()


def load_json(filename):
    """Load text data."""
    with open(filename) as fh:
        return json.load(fh)


def load_data():
    """Load data."""
    data_dir = 'data/bmi'
    prompt_dir = 'templates/prompts/bmi'
    return dict(
        dfr=pd.read_csv(join(data_dir, 'dataframe.csv')),
        meta=load_yaml(join(data_dir, 'meta.yaml')),
        desc=load_json(join(data_dir, 'description.json')),
        cmd_prompt=load_txt(join(prompt_dir, 'cmd.txt')),
        chat_prompt=load_txt(join(prompt_dir, 'chat.txt'))
        )


data = load_data()
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
