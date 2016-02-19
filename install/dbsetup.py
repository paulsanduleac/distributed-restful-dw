# Run this when you first install Cassandra to set up the keyspace and articles table
from cassandra.cluster import Cluster

cluster = Cluster()
dbsession = cluster.connect()

dbsession.execute("CREATE KEYSPACE dev with replication = {'class':'SimpleStrategy','replication_factor':1};")
dbsession.execute("USE dev;")
dbsession.execute("CREATE TABLE articles (aid INT PRIMARY KEY, title TEXT);")
dbsession.execute("INSERT INTO articles (aid, title) values (1, 'First Article');")
dbsession.execute("INSERT INTO articles (aid, title) values (2, 'Second Article');")



