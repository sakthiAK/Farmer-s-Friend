
from flask import Flask , request , render_template,url_for, request, session
from PIL import Image
from io import BytesIO  
import pymongo
from flask_session import Session
import datetime	

Client = pymongo.MongoClient()

mydb = Client['Farmers_friend']



app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
########################home Page
@app.route('/')
def home():
    return render_template('clogin.html')


##################### signup
@app.route('/csignup',methods=['POST'])
def csignup():
    mycol = mydb["Customer"]
    current_time = datetime.datetime.now()
    name = request.form['Name'] 
    email = request.form['Email']
    phoneNumber = request.form['phone_number']
    password = request.form['password']
    confirm_password =request.form['confirm_password']
    district = request.form['district']
    x = mycol.find_one({'E-mail':email})
    if x :
        msg = 'User Name Is Already Exist'
        return render_template('csignin.html',msg=msg)
    else :
       session["user"]=name
       session["district"]=district
       session['time'] = current_time
       mydict = { "name":name, "phoneNumber":phoneNumber,'district':district, "E-mail":email,"password":password }
       x = mycol.insert_one(mydict)
       print(x)    
       return render_template('cmiddle.html')

@app.route('/fsignup',methods=['POST'])
def fsignup():
    mycol = mydb['Farmer']
    name = request.form['Name'] 
    email = request.form['Email']
    phoneNumber = request.form['phone_number']
    password = request.form['password']
    confirm_password =request.form['confirm_password']
    district = request.form['district']
    x = mycol.find_one({'E-mail':email})
    if x :
        msg = 'User Name Is Already Exist'
        return render_template('csignin.html',msg=msg)
    else :    
        session["user"]=email
        session["district"]=district   
        mydict = { "name":name, "phoneNumber":phoneNumber, "E-mail":email,"password":password }
        x = mycol.insert_one(mydict)
        return render_template('fmiddle.html')    

#######################login
@app.route('/clogin',methods=['POST'])
def clogin():
    current_time = datetime.datetime.now()
    mycol = mydb['Customer']
    session["user"] =request.form['username']
    x=session.get("user")
    session['time'] = current_time
    print('########### C login ############')
    print(x)
    user = request.form['username']
    password = request.form['password']
    mydoc = mycol.find_one({'E-mail':user})
    if mydoc:
        if password == mydoc.get('password'):
           print('login successfully')
           return render_template('cmiddle.html')
        else:    
          error = 'The Password Does not match '
          return render_template('clogin.html',msg=error)   
    else:
       error = 'user name Does not exist'
       return render_template('clogin.html',msg=error) 



@app.route('/flogin',methods=['POST'])
def flogin():
    mycol = mydb['Farmer']
    user = request.form['username']
    password = request.form['password']
    session["user"] =request.form['username']
    x=session.get("user")
    print('########### f login ############')
    print(x)
    
    mydoc = mycol.find_one({'E-mail':user})
    if mydoc:
        if password == mydoc.get('password'):
           print('login successfully')
           return render_template('fmiddle.html',hide=user)
        else:    
          error = 'The Password Does not match '
          return render_template('flogin.html',msg=error)   
    else:
       error = 'user name Does not exist'
       return render_template('flogin.html',msg=error)  

###############################################################    Farmer Module    #################################################


############### farmers's Item Add route
@app.route('/additems',methods=['POST'])
def additems():
    mycol = mydb['Items']
    iname = request.form['cname']
    icost = request.form['cost']
    district = request.form['district']
    tons = request.form['tons']
    user_name = session.get("user")
    print(user_name)
    myrow ={'user_name':user_name,'item_name':iname,'cost':icost,'district':district,'tons':tons}
    x = mycol.insert_one(myrow)
    msg = 'items added sucessfully'
    return render_template('fadd.html',msg=msg) 

################# Farmers Item Delete Route       
@app.route('/fdeleteaction',methods=['POST'])
def fdeleteaction():
     mycol = mydb['Items']
     x=session.get("user")
     item = request.form['itemname']
     mydoc = mycol.find_one({'user_name':x})
     if mydoc:
        if item == mydoc.get('item_name'):
           print('item Available')
           myquery = { "user_name": "sakthi260601@gmail.com",'item_name':'carrot' }
           mycol.delete_one(myquery)
           msg='Item deleted Successfully'
           return render_template('fdelete.html',msg=msg)
        else:    
          error = 'item not available '
          return render_template('fdelete.html',msg=error)   
     else:
       error = 'user name Does not exist'
       return render_template('clogin.html',msg=error) 

          
################ Farmers Item Showing Route
@app.route('/showbutton',methods=['POST'])
def fshowbutton():
    mycol = mydb['Items']
    user = session['user']
    print(user)
    list =[]
    for i in mycol.find({'user_name':user}):
        print(i)
        list.append(i)
    
    print(list)    
    return render_template('fshow.html',lsobj=list)   



######################################################## Customer Module ##############################################################


