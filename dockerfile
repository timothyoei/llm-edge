FROM mambaorg/micromamba

WORKDIR /playground

ENV DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install -y \
  curl

COPY env.yml .

RUN micromamba env create -f env.yml -y

COPY . .
