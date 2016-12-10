language_code=$1
get_url="https://dumps.wikimedia.org/${language_code}wiktionary/20161201/${language_code}wiktionary-20161201-all-titles.gz"

# Retrieve the dictionary
echo "get: ${get_url}"
curl -O ${get_url}

# Extract the dictionary
gzip -d *.gz