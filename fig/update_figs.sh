#!/bin/bash
# copy all pdf,png files in `../data` into current directory.
find ../data -name '*.pdf' -exec cp {} ./ \;
find ../data -name '*.png' -exec cp {} ./ \;

