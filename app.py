#!flask/bin/python
import json
from flask import Flask,jsonify
from flask import request
from cdata import Beerdata

app = Flask(__name__)

@app.route('/beer/api/create', methods=['POST','GET'])
def createuser():
    #username,email,password
    if not request.is_json:
        abort(400)
    content = request.get_json(force=True)

    user=content['username'] 
    username=content['username']
    email=content['email']
    password=content['password']
    
    b=Beerdata()
    b.adduser(username,email,password)
    
    return json.dumps(b.listusers())


@app.route('/beer/api/addbeer', methods=['POST','GET'])
def addbeer():
    #userid,beercode,ibu,calories,abv,style,brewerlocation,glasstype
    if not request.is_json:
        abort(400)
    
    content = request.get_json(force=True)
    userid=content['userid'] 
    beercode=content['beercode']
    ibu=content['ibu']
    calories=content['calories']
    abv=content['abv']
    style=content['style']
    brewerlocation=content['brewerlocation']
    glasstype=content['glasstype']
    
    b=Beerdata()
    msg=b.addbeer(userid,beercode,ibu,calories,abv,style,brewerlocation,glasstype)
    
    return json.dumps(msg)

@app.route('/beer/api/addreview', methods=['POST','GET'])
def addreview():
    #userid,beercode,aroma,appearance,taste,palate,bottlestyle
    if not request.is_json:
        abort(400)
    content = request.get_json(force=True)

    userid=content['userid'] 
    beercode=content['beercode']
    aroma=content['aroma']
    appearance=content['appearance']
    taste=content['taste']
    palate=content['palate']
    bottlestyle=content['bottlestyle']
      
    b=Beerdata()
    msg=b.addreview(userid,beercode,aroma,appearance,taste,palate,bottlestyle)
    
    return json.dumps(msg)


@app.route('/beer/api/addglass', methods=['POST','GET'])
def addglass():
    #userid,glasscode,name
    if not request.is_json:
        abort(400)
    content = request.get_json(force=True)

    userid=content['userid'] 
    glasscode=content['glasscode']
    name=content['name']
        
    b=Beerdata()
    msg=b.addglass(userid,glasscode,name)    
    return json.dumps(msg)

@app.route('/beer/api/deleteglass', methods=['POST','GET'])
#deleteglass(user,glass)
def deleteglass():
    #userid,glasscode,name
    
    if not request.is_json:
        abort(400)
        
    content = request.get_json(force=True)
    print (content)

    userid=content['userid'] 
    glasscode=content['glasscode']
         
    b=Beerdata()
    msg=b.deleteglass(userid,glasscode)    
    return json.dumps(msg)

@app.route('/beer/api/myquery', methods=['POST','GET'])
def myquery():
    #userid,sqlquery
    if not request.is_json:
        abort(400)
        
    content = request.get_json(force=True)

    #user Id can be authenticated to run query
    userid=content['userid'] 
    sqlquery=content['sqlquery']
         
    b=Beerdata()
    msg=b.findrecords(sqlquery)
    
    return json.dumps(msg)

if __name__ == '__main__':
    app.run(debug=True)
