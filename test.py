import json
import sys

#Reference requests module from your flask virtual environment.
#You may ignore the line if you have requests installed in your main python application
sys.path.append('C:/Users/jawebwa/Desktop/challenge/flask/Lib/site-packages')
import requests

#this is the database module
from cdata import Beerdata

#You can use this to recreate the sqlite3 database.
def createtables():
    t = Beerdata()
    print(t.createusertable())
    print(t.createbeertable())
    print(t.createglasstable())
    print(t.createreviewtable())

#Testing adding a user
def adduser():
    url='http://localhost:5000/beer/api/create'
    payload={'username':'awebwa2',
             'email':'jj@rr',
             'password':'kk'}
    r = requests.post(url, data=json.dumps(payload),headers={'content-type': 'application/json'})
    print(r.text)

#Testing Adding a beer
def addbeer():
    #object (userid,beercode,ibu,calories,abv,style,brewerlocation,glasstype)
    url='http://localhost:5000/beer/api/addbeer'
    payload={'userid':'awebwa2',
             'beercode':'XYZ',
             'ibu':'CONC',
             'calories':'45.23',
             'abv':'21',
             'style':'Long',
             'brewerlocation':'Milwaulee',
             'glasstype':'Clear'}
    r = requests.post(url, data=json.dumps(payload),headers={'content-type': 'application/json'})
    print(r.text)

#Testing adding a review
def addreview():
    #object (userid,beercode,aroma,appearance,taste,palate,bottlestyle)
    url='http://localhost:5000/beer/api/addreview'
    payload={'userid':'awebwa2',
             'beercode':'XYZ',
             'aroma':'1',
             'appearance':'3',
             'taste':'2',
             'palate':'4',
             'bottlestyle':'5'}
    r = requests.post(url, data=json.dumps(payload),headers={'content-type': 'application/json'})
    print(r.text)

#Testing adding a glass
def addglass():
    #object(userid,glasscode,name)
    url='http://localhost:5000/beer/api/addglass'
    payload={'userid':'awebwa2',
             'glasscode':'favourite1',
             'name':'Maroon Beer'}
    r = requests.post(url, data=json.dumps(payload),headers={'content-type': 'application/json'})
    print(r.text)

#Testing running any logical analytical qury
def myquery():
    #userid,sqlquery
    #use user I to authenticate who can run the query
    #craft any valid sql query
    sqlquery='select * from reviews'
    
    url='http://localhost:5000/beer/api/myquery'
    payload={'userid':'awebwa2',
             'sqlquery':sqlquery}
    r = requests.post(url, data=json.dumps(payload),headers={'content-type': 'application/json'})
    print(r.text)
    
#Test deleting a glass
def deleteglass():
    #object(userid,glasscode)
    url='http://localhost:5000/beer/api/deleteglass'
    payload={'userid':'awebwa2',
             'glasscode':'favourite1'}
    r = requests.post(url, data=json.dumps(payload),headers={'content-type': 'application/json'})
    print(r.text)

#Use this to display data in the tables if you have no tools for sqlite3
b=Beerdata()
def showusers():
    print(b.findrecords('select * from users'))
def showbeers():
    print(b.findrecords('select * from beers'))
def showglasses():
    print(b.findrecords('select * from glasses'))
def showreviews():
    print(b.findrecords('select * from reviews'))
    

    
