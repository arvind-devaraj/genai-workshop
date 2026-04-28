#!/bin/bash

# Check if an argument was provided
if [ -z "$1" ]; then
    echo "Error: Please provide a page number."
    exit 1
fi

# Pass the first Bash argument ($1) to the Python script
python extract-page.py "$1"  > contents.txt
python summarize-local.py
python test-audio.py > url.txt
open $(< url.txt)