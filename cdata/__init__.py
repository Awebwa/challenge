
#These modules are avaible in any python installation
import sqlite3
import time
from datetime import datetime

#This database implements all the objects described. The objective is to provide a separate mechanism for:
#1)Storing data
#2)Executing independent DML statements
#3)Levarage data validation mechanism available in SQL

# sqlite3 has been used but this could be any DBMS with all the capabilities
#=================================================================================================

class Beerdata:
    #Edit this line to correpond with a directory on your PC
    def __init__(self,filename='C:/Users/jawebwa/Desktop/challenge/cdata/data/drink.db'):
        self.file=filename

    #Create database objects if database is not available
    #----------------------------------------------------------------------------------------------
    #Note that cur.execute(sql1) is turned off while creating tables unless the table already exists

    def createusertable(self):
        conn=sqlite3.connect(self.file)
        cur=conn.cursor()
        
        sql1='DROP TABLE USERS'        
        sql2='''CREATE TABLE USERS (USERID TEXT PRIMARY KEY,
                                          DATE DATETIME DEFAULT CURRENT_TIMESTAMP,
                                          EMAIL TEXT,
                                          PASSWORD TEXT,
                                          CURRENT  TEXT,
                                          LASTSEEN TEXT)'''        
        #cur.execute(sql1)
        cur.execute(sql2)
        conn.close()
        return 'User Table droped and created'
        
    def createbeertable(self):        
        conn=sqlite3.connect(self.file)
        cur=conn.cursor()        
        sql1='DROP TABLE BEERS'        
        sql2='''CREATE TABLE BEERS (ID INTEGER PRIMARY KEY,
                                          DATE DATE,
                                          BEERCODE TEXT,
                                          IBU TEXT,
                                          CALORIES REAL,
                                          ABV TEXT,
                                          STYLE TEXT,
                                          BREWERYLOCATION TEXT,
                                          GLASSTYPE TEXT,
                                          USERID TEXT,                                          
                                          ACTIVITY  TEXT,
                                          PARAMETER INREGER)'''
        #cur.execute(sql1)
        cur.execute(sql2)
        conn.close()
        return 'Beer Table droped and created'

    def createglasstable(self):        
        conn=sqlite3.connect(self.file)
        cur=conn.cursor()        
        sql1='DROP TABLE GLASSES'        
        sql2='''CREATE TABLE GLASSES (ID INTEGER PRIMARY KEY,
                                          DATE DATE,
                                          USERID TEXT,
                                          GLASSCODE TEXT,
                                          NAME TEXT)'''          
        #cur.execute(sql1)
        cur.execute(sql2)
        conn.close()
        return 'Glass Table droped and created'

    def createreviewtable(self):        
        conn=sqlite3.connect(self.file)
        cur=conn.cursor()        
        sql1='DROP TABLE REVIEWS'        
        sql2='''CREATE TABLE REVIEWS (ID INTEGER PRIMARY KEY,
                                          DATE DATE,
                                          BEERCODE TEXT,
                                          USERID TEXT,                           
                                          AROMA INTEGER DEFAULT 0,
                                          APPEARANCE INTEGER DEFAULT 0,
                                          TASTE INTEGER DEFAULT 0,
                                          PALATE INTEGER DEFAULT 0,
                                          BOTTLESTYLE INTEGER DEFAULT 0,
                                          YEARWEEK TEXT,
                                          OVERALL INTEGER
                                          )'''          
        cur.execute(sql1)
        cur.execute(sql2)
        conn.close()
        return 'Review Table droped and created'

   #DML utilities to implement data requirements
   #------------------------------------------------------------------------------------------
    def findvalue(self,table,resultfield,searchfield,searchvalue):
        conn=sqlite3.connect(self.file)
        cur=conn.cursor()
        sql1="SELECT {} FROM {} WHERE {}='{}'".format(resultfield,table,searchfield,searchvalue)
        cur.execute(sql1)
        values=cur.fetchall()
        conn.close()
        if len(values)>0:
            return values[0][0]
        else:
            return 'Not Found'

    def findrecord(self,table,searchfield,searchvalue):
        conn=sqlite3.connect(self.file)
        cur=conn.cursor()
        sql1="SELECT * FROM {} WHERE {}='{}'".format(table,searchfield,searchvalue)
        cur.execute(sql1)
        records=cur.fetchall()
        conn.close()
        if len(records)>0:
            return records[0]
        else:
            return records

    def findrecords(self,sqlstatement):
        records=[]
        conn=sqlite3.connect(self.file)
        cur=conn.cursor()
        cur.execute(sqlstatement)
        records=cur.fetchall()
        conn.close()
        return records
    
    def execuresql(self,sql):
        conn=sqlite3.connect(self.file)
        cur=conn.cursor()       
        cur.execute(sql)
        conn.commit()
        conn.close()
        return 'Statement has been executed'
        
    def adduser(self,username,email,password):
        msg='No action taken'
        conn=sqlite3.connect(self.file)
        cur=conn.cursor()
        sql1="INSERT INTO USERS(USERID,EMAIL,PASSWORD) VALUES (?,?,?)"        
        
        if self.findvalue('USERS','USERID','USERID',username)==username:
            msg= 'User {} already exits'.format(username)            
        else:
            cur.execute(sql1,(username,email,password))
            conn.commit()
            msg='User {} has been added'.format(username)            
        conn.close()        
        return msg

    def userlogin(self,username):
        msg='Welcome ! {}'.format(username)

        conn=sqlite3.connect(self.file)
        cur=conn.cursor()
        currenttime=datetime.now()
        
        sql1="UPDATE USERS SET LASTSEEN=CURRENT WHERE USERID ='{}'".format(username)
        sql2="UPDATE USERS SET CURRENT='{}' WHERE USERID ='{}'".format(currenttime,username)

        if self.findvalue('USERS','USERID','USERID',username)!=username:
            msg= 'User name {} does nor exist'.format(username)            
        else:
            cur.execute(sql1)
            cur.execute(sql2)
            conn.commit()            
        conn.close()        
        return msg
 
    def addbeer(self,userid,beercode,ibu,calories,abv,style,brewerlocation,glasstype):
        msg='No action taken'
        d = datetime.now()
        only_date, only_time = d.date(), d.time()
        
        sqlstatement="select userid from beers where userid='"+userid+"' and date= '"+str(only_date)+"'"
        weeklyreviews=self.findrecords(sqlstatement)

        if len(weeklyreviews)>1:
            msg='you have already made your update for today'
        else:
            conn=sqlite3.connect(self.file)
            cur=conn.cursor()
            sql1="INSERT INTO BEERS (DATE,USERID,BEERCODE,IBU,CALORIES,ABV,STYLE,BREWERYLOCATION,GLASSTYPE,ACTIVITY,PARAMETER) VALUES (?,?,?,?,?,?,?,?,?,?,?)"       
            cur.execute(sql1,(only_date,userid,beercode,ibu,calories,abv,style,brewerlocation,glasstype,'new','1'))
            conn.commit()
            msg='Beer has been added'
            conn.close()        
        return msg

    def deletebeer(self,beercode,beerid):
        sql1="DELETE FROM BEERS WHERE BEERCODE='{}' OR ID='{}'".format(beercode,beerid)
        return self.findrecords(sql1)

    def addglass(self,userid,glasscode,name):
        msg='No action taken'
        conn=sqlite3.connect(self.file)
        cur=conn.cursor()
        sql1="INSERT INTO GLASSES (USERID,GLASSCODE,NAME) VALUES (?,?,?)"       
        cur.execute(sql1,(userid,glasscode,name))
        conn.commit()
        msg='glass has been added'            
        conn.close()        
        return msg

    def deleteglass(self,glasscode,glassid):
        sql1="DELETE FROM GLASSES WHERE GLASSCODE='{}' OR ID='{}'".format(glasscode,glassid)
        return self.findrecords(sql1)
  
    def addreview(self,userid,beercode,aroma,appearance,taste,palate,bottlestyle):

        d=datetime.now()
        only_date, only_time = d.date(), d.time()
        
        msg='No action taken'
        sql1="INSERT INTO REVIEWS (DATE,USERID,BEERCODE,AROMA,APPEARANCE,TASTE,PALATE,BOTTLESTYLE,YEARWEEK) VALUES (?,?,?,?,?,?,?,?,?)"
        sql2="update reviews set overall=(aroma+appearance+taste+palate+bottlestyle) where userid='"+userid+"'"
        
        year = datetime.today().year
        week = datetime.today().isocalendar()[1]

        sqlstatement="select userid from reviews where userid='"+userid+"' and yearweek='"+str(year)+'-'+str(week)+"' and beercode='"+beercode+"'"
        weeklyreviews=self.findrecords(sqlstatement)
        msg='You have already added your weekly review'
        
        if len(weeklyreviews)<=4:
            conn=sqlite3.connect(self.file)
            cur=conn.cursor()            
            cur.execute(sql1,(only_date,userid,beercode,aroma,appearance,taste,palate,bottlestyle,str(year)+'-'+str(week)))
            conn.commit()
            msg='Beer has been reviewed'     
            conn.close()
        self.execuresql(sql2)
        return msg

    def deletebeer(self,beercode,beerid):
        sql1="DELETE FROM BEERS WHERE BEERCODE='{}' OR ID='{}'".format(beercode,beerid)
        return self.findrecords(sql1)

    def deleteglass(self,userid,glass):
        sql1="DELETE FROM GLASSES WHERE USERID='{}' AND(GLASSCODE='{}' OR ID='{}')".format(userid,glass,glass)
        self.findrecords(sql1)
        msg=glass+ ' has been deleted please review your list'        
        return msg

    def querytreview(self,userid,beer):
        sql1="SELECT * FROM REVIEWS WHERE USERID='{}' AND BEERCODE='{}' OORDER BY DATE DESC LIMIT 10".format(userid,beer)
        return self.findrecords(sql1)
    
    def listusers(self):
        sql1="SELECT USERID FROM USERS"
        return self.findrecords(sql1)



    
