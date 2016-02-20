# Distributed RESTful data warehouse

Proof of concept for a RESTful interface on a Cassandra database that stores information about articles (id, title). Multiple instances of the interface are accessed through a proxy. The proxy also acts as a roundrobin load balancer and as a cache layer storing cache in a Redis instance.

_GET_ requests to the proxy on the path /article/ID (where ID is replaced by the ID of the article) are cached for 5 seconds in Redis, _POST_ requests are not cached, but instead passed directly to one of the registered REST interfaces for the Cassandra database. 

When it is run, each instance of the REST interface for Cassandra notifies the proxy of the address and port it is running on. If you exit it through a _KeyboardInterrupt_, it will also notify the proxy of its shutdown.

## Usage
In the distributed-restful-dw directory, run app.py (as many times as you want, each execution starts and instance) and proxy.py in two or more different terminal windows. The proxy needs to be started first.
```
python proxy.py
python app.py  (this can be run again to start another instance)

## Basic testing
```
Open a terminal window and send a POST request using curl:
```
curl http://localhost:5000/article/5 -d "title=Article Five" -X POST
```

Open the same URL in a browser: http://localhost:5003/article/5. You should see the title of the article you just sent earlier in the JSON response.

If you refresh it again within 5 seconds, you should get the same response with the field 'cached' added, showing that this time the response comes from the cache storage in Redis.

## Configuration & installation

## Built With & Prerequisites

* [Python 2.7.11](http://python.org/)
* [Flask](http://flask.pocoo.org/)
* [Flask Restful](http://flask-restful-cn.readthedocs.org/en/latest/)
* [Redis-py](https://redis-py.readthedocs.org/en/latest/)
* [Python Driver for Apache Cassandra](https://github.com/datastax/python-driver)
* [Apache Cassandra 3.3](http://cassandra.apache.org/)