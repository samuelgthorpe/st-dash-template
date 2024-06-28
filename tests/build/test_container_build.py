"""
System tests to probe the container environment.

Note these can also be done manually with the make docker.test.shell command
to launch an interactive terminal into the container and probe the
dependencies/connections


# NOTES
# ----------------------------------------------------------------------------|


Written by Samuel Thorpe
"""


# # Imports
# -----------------------------------------------------|
import argparse
from os import environ, listdir
import numpy as np
import scipy as sp
import pandas as pd
import boto3


# # Defs
# -----------------------------------------------------|
def main(local=False):
    """Run basic checks for built container."""
    print(f'\nCHECKING LIBS\n{"-"*40}>>>')
    for mod in [np, sp, pd, boto3]:
        print(f"{mod.__name__} version: {mod.__version__}")

    # check aws credentials volumne mount
    print(f'\nCHECKING AWS CREDENTIALS\n{"-"*40}>>>')
    cfg_dir = f"{environ['HOME']}/.aws" if local else "/root/.aws"
    contents = listdir(cfg_dir)
    print(f'config path: {cfg_dir}')
    print(f'detected contents: {contents}')

    # check boto connections
    print(f'\nCHECKING AWS CONNECTION\n{"-"*40}>>>')
    test_bucket = None
    test_prefix = None
    _s3_summary(test_bucket, test_prefix)
    print('')


def _s3_summary(bucket_name, prefix):
    """List items at specified s3 location."""
    session = boto3.Session()
    resource = session.resource('s3')
    bucket = resource.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=prefix):
        print(f"{obj.key}: {obj.size} Bytes")


# # Main Entry
# -----------------------------------------------------|
if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(description='test environment')
    PARSER.add_argument("--local", action="store_true")
    ARGS = PARSER.parse_args()
    main(ARGS.local)
