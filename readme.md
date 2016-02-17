# Distributed RESTful data warehouse

Description here

## Usage
In the distributed-restful-dw directory, run app.py, app2.py and proxy.py in three different terminal windows:
```
python app.py
python app2.py
python proxy.py
```
Open a terminal window and send a POST request using curl:
```
curl http://localhost:5003/article/10 -d "title=Article Five" -X POST
```

Open the same URL in a browser: http://localhost:5003/article/5.You should see the title of the article you just sent earlier.




### Prerequisities

* [Python 2.7.11](http://python.org/)
* [Apache Cassandra 3.3](http://cassandra.apache.org/)

### Installing


## Built With

* [Python 2.7.11](http://python.org/)
* [Flask](http://flask.pocoo.org/)
* [Flask Restful](http://flask-restful-cn.readthedocs.org/en/latest/)
* [Apache Cassandra 3.3](http://cassandra.apache.org/)
* [Sublime](https://www.sublimetext.com/)