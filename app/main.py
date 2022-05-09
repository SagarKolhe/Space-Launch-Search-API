try:
    # import Data_extraction_ingestion as DEI
    import Article_search_app as APP
    import logging
    from configparser import ConfigParser

    if __name__ == '__main__':
        config = ConfigParser()
        config.read('./app/app.ini')
        # print("Sections : ", config.sections())
        logging.basicConfig(filename=config.get("Files", "LOG_FILE"), level=logging.INFO)
        logging.info("\n Starting the service......!!")
        APP.main()
        logging.info("\n Service is up now.....!!")
        logging.info("Code execution ended......!!")
except Exception as e:
    print("Main Error:", e)
