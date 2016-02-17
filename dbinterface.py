#initial proof of concept for connecting to Cassandra
from cassandra.cluster import Cluster

cluster = Cluster()
dbsession = cluster.connect('dev')
users = dbsession.execute('SELECT * FROM articles')

for user_row in users:
	print user_row.id, user_row.name


