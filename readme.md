# Distributed RESTful Datawarehouse

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

Open the same URL in a browser: http://localhost:5003/article/5
You should see the title of the article you just sent earlier.




### Prerequisities

* Python 2.7.11
* Apache Cassandra

### Installing


## Built With

* Python 2
* Flask
* Apache Cassandra
* Sublime