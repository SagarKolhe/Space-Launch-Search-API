try:
    import json
    from flask import Flask, request, jsonify
    from elasticsearch import Elasticsearch
    from configparser import ConfigParser
    import logging

    config = ConfigParser()
    config.read('./app/app.ini')

    def connect_elasticsearch(**kwargs):
        _es_config = config.get("Elasticsearch", "HOST1")
        _es_hosts = [_es_config]
        if 'hosts' in kwargs.keys():
            _es_hosts = kwargs['hosts']
        _es_obj = None
        _es_obj = Elasticsearch(hosts=_es_hosts, timeout=10)
        if _es_obj.ping():
            print("\nConnected Successfully....!!\n")
        else:
            print("\nAwe, connection failed. Please try again.....!!\n")
        return _es_obj
    es = connect_elasticsearch()
    app = Flask(__name__)

    # Default route
    @app.route("/")
    def home():
        return "<h3>Welcome to Spaceflight's News Articles.....!!</h3>"


    @app.route('/search', methods=['GET'])
    def search():
        query_string = request.args.get('q')
        final_query = {"match": {"title": query_string}}
        result = es.search(index="articles", query=final_query)
        return jsonify(result['hits']['hits'])

    def main():
        app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
        app.run(debug=True, host='0.0.0.0', port=5000)

except Exception as e:
    print("Flask Application Error: ", e)
