""""
This code extart the articles from 'https://api.spaceflightnewsapi.net/v3/documentation#/Article/get_articles' and

ingest those into Elastic search docker container for further processing.

"""

__author__ = "Sagar Devidas Kolhe"

try:
    import os
    import sys
    import requests
    import json
    import csv
    import pandas as pd
    import logging

    import elasticsearch
    from elasticsearch import Elasticsearch
    from elasticsearch import helpers
    from configparser import ConfigParser

    print("All Modules Loaded......!")

except Exception as e:
    print("some modules are missing {}".format(e))

try:

    class DataExtractionIngestion:
        # Constructor of the class
        def __init__(self):
            self.config = ConfigParser()
            self.config.read('./app/app.ini')
            self.es = Elasticsearch(self.config.get("Elasticsearch", "HOST2"))
            # print(self.es.ping())

            self.data = None

        # For extracting the data from api.spaceflightnewsapi.net
        def DataExtarction(self):
            count_result = requests.get(self.config.get("Public API", "ARTICLES_COUNT"))
            print("Total number of Articles in the spaceflightnews are", count_result.json())
            # print(count_result.json())

            articles_result = requests.get(self.config.get("Public API", "ALL_ARTICLES"))
            self.data = articles_result.json()
            logging.info("\nData Extraction is Done.......!!")

        # Data Processing
        def DataPreprocessing(self):
            df = pd.read_csv(self.config.get("Files", "CSV_FILE"))
            print("\nchecking any feature has nan values: ", df.isna().sum())
            df = df.drop(['summary'], axis=1)

            print("Feature set after removing nan values column summary. ", df.isna().sum())
            df = df.to_dict('records')
            # print(df[0])
            logging.info("\n Data preprocessing is done.....!!")
            return df

        def saveExtectedDataToCSVFile(self):
            df = pd.DataFrame(self.data)
            df.to_csv(self.config.get("Files", "CSV_FILE"), index=False)
            logging.info("\nData is saved to .csv File.....!!")

        def DataIngestion(self, final_data):
            res = helpers.bulk(self.es, self.generator(final_data))
            logging.info("\n Bulk Data Ingested to Elasticsearch successfully.......!!!")

        def generator(self, final_data):
            for c, line in enumerate(final_data):
                # print(c)
                yield {
                    "_index": "articles",
                    "_type": "doc",
                    "_id": line["id"],
                    "_source": {
                        "events": line["events"],
                        "featured": line["featured"],
                        "imageUrl": line["imageUrl"],
                        "launches": line["launches"],
                        "newsSite": line["newsSite"],
                        "publishedAt": line["publishedAt"],
                        # "summary": line["summary"],
                        "title": line["title"],
                        "updatedAt": line["updatedAt"],
                        "url": line["url"]
                    }
                }

except Exception as e:
    print("Something went wrong:-> {}  .......!!".format(e))

def main():
    obj1 = DataExtractionIngestion()
    obj1.DataExtarction()

    obj1.saveExtectedDataToCSVFile()

    data = obj1.DataPreprocessing()

    obj1.DataIngestion(data)

if __name__ == '__main__':
    main()
