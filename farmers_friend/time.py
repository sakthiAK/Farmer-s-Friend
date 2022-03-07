# Python3 code to demonstrate
# attributes of now()
import pymongo
import datetime	
# using now() to get current time
Client = pymongo.MongoClient()
mydb = Client['Farmers_friend']
mycol =mydb['time']
mycol1 = mydb['confirmed_Orders']
current_time = datetime.datetime.now()
# Printing attributes of now().
print ("The attributes of now() are : ")
list =[]
for i in mycol.find({'time':{'$lte':current_time}}):
    print(i)
    list.append(i)
    
print(list)    

for y in list:
    z =mycol1.insert_one({'time':y.get('time')})
    print(z)

