#!/usr/bin/env bash

sudo su

docker run -d -P --name staticsite staticsite:latest

docker port staticsite
