import os
import subprocess
import random
import sys

crawl = sys.argv[1]
print("Loading crawl", crawl)

# Clean up from prior runs
os.system("rm -f cc-index.paths.gz")
os.system("rm -f cc-index.paths")
os.system("rm -f urls.txt")

# Fetch the list of index segment paths
os.system(f"wget https://data.commoncrawl.org/crawl-data/{crawl}/cc-index.paths.gz")
os.system("gzip -d cc-index.paths.gz")

with open("cc-index.paths", "r") as fh:
    urls = list(fh.readlines())

random.shuffle(urls)

# List of Amazon TLDs to match
amazon_tlds = [
    "com", "de", "fr", "it", "es",
    "co\\.uk", "co\\.jp",
    "ca", "com\\.au", "com\\.mx", "com\\.br",
    "nl", "se", "pl", "sa", "ae", "sg", "tr", "in"
]
tld_group = "(?:" + "|".join(amazon_tlds) + ")"

# Pattern matches:
#   https://{anything}.amazon.<tld>/(dp|gp/product)/ASIN
# Extracts the whole URL; ASINs are 10 chars [A-Z0-9]
pattern = rf"https?://[^ ]*amazon\.{tld_group}/(?:dp|gp/product)/[A-Z0-9]{{10}}"

for path_line in urls:
    url = "https://data.commoncrawl.org/" + path_line.strip()
    print("Loading", url)

    # Download the gz index segment quietly
    os.system(f"wget -q {url}")

    fname = path_line.split("/")[-1].strip()

    # Grep the compressed file for product URLs in all supported locales
    cmd = f"zgrep --line-buffered -Eo '{pattern}' \"{fname}\" >> urls.txt"
    subprocess.run(cmd, shell=True, executable="/bin/bash")

    print(f"Finished processing {url}")
    os.system(f"rm -f {fname}")

# Move output to <crawl>.urls.txt
os.system(f"mv urls.txt {crawl}.urls.txt")
print(f"Wrote {crawl}.urls.txt")
