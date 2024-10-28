#!/bin/sh

cd /usr/src/app
python tinystatus.py &
python serve.py

