import redis

r = redis.Redis("localhost")

#add data to db 
r.set('1', 'article1')
r.set('2', 'article2')

#get data from db
var = r.get('1')
print (var)

#in redis-cli.exe 
# get 1 command will respond> article1 