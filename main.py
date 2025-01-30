import argparse
import os
import sys
from pprint import pprint

from utils.extractor import ml_extract
from utils.tracker import price_tracking

parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, required=True, help="url of mercadolibre.com")
parser.add_argument("--no-headless", action="store_false", help="show browser window")
parser.add_argument("--cache", help="directory")
parser.add_argument("--keyword", type=str, help="items that match word")
parser.add_argument("--exclude", type=str, help="word to exclude items")
parser.add_argument("--notify", type=str, help="email address")

args = parser.parse_args()

if args.cache and not os.path.isdir(args.cache):
    print(f"directory {args.cache_directory} not found...")
    sys.exit(1)

filtered = []
results = ml_extract(args.url, args.no_headless)

if args.keyword:
    filtered = [
        item for item in results if args.keyword.lower() in item["title"].lower()
    ]

if args.exclude:
    if filtered:
        filtered = [
            item
            for item in filtered
            if args.exclude.lower() not in item["title"].lower()
        ]
    else:
        filtered = [
            item
            for item in results
            if args.exclude.lower() not in item["title"].lower()
        ]

pprint(filtered, indent=4)

if args.cache:
    price_tracking(filtered, args.cache, args.notify)
