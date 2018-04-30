#!/bin/sh

# Creates asset dir
if [ ! -d "assets" ]; then
    mkdir assets
fi

# Clears public directory
if [ -d "html" ]; then
    rm -r html
fi
mkdir html

# Merges all documents and creates a table of contents
pandoc -s -c pandoc.css --toc --toc-depth=4 src/* -o "html/index.html"

# Copies all assets into the html dir
cp -r assets/* html/
