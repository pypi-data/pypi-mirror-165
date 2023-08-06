#!/bin/bash
pip install -r requirements.txt
pip install markdown pdoc3  mkdocs mkdocs-material mkdocstrings
pdoc superwise  -o temp
mv ./temp/superwise/* temp
rm -rf ./temp/superwise
mkdir docs
python docs.py
mkdocs build
rm -rf ./temp/superwise
mv site public
