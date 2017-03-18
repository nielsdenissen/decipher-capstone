#!/usr/bin/env bash

language_code=$1
location=$2
get_url="https://dumps.wikimedia.org/${language_code}wiktionary/20161201/${language_code}wiktionary-20161201-all-titles.gz"

# Retrieve the dictionary
echo "get: ${get_url}"
cd ${location}
curl -O ${get_url}

# Extract the dictionary
gzip -d *.gz