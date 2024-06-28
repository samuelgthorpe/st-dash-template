FROM ubuntu:22.04 as base

RUN apt update && \
    apt-get install -y software-properties-common

RUN apt-get update -y && \
    apt-get install -y \
    openssh-client \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip \
    make \
    g++ \
    git \
    libproj-dev \
    unzip \
    autoconf \
    automake \
    libtool \
    cmake \
    libpng-dev \
    zlib1g-dev \
    xz-utils \
    libbz2-dev \
    libffi-dev \
    libsnappy-dev \
    wget \
    gfortran \
    curl \
    libpq-dev \
    libpcap-dev \
    bash \
    nano \
    && apt-get clean -y

# set workdir add src
WORKDIR /app
COPY . .

# update pip & install
ARG GITHUB_TOKEN
RUN pip install --upgrade pip && pip install -e . --ignore-installed

# set entry point
ENV PYTHONPATH=.
ENTRYPOINT ["python3"]





