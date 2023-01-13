FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

# Install System dependencies
RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get -y install \
        software-properties-common \
        curl \
        unzip \
        bash \
        python3-pip \        
        git \
        jq \
        zsh

# Install the dependencies file to the working directory
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt