""""
This code extart the articles from 'https://api.spaceflightnewsapi.net/v3/documentation#/Article/get_articles' and

ingest those into Elasticsearch docker container for further processing.

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
    config = ConfigParser()
    config.read('./app/app.ini')
    es = Elasticsearch(config.get("Elasticsearch", "HOST2"))


    class DataExtractionIngestion:
        """ Extract the data from public API and Insert it into Elasticsearch. """

        # Constructor of the class
        def __init__(self):
            """ Required Variables. """
            self.data = None

        # For extracting the data from api.spaceflightnewsapi.net
        def DataExtarction(self):
            """ Extract the data from the Public API and
                save it to self.data
            """
            count_result = requests.get(config.get("Public API", "ARTICLES_COUNT"))
            print("Total number of Articles in the spaceflightnews are", count_result.json())

            all_articles = config.get("Public API", "ARTICLES")
            # print(all_articles +"?_limit="+str(count_result.json())+"&_sort=id")
            articles_result = requests.get(all_articles + "?_limit=" + str(count_result.json()) + "&_sort=id")
            self.data = articles_result.json()
            logging.info("\nData Extraction is Done.......!!")

        # Data Processing
        def DataPreprocessing(self):
            """ To check if there are NAN values in our data or not. If present remove those values."""

            df = pd.read_csv(config.get("Files", "CSV_FILE"))
            print("\nchecking any feature has nan values: ", df.isna().sum())
            df = df.drop(['summary'], axis=1)

            print("Feature set after removing nan values column summary. ", df.isna().sum())
            df = df.to_dict('records')
            # print(df[0])
            logging.info("\n Data preprocessing is done.....!!")
            return df

        def saveExtectedDataToCSVFile(self):
            """
                Convert the data inside the self.data to pandas data frame and save it to CSV file
            """
            df = pd.DataFrame(self.data)
            df.to_csv(config.get("Files", "CSV_FILE"), index=False)
            logging.info("\nData is saved to .csv File.....!!")

        def DataIngestion(self, final_data):
            """ Bulk ingestion of the data to elasticsearch.

                input: final_data. Elasticsearch supported data
            """
            res = helpers.bulk(es, self.generator(final_data))
            logging.info("\n Bulk Data Ingested to Elasticsearch successfully.......!!!")

        def generator(self, final_data):
            """ Generates the data in Elasticsearch format.

                input : final_data. Contains data which is not supported by the Elasticsearch.

                output: convert each data in to Elasticsearch format
             """
            for c, line in enumerate(final_data):
                # print(c)
                yield {
                    "_index": "demo",
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
    """ Create the object of the class DataExtractionIngestion () and
        calls the required methods sequentially
    """

    data_extract_ingest = DataExtractionIngestion()
    data_extract_ingest.DataExtarction()

    data_extract_ingest.saveExtectedDataToCSVFile()

    data = data_extract_ingest.DataPreprocessing()

    data_extract_ingest.DataIngestion(data)


# if __name__ == '__main__':
#     main()
