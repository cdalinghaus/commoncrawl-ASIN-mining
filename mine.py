import os
import subprocess
import random
import sys

crawl = sys.argv[1]
print("Loading crawl", crawl)

os.system("rm cc-index.paths.gz")
os.system("rm cc-index.paths")
os.system("rm urls.txt")
os.system(f"wget https://data.commoncrawl.org/crawl-data/{crawl}/cc-index.paths.gz")
os.system("gzip -d cc-index.paths.gz")

f = open("cc-index.paths")

urls = list(f.readlines())
random.shuffle(urls)

for f in urls:
    url = "https://data.commoncrawl.org/"  + f
    print("Loading", url)

    os.system(f"wget {url} > /dev/null")

    fname = f.split("/")[-1].strip()
    cmd = f"zgrep --line-buffered -Eo 'https?://[^ ]*amazon\\.com/(dp|gp/product)/[A-Z0-9]{{10}}' \"{fname}\" >> urls.txt"
    subprocess.run(cmd, shell=True, executable="/bin/bash")

    print(f"Finished processing {url}")
    os.system(f"rm {fname}")

os.system(f"mv urls.txt {crawl}.urls.txt")