### customer searching route
@app.route('/getitem',methods=['POST'])
def getitem():
    mycol = mydb['Items']
    item = request.form['item']
    mycol = mydb['Items']
    mycol1 = mydb['Farmer']
    msg=''
    list =[]
    list2 =[]
    
    for i in mycol.find({'item_name':item}):
        print(i)
        list.append(i)
        print(list)   
    if not list:
           msg = 'Items Not Available'
    for x in list:
      for y in mycol1.find({'E-mail':x.get('user_name')}):
          list2.append(y)
          print(y)    
    return render_template('cmiddle.html',lsobj=list,lsobj2=list2,msg=msg)   

 


################## customer Item Add route
@app.route('/cadd',methods=['POST'])
def cadd():
    current_time = datetime.datetime.now()
    mycol = mydb['customeritems']
    user_name = session.get("user")
    seller = request.form['seller']
    item = request.form['item']
    cost = request.form['cost']
    
    print(seller)
    myrow ={'user':user_name,'seller_id':seller,'item_name':item,'cost':cost,'time':current_time}
    x = mycol.insert_one(myrow)
    msg = 'items added sucessfully'
    return render_template('cmiddle.html',msg=msg) 


####### customer's recent Item Show route
@app.route('/crecent',methods=['POST'])
def crecent():
    x=session.get("time")
    mycol = mydb['customeritems']
    user = session.get("user")
    list =[]
    total = int(0)
    for i in mycol.find({'user':user,'time':{'$gte':x}}):
        print(i)
        total = total+int(i.get('cost'))
        list.append(i)
    return render_template('crecent.html',lsobj=list,total=total) 


########### customer's Item drop route
@app.route('/cdrop',methods=['POST'])
def cdrop():
     current_time = datetime.datetime.now()
     y=session.get("time")
     mycol = mydb['customeritems']
     x = session.get("user")
     item = request.form['item'] 
     print(item)
     myquery = { "user":x,'item_name':item,'time':{'$gte':y} }
     mycol.delete_one(myquery)
     list =[]
     total =int(0)
     for i in mycol.find({'user':x,'time':{'$gte':y}}):
        print(i)
        total=total+int(i.get('cost'))
        list.append(i)
     print(total)    
     return render_template('crecent.html',lsobj=list,total=total) 


@app.route('/placemyorder',methods=['POST'])
def placemyorder():
     user = session.get('user')
     ses_time = session.get('time')
     mycol = mydb['customeritems']
     mycol2 = mydb['confirmed_Orders']
     for x in mycol.find({'user':user,'time':{'$gte':ses_time}}):
         mycol2.insert_one({'user':x.get('user'),'seller_id':x.get('seller_id'),'item_name':x.get('item_name'),'cost':x.get('cost'),'time':x.get('time')})
     msg = "Orokder Placed Successfully"
     query = {"time":{'$gte':ses_time}}
     d = mycol.delete_many(query)
     print(d.deleted_count, " documents deleted !!")
     return render_template('crecent.html',msg=msg)      
     

########################## Cost Update Route
@app.route('/fupdateaction',methods=['post'])
def fupdateaction():
    mycol = mydb['Items']
    x=session.get("user")
    item = request.form['itemname']
    cost = request.form['cost']
    mydoc = mycol.find_one({'user_name':x})
    if mydoc:
        if item == mydoc.get('item_name'):
           print('item Available')
           myquery = { "user_name": x ,"item_name":item}
           newvalues = { "$set": { "cost":cost } }
           mycol.update_one(myquery, newvalues)
           msg='Cost Upadated Successfully'
           return render_template('fupdate.html',msg=msg)
        else:    
          error = 'item not available '
          return render_template('fupdate.html',msg=error)   
    else:
       error = 'user name Does not exist'
       return render_template('clogin.html',msg=error) 

   
########################################### Link Buttons Route #####################################################     

#afterhome page
@app.route('/afterhome')
def afterhome():
    return render_template('afterhome.html')
#customer signin page
@app.route('/csignin')
def csignin():
    return render_template('csignin.html')
#seller or Farmer sign in page
@app.route('/fsignin')
def fsignin():
    return render_template('fsignin.html')    

#login page

@app.route('/flogbutton')
def flogbutton():
    return render_template('flogin.html')    

@app.route('/clogbutton')
def clogbutton():
    return render_template('clogin.html')

@app.route('/addbutton')
def faddbutton():
    return render_template('fadd.html')    

@app.route('/updatebutton')
def fupdatebutton():
    return render_template('fupdate.html')    

@app.route('/deletebutton')
def fdeletebutton():
    return render_template('fdelete.html') 


@app.route('/backtopurchase')
def backtopurchase():
    return render_template('cmiddle.html')      

@app.route('/fmiddle')
def fmiddle():
    return render_template('fmiddle.html')       

        
@app.route('/vimage',methods=['POST'])
def vimage():
    vimage = request.files['vimage']
    mycol = mydb['veg_image']
    x=mycol.insert_one({'username':'sakthi','vimage':vimage.filename})
    print(x)
    return 'done'
app.run()    