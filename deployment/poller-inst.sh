#!/usr/bin/env bash


apt-get update --allow-releaseinfo-change && apt-get upgrade -y &&\
apt-get install -y supervisor ntp git


