#!/bin/bash

INPUT_DIR=${INPUT_DIR:-input}
PERSONA=${PERSONA:-"PhD Researcher in AI"}
JOB_TO_BE_DONE=${JOB_TO_BE_DONE:-"Literature review on neural networks"}
OUTPUT_FILE=${OUTPUT_FILE:-output/output.json}

mkdir -p output

python main.py "$INPUT_DIR" "$PERSONA" "$JOB_TO_BE_DONE" "$OUTPUT_FILE"