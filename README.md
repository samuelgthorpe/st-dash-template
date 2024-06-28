# st-dash-template

This repo houses a template prototype experiment for research/development. Experiments are configured in parameterized blocks which run in sequence, as detailed in st_dash_template/cfg.yaml


### Usage

Pull repo, create virtual environment with necessary dependencies installed (see below for details) and execute the main script via:

`python st_dash_template/main.py`

or its alias:

`make run.local`

Alternatively, build Docker container with necessary dependencies installed (see below for details) and execute via:

`make docker.run.local`


## Setup, Installation, and Testing (BOILERPLATE)

The Makefile contains shortcuts for many useful commands referenced below. To utilize these commands "make" must be installed on your system (see details [here](https://stackoverflow.com/questions/10265742/how-to-install-make-and-gcc-on-a-mac) for mac os)

### Github Token
For installation of Github dependencies, both for local testing and within the docker container, a personal access token must be created on github, and an environmental variable named "GITHUB_TOKEN" with value set to the token string must be present in the environment. See [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) for details on how to create a personal access token.

### Python Version
For this project use Python >= 3.10

BOILERPLATE: If specific versions of python are required, a virtual environment with the correct python version must first be installed. I recommend using pyenv for installing old versions of python (see installation instructions [here](https://realpython.com/intro-to-pyenv/)). FOR EXAMPLE, after installing pyenv, python 3.6.12 can be installed using the command:

`pyenv install 3.6.12`  (NOTE: python 3.6.12 NOT required for this project)

Within a docker container, this is handled by using python3.6.12 as the base image (see DockerFile).

### Local Testing
For local testing, a virtual environment is required. Wherever you choose to create your virtual environment, just be mindful not to inadvertantly check it into the repo! If no specific version of python is required (i.e. you are using the current default) this can be done with the following simple command:

`python3 -m venv platform-container-template`

If a specific python version is required (see Python Version section above), then after installing the requisite version with pyenv (for example python 3.6.12) the command would look something like:

`python3 -m venv --python=/Users/<username>/.pyenv/versions/3.6.12/bin/python  platform-container-template`

With the virtualenv installed, activate via:

`source platform-container-template/bin/activate`

Finally, pip install the repo to run or develop via:

`pip install -e .`

### Container Testing

To build and run the container associated with this repo requires Docker be installed on your system. See installation details [here](https://docs.docker.com/desktop/install/mac-install/) for Mac os.

Once installed, you can build the container image from the Dockerfile via:

`make docker.build`

Once built you can test the build environment in two useful ways. First by running the prepared test script to test library versions and boto3 connections:

`make docker.test.build`

A second way is to launch an interactive terminal into the built container using:

`make docker.test.shell`

## Release Notes
N/A
