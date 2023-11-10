FROM mambaorg/micromamba

WORKDIR /playground

ENV DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update -y && apt-get upgrade -y

COPY env.yml .

RUN micromamba env create -f env.yml -y

COPY . .
