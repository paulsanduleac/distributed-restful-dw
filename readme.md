# Distributed RESTful data warehouse

Proof of concept for a RESTful interface on a Cassandra database that stores information about articles (id, title). Multiple instances of the interface are accessed through a proxy. The proxy also acts as a roundrobin load balancer and as a cache layer storing cache in a Redis instance.

## Usage
In the distributed-restful-dw directory, run app.py (as many times as you want, each execution starts and instance) and proxy.py in three different terminal windows:
```
python app.py 
python proxy.py
```
Open a terminal window and send a POST request using curl:
```
curl http://localhost:5000/article/5 -d "title=Article Five" -X POST
```

Open the same URL in a browser: http://localhost:5003/article/5. You should see the title of the article you just sent earlier.

If you refresh it again within 5 seconds, you'll also get the value '1' for the field 'cached', showing that this time the response comes from the cache storage in Redis.

### Installing


## Built With && Prerequisites

* [Python 2.7.11](http://python.org/)
* [Flask](http://flask.pocoo.org/)
* [Flask Restful](http://flask-restful-cn.readthedocs.org/en/latest/)
* [Redis-py](https://redis-py.readthedocs.org/en/latest/)
* [Python Driver for Apache Cassandra](https://github.com/datastax/python-driver)
* [Apache Cassandra 3.3](http://cassandra.apache.org/)