import requests
from parser import parse_mesures
from model import DBClient
import argparse

def get_latest_raw_urls():
    """
    Get newly published air quality dataset from an open data API

    Returns:
        list(string): list of the urls of the new datasets
    """
    r = requests.get("https://mg-services.herokuapp.com/api/open-data/pollution/air/datasets")
    results = r.json()
    url_list = []
    for result in results :
        if "Données brutes" in result["name"] :
            url_list.append(result["link"].split("?url=")[-1])
    return url_list

def insert_new_mesures(new_urls, limit=10):
    """
    Parse and insert the new datasets which have not yet been inserted

    Args:
        new_urls (list(string)): list of the latest datasets urls
        limit (int, optional): maximum number of datasets to parse. Defaults to 10.
    """
    print(f"found {len(new_urls)} new urls, only last {limit} will be parsed")
    client = DBClient()
    already_inserted_urls = [dataset["url"] for dataset in client.datasets.find()]
    for url in new_urls[:limit]:
        if not (url in already_inserted_urls):
            client.insert_dataset(url)
            r = requests.get(url)
            mesures = parse_mesures(r.text)
            client.insert_mesures(mesures)
            print(f"inserted new dataset from url {url}")

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", help="limit on the number of datasets to import", type=int, default=10)
    args = parser.parse_args()
    urls = get_latest_raw_urls()
    insert_new_mesures(urls, limit=args.limit)
    