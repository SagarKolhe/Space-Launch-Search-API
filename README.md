**Space launch search API**

**Pre-requisites:**

1. python version 3.7

2. Elasticsearch python client version should be 7.16.3

3. Elasticsearch docker image version should be 6.6.1

4. Docker should be installed on your machine

5. There should be docker network called "mybridge"

**Workflow:**

**Step 1**: In this project, we start the Elasticsearch server inside the docker container by running star_elsticsearch.sh script

**Step 2**: We run the run.sh script, which pull the data from the Public API (https://api.spaceflightnewsapi.net/v3/documentation#/Article/get_articles) and ingest that data inside the Elasticsearch.

**Step 3**: Now, we run our flask search app through the docker container. Build the docker file with this command as "docker build -t spaceflightnews ."

**Step 4**: Run the docker file with this command as "docker run --net="mybridge" --name searchsvc -p 5000:5000 spaceflightnews"

**Step 5**: Provide the query inside the brower url as "http://172.18.0.3:5000/search?q=NASA"

**Step 6**: This will return the Articles inside the Elasticsearch which matches title with "NASA" as sub-string.

Also, If you want to persist the container's data the there are two ways to do it.

By using the concept called 1) volumes 2) Bind Mount.

1) Volumes:-
For this use docker run command as:
“docker run -d -v es-data:/usr/share/elasticsearch/data  --name container22 --net="mybridge"  -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:6.6.1”

2) Bind Mount:-
a. Set permissions to:
	i. sudo mkdir -p $PWD/elasticsearch/data
	ii. sudo chmod 777 -R $PWD/elasticsearch/data

b. Docker run command with Bind Mount:
    “docker run -d --name elasticsearch --net="mybridge"  -p 9200:9200 -p  9300:9300 -v $PWD/elasticsearch/data:/usr/share/elasticsearch/data -e "discovery.type=single-node" elasticsearch:6.6.1”

