#!/usr/bin/env bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <file_name> <word>"
    exit 1
fi

file_name=$1
word=$2

if [ ! -f "$file_name" ]; then
    echo "Error: File '$file_name' not found."
    exit 2
fi

word_count=$(grep -oiw "$word" "$file_name" | wc -l)
echo $word_count
