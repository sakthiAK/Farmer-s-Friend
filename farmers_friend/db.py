import pymongo
import datetime	
Client = pymongo.MongoClient()

mydb = Client['Farmers_friend']

col = mydb["customeritems"]
current_time = datetime.datetime.now()
query = {"time":{'$lte':current_time}}
d = col.delete_many(query)
  
print(d.deleted_count, " documents deleted !!")











   

