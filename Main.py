# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "home"
__date__ = "$26 Mar, 2020 12:40:37 PM$"

from collections import defaultdict
from flask import Flask
from flask import flash
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
import numpy as np
import numpy as objnumpy
import os
import pandas as objpandas
import pandas as pd
#import pygal
import pymysql
from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin
import urllib.parse as urlparse
from urllib.parse import parse_qs
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/uploads'
ALLOWED_EXTENSIONS = set(["jpg", "jpeg", "tif", "tiff", "png"])

app = Flask(__name__)
app.secret_key = "1234"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = ""
        db = "productionplaning"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
    def insertdataownerdetails(self, firstname, lastname, phone, email, address, username, password):
        print('insertdataownerdetails::' + username)
        strQuery = "INSERT INTO dataownerdetails(Firstname, Lastname, Phoneno, Emailid, Address, Username, Password, Recorded_Date) values(%s, %s, %s, %s, %s, %s, %s, now())"
        strQueryVal = (firstname, lastname, phone, email, address, username, password)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""    
    def getdataownerdetails(self, username, password):
        strQuery = "SELECT COUNT(*) AS c, UserId FROM dataownerdetails WHERE Username = '" + username + "' AND Password = '" + password + "'"        
        self.cur.execute(strQuery)        
        result = self.cur.fetchall()       
        return result
    def getprofiledetails(self, username):
        strQuery = "SELECT UserId,Firstname,Lastname,Phoneno,Address,Recorded_Date FROM dataownerdetails WHERE Username = '" + username + "' LIMIT 1"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getadmindetails(self, username, password):
        strQuery = "SELECT COUNT(*) AS c, AdminId FROM admindetails WHERE Username = '" + username + "' AND Password = '" + password + "'"        
        self.cur.execute(strQuery)        
        result = self.cur.fetchall()       
        return result    
    def getalldataownerdetails(self):
        strQuery = "SELECT UserId, Firstname, Lastname, Phoneno, Address, Recorded_Date FROM dataownerdetails ORDER BY Recorded_Date"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getimagedetails(self, imgId):
        strQuery = "SELECT i.Image "
        strQuery += "FROM productdetails AS i "
        strQuery += "WHERE i.Product_Id = (%s) "
        strQueryVal = str(imgId)
        self.cur.execute(strQuery, strQueryVal)
        result = self.cur.fetchall()
        print(result)
        return result
    def getdatacentredetailsbyname(self, name):
        strQuery = "SELECT DataCentreId, Name, Location, Pincode, Lattitude, Longitude, Recorded_Date FROM datacentredetails WHERE Name LIKE '" + name + "%' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getcountofconfigdetailsbyname(self, categoryId, sizeId):
        strQuery = "SELECT COUNT(*) AS c, ConfigId FROM configdetails WHERE CategoryId = '" + str(categoryId) + "' AND Size_Id = '" + str(sizeId) + "' "        
        self.cur.execute(strQuery)        
        result = self.cur.fetchall()       
        return result
    def insertconfigdetails(self, userId, categoryId, sizeId, min, max):
        print('insertconfigdetails::' + str(categoryId))
        strQuery = "INSERT INTO configdetails(UserId, CategoryId, Size_Id, Min_Quantity, Max_Quantity, Recorded_Date) values(%s, %s, %s, %s, %s, now())"
        strQueryVal = (userId, categoryId, sizeId, min, max)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def insertorderdetails(self, personId, userId, productId, sizeId, quantity):
        print('insertorderdetails::' + str(personId))
        print('insertorderdetails::' + str(userId))
        strQuery = "INSERT INTO orderdetails(PersonId, UserId, Product_Id, Size_Id, Quantity, Delivered, Recorded_Date) values(%s, %s, %s, %s, AES_ENCRYPT(%s, " + app.secret_key + "), '0', now())"
        strQueryVal = (str(personId), str(userId), str(productId), str(sizeId), str(quantity))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def insertproductdetails(self, userId, name, description, price, image, sizeId):
        print('insertproductdetails::' + str(userId))
        strQuery = "INSERT INTO productdetails(UserId, Name, Description, Price, Image, Size_Id, Status, Recorded_Date) values(%s, %s, %s, %s, %s, %s, '1', now())"
        strQueryVal = (str(userId), name, description, str(price), str(image), str(sizeId))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def getdataownerprofiledetails(self, name):
        strQuery = "SELECT UserId, Firstname, Lastname, Phoneno, Address, Recorded_Date FROM dataownerdetails WHERE Username = '" + name + "' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getdatacentredetailsbygeolocation(self, latitude, longitude):
        strQuery = "SELECT DataCentreId, Name, Location, Pincode, Lattitude, Longitude, Recorded_Date FROM datacentredetails WHERE Lattitude = '" + latitude + "' AND Longitude = '" + longitude + "' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getalldatacentredetails(self):
        strQuery = "SELECT DataCentreId, Name FROM datacentredetails"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def insertloandetails(self, Loan_ID, Customer_ID, Data_Centre_Id, Data_Owner_Id, Current_Loan_Amount, Term, Credit_Score, Annual_Income, Years_in_current_job, Home_Ownership, Purpose, Monthly_Debt, Years_of_Credit_History, Months_since_last_delinquent, Number_of_Open_Accounts, Number_of_Credit_Problems, Current_Credit_Balance, Maximum_Open_Credit, Bankruptcies, Tax_Liens):
        print('insertloandetails::' + Loan_ID)
        strQuery = "INSERT INTO loandetails(Loan_ID, Customer_ID, Data_Centre_Id, Data_Owner_Id, Current_Loan_Amount, Term, Credit_Score, Annual_Income, Years_in_current_job, Home_Ownership, Purpose, Monthly_Debt, Years_of_Credit_History, Months_since_last_delinquent, Number_of_Open_Accounts, Number_of_Credit_Problems, Current_Credit_Balance, Maximum_Open_Credit, Bankruptcies, Tax_Liens, Status, RecordedDate) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'In-Active', now())"
        strQueryVal = (Loan_ID, Customer_ID, Data_Centre_Id, Data_Owner_Id, Current_Loan_Amount, Term, Credit_Score, Annual_Income, Years_in_current_job, Home_Ownership, Purpose, Monthly_Debt, Years_of_Credit_History, Months_since_last_delinquent, Number_of_Open_Accounts, Number_of_Credit_Problems, Current_Credit_Balance, Maximum_Open_Credit, Bankruptcies, Tax_Liens)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""    
    def getdataowneruploadeddetails(self, dataownername):
        #strQuery = "SELECT l.LoanId, l.Loan_ID, l.Customer_ID, l.Current_Loan_Amount, l.Term, l.Credit_Score, l.Annual_Income, l.Status, dc.Name, l.RecordedDate "
        #strQuery += "FROM loandetails AS l "
        strQuery = "SELECT l.CreditCardId, l.Time, l.V1, l.V2, l.V3, l.V4, l.V5, l.V6, l.V7, l.V8, l.V9, l.V10, l.V11, l.V12, l.V13, l.V14, l.V15, l.V16, l.V17, l.V18, l.V19, l.V20, l.V21, l.V22, l.V23, l.V24, l.V25, l.V26, l.V27, l.V28, AES_DECRYPT(l.Amount, " + app.secret_key + ") AS Amount, l.Class, l.Status, dc.Name, l.RecordedDate "
        strQuery += "FROM creditcarddetails AS l "
        strQuery += "LEFT JOIN dataownerdetails AS dow ON dow.UserId = l.Data_Owner_Id "
        strQuery += "LEFT JOIN datacentredetails AS dc ON dc.DataCentreId = l.Data_Centre_Id "
        strQuery += "WHERE dow.Username = '" + dataownername + "' "
        strQuery += "ORDER BY RecordedDate DESC "
        strQuery += "LIMIT 10"        
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def updatestatus(self, userid, loadids, operation):
        print(userid)
        print('loadids::' + loadids)
        print('operation::' + operation)
        #strQuery = "UPDATE loandetails SET Status = (%s) WHERE Data_Owner_Id = (%s) AND LoanId IN " + loadids
        strQuery = "UPDATE creditcarddetails SET Status = (%s) WHERE Data_Owner_Id = (%s) AND CreditCardId IN " + loadids
        strQueryVal = (operation, str(userid))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""   
    def deleteloandetails(self, loanId):
        print(loanId)
        #strQuery = "DELETE FROM loandetails WHERE LoanId = (%s) " 
        strQuery = "DELETE FROM creditcarddetails WHERE CreditCardId = (%s) " 
        strQueryVal = (str(loanId))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""   
    def getdataownerloaddetails(self, dataCentreId, userId):
        #strQuery = "SELECT l.LoanId, l.Loan_ID, l.Customer_ID, l.Current_Loan_Amount, l.Term, l.Credit_Score, l.Annual_Income, l.Status, dc.Name, l.RecordedDate "
        #strQuery += "FROM loandetails AS l "
        strQuery = "SELECT l.CreditCardId, l.Time, l.V1, l.V2, l.V3, l.V4, l.V5, l.V6, l.V7, l.V8, l.V9, l.V10, l.V11, l.V12, l.V13, l.V14, l.V15, l.V16, l.V17, l.V18, l.V19, l.V20, l.V21, l.V22, l.V23, l.V24, l.V25, l.V26, l.V27, l.V28, AES_DECRYPT(l.Amount, " + app.secret_key + ") AS Amount, l.Class, l.Status, dc.Name, l.RecordedDate "
        strQuery += "FROM creditcarddetails AS l "
        strQuery += "LEFT JOIN dataownerdetails AS dow ON dow.UserId = l.Data_Owner_Id "
        strQuery += "LEFT JOIN datacentredetails AS dc ON dc.DataCentreId = l.Data_Centre_Id "
        strQuery += "WHERE l.Data_Owner_Id = '" + userId + "' "
        strQuery += "AND l.Data_Centre_Id = '" + dataCentreId + "' "
        strQuery += "ORDER BY RecordedDate DESC "
        strQuery += "LIMIT 10" 
        print(strQuery)
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getdatacentredetailsbydataCentreId(self, dataCentreId):
        strQuery = "SELECT DataCentreId, Name FROM datacentredetails WHERE DataCentreId = '" + dataCentreId + "'"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getdatacentredetails(self, username, password):
        strQuery = "SELECT COUNT(*) AS c, DataCentreId FROM datacentredetails WHERE Username = '" + username + "' AND Password = '" + password + "'"        
        self.cur.execute(strQuery)        
        result = self.cur.fetchall()       
        return result
    def getdatacentreprofiledetails(self, dataCentreId):
        strQuery = "SELECT DataCentreId,Name,Location,Pincode,Lattitude,Longitude,Username,Password,Recorded_Date FROM datacentredetails WHERE DataCentreId = '" + str(dataCentreId) + "' LIMIT 1"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getdatamovementdetails(self, Data_Centre_Id):
        #strQuery = "SELECT l.LoanId, l.Loan_ID, l.Customer_ID, l.Current_Loan_Amount, l.Term, l.Credit_Score, l.Annual_Income, l.Status, dc.Name, dow.Firstname, dow.Lastname, l.RecordedDate "
        #strQuery += "FROM loandetails AS l "
        strQuery = "SELECT l.CreditCardId, l.Time, l.V1, l.V2, l.V3, l.V4, l.V5, l.V6, l.V7, l.V8, l.V9, l.V10, l.V11, l.V12, l.V13, l.V14, l.V15, l.V16, l.V17, l.V18, l.V19, l.V20, l.V21, l.V22, l.V23, l.V24, l.V25, l.V26, l.V27, l.V28, AES_DECRYPT(l.Amount, " + app.secret_key + ") AS Amount, l.Class, l.Status, dc.Name, dow.Firstname, dow.Lastname, l.RecordedDate "
        strQuery += "FROM creditcarddetails AS l "
        strQuery += "LEFT JOIN dataownerdetails AS dow ON dow.UserId = l.Data_Owner_Id "
        strQuery += "LEFT JOIN datacentredetails AS dc ON dc.DataCentreId = l.Data_Centre_Id "
        strQuery += "WHERE l.Status = 'move' "
        strQuery += "AND l.Data_Centre_Id = '" + Data_Centre_Id + "' "
        strQuery += "ORDER BY RecordedDate DESC "
        strQuery += "LIMIT 10"        
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def updatedatamovementstatus(self, userid, loadids, operation):
        print(userid)
        print('loadids::' + loadids)
        print('operation::' + operation)
        #strQuery = "UPDATE loandetails SET Status = (%s), Data_Centre_Id = (%s) WHERE LoanId IN " + loadids
        strQuery = "UPDATE creditcarddetails SET Status = (%s), Data_Centre_Id = (%s) WHERE CreditCardId IN " + loadids
        strQueryVal = (operation, str(userid))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""   
    def getdatafortaskdetails(self, Data_Centre_Id):
        #strQuery = "SELECT l.LoanId, l.Loan_ID, l.Customer_ID, l.Current_Loan_Amount, l.Term, l.Credit_Score, l.Annual_Income, l.Status, dc.Name, dow.Firstname, dow.Lastname, l.RecordedDate "
        #strQuery += "FROM loandetails AS l "
        strQuery = "SELECT l.CreditCardId, l.Time, l.V1, l.V2, l.V3, l.V4, l.V5, l.V6, l.V7, l.V8, l.V9, l.V10, l.V11, l.V12, l.V13, l.V14, l.V15, l.V16, l.V17, l.V18, l.V19, l.V20, l.V21, l.V22, l.V23, l.V24, l.V25, l.V26, l.V27, l.V28, AES_DECRYPT(l.Amount, " + app.secret_key + ") AS Amount, l.Class, l.Status, dc.Name, dow.Firstname, dow.Lastname, l.RecordedDate "
        strQuery += "FROM creditcarddetails AS l "
        strQuery += "LEFT JOIN dataownerdetails AS dow ON dow.UserId = l.Data_Owner_Id "
        strQuery += "LEFT JOIN datacentredetails AS dc ON dc.DataCentreId = l.Data_Centre_Id "
        strQuery += "WHERE l.Status NOT IN ('move', 'In-Active', 'Accept', 'Reject') "
        strQuery += "AND l.Data_Centre_Id = '" + Data_Centre_Id + "' "
        strQuery += "ORDER BY RecordedDate DESC "
        strQuery += "LIMIT 10"        
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def updatetaskstatus(self, userid, loadids, operation):
        print(userid)
        print('loadids::' + loadids)
        print('operation::' + operation)
        #strQuery = "UPDATE loandetails SET Status = (%s) WHERE Data_Centre_Id = (%s) AND LoanId IN " + loadids
        strQuery = "UPDATE creditcarddetails SET Status = (%s) WHERE Data_Centre_Id = (%s) AND CreditCardId IN " + loadids
        strQueryVal = (operation, str(userid))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def insertcreditcarddetails(self, Data_Centre_Id, Data_Owner_Id, Time, V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25, V26, V27, V28, Amount, Class):
        print('insertcreditcarddetails::' + V1)
        strQuery = "INSERT INTO creditcarddetails(Data_Centre_Id, Data_Owner_Id, Time, V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25, V26, V27, V28, Amount, Class, Status, RecordedDate) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, AES_ENCRYPT(%s, " + app.secret_key + "), %s, 'In-Active', now())"
        strQueryVal = (Data_Centre_Id, Data_Owner_Id, Time, V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20, V21, V22, V23, V24, V25, V26, V27, V28, Amount, Class)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""   
    def getaccepteddataownerdetails(self, dataownername):
        #strQuery = "SELECT l.LoanId, l.Loan_ID, l.Customer_ID, l.Current_Loan_Amount, l.Term, l.Credit_Score, l.Annual_Income, l.Status, dc.Name, l.RecordedDate "
        #strQuery += "FROM loandetails AS l "
        strQuery = "SELECT COUNT(*) AS c "
        strQuery += "FROM creditcarddetails AS l "
        strQuery += "LEFT JOIN dataownerdetails AS dow ON dow.UserId = l.Data_Owner_Id "
        strQuery += "LEFT JOIN datacentredetails AS dc ON dc.DataCentreId = l.Data_Centre_Id "
        strQuery += "WHERE dow.Username = '" + dataownername + "' "
        strQuery += "AND l.Status = 'Accept' "
        strQuery += "ORDER BY RecordedDate DESC "
        strQuery += "LIMIT 10"        
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getvalidationdataownerdetails(self, dataownername):
        #strQuery = "SELECT l.LoanId, l.Loan_ID, l.Customer_ID, l.Current_Loan_Amount, l.Term, l.Credit_Score, l.Annual_Income, l.Status, dc.Name, l.RecordedDate "
        #strQuery += "FROM loandetails AS l "
        strQuery = "SELECT COUNT(*) AS c "
        strQuery += "FROM creditcarddetails AS l "
        strQuery += "LEFT JOIN dataownerdetails AS dow ON dow.UserId = l.Data_Owner_Id "
        strQuery += "LEFT JOIN datacentredetails AS dc ON dc.DataCentreId = l.Data_Centre_Id "
        strQuery += "WHERE dow.Username = '" + dataownername + "' "
        strQuery += "AND l.Status = 'validate' "
        strQuery += "ORDER BY RecordedDate DESC "
        strQuery += "LIMIT 10"        
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getmovedataownerdetails(self, dataownername):
        #strQuery = "SELECT l.LoanId, l.Loan_ID, l.Customer_ID, l.Current_Loan_Amount, l.Term, l.Credit_Score, l.Annual_Income, l.Status, dc.Name, l.RecordedDate "
        #strQuery += "FROM loandetails AS l "
        strQuery = "SELECT COUNT(*) AS c "
        strQuery += "FROM creditcarddetails AS l "
        strQuery += "LEFT JOIN dataownerdetails AS dow ON dow.UserId = l.Data_Owner_Id "
        strQuery += "LEFT JOIN datacentredetails AS dc ON dc.DataCentreId = l.Data_Centre_Id "
        strQuery += "WHERE dow.Username = '" + dataownername + "' "
        strQuery += "AND l.Status = 'move' "
        strQuery += "ORDER BY RecordedDate DESC "
        strQuery += "LIMIT 10"        
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getpersonaldetails(self, username, password):
        strQuery = "SELECT COUNT(*) AS c, PersonId FROM personaldetails WHERE Username = '" + username + "' AND Password = '" + password + "'"        
        self.cur.execute(strQuery)        
        result = self.cur.fetchall()       
        return result
    def getuserprofiledetails(self, username):
        strQuery = "SELECT PersonId,Firstname,Lastname,Phoneno,Address,Recorded_Date FROM personaldetails WHERE Username = '" + username + "' LIMIT 1"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def insertpersonaldetails(self, firstname, lastname, phone, email, address, username, password):
        print('insertpersonaldetails::' + username)
        strQuery = "INSERT INTO personaldetails(Firstname, Lastname, Phoneno, Emailid, Address, Username, Password, Recorded_Date) values(%s, %s, %s, %s, %s, %s, %s, now())"
        strQueryVal = (firstname, lastname, phone, email, address, username, password)
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""    
    def getuserpersonaldetails(self, name):
        strQuery = "SELECT PersonId, Firstname, Lastname, Phoneno, Address, Recorded_Date FROM personaldetails WHERE Username = '" + name + "' "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getconfigdetails(self, userId):
        strQuery = "SELECT c.ConfigId, ca.Name, s.Standard_Sheet_Length, s.Overall_Profile_Width, s.Effective_Cover_Width, s.Minimum_Roof_Slope, c.Min_Quantity, c.Max_Quantity, c.Recorded_Date "
        strQuery += "FROM configdetails AS c ";
        strQuery += "LEFT JOIN categorydetails AS ca ON ca.CategoryId = c.CategoryId ";
        strQuery += "LEFT JOIN sizedetails AS s ON s.Size_Id = c.Size_Id ";
        strQuery += "LEFT JOIN dataownerdetails AS d ON d.UserId = c.UserId ";
        strQuery += "WHERE d.UserId = '" + str(userId) + "' "
        strQuery += "ORDER BY ConfigId DESC ";
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getuserdetails(self):
        strQuery = "SELECT PersonId, Firstname, Lastname, Phoneno, Address, Recorded_Date FROM personaldetails ORDER BY PersonId DESC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getorderdetails(self, userId):
        strQuery = "SELECT o.OrderId, o.PersonId, o.Product_Id, o.Size_Id, AES_DECRYPT(o.Quantity, " + app.secret_key + ") AS Quantity, o.Production_Date, o.Updated_Date, o.Recorded_Date, m.Firstname, m.Lastname, p.Name "
        strQuery += "FROM orderdetails AS o "
        strQuery += "LEFT JOIN productdetails AS p ON p.Product_Id = o.Product_Id "
        strQuery += "LEFT JOIN dataownerdetails AS d ON d.UserId = p.UserId "
        strQuery += "LEFT JOIN personaldetails AS m ON  m.PersonId = o.PersonId "
        strQuery += "WHERE d.UserId = " + str(userId) + " "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getuserorderdetails(self, userId):
        strQuery = "SELECT o.OrderId, o.PersonId, o.Product_Id, o.Size_Id, AES_DECRYPT(o.Quantity, " + app.secret_key + ") AS Quantity, o.Production_Date, o.Updated_Date, o.Recorded_Date, d.Firstname, p.Name "
        strQuery += "FROM orderdetails AS o "
        strQuery += "LEFT JOIN productdetails AS p ON p.Product_Id = o.Product_Id "
        strQuery += "LEFT JOIN dataownerdetails AS d ON d.UserId = p.UserId "
        strQuery += "LEFT JOIN personaldetails AS m ON m.PersonId = o.PersonId "
        strQuery += "WHERE m.PersonId = " + str(userId) + " "
        strQuery += "ORDER BY o.Recorded_Date DESC "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getorders(self, orderId):
        strQuery = "SELECT o.OrderId, o.PersonId, o.Product_Id, o.Size_Id, AES_DECRYPT(o.Quantity, " + app.secret_key + ") AS Quantity, o.Production_Date, o.Updated_Date, o.Recorded_Date, o.Delivered, o.Delivered_Date,  m.Firstname, m.Lastname, p.Name, d.Firstname AS OwnerName "
        strQuery += "FROM orderdetails AS o "
        strQuery += "LEFT JOIN productdetails AS p ON p.Product_Id = o.Product_Id "
        strQuery += "LEFT JOIN dataownerdetails AS d ON d.UserId = p.UserId "
        strQuery += "LEFT JOIN personaldetails AS m ON  m.PersonId = o.PersonId "
        strQuery += "WHERE o.OrderId = " + str(orderId) + " "
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getproducts(self, productId):
        strQuery = "SELECT Product_Id, UserId, Name, Description, Price, Image, Size_Id, Status, Recorded_Date FROM productdetails WHERE Product_Id = " + str(productId) + " AND Status = 1 ORDER BY Product_Id DESC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getproductsbyuserid(self, productId, userId):
        strQuery = "SELECT Product_Id, UserId, Name, Description, Price, Image, Size_Id, Status, Recorded_Date FROM productdetails WHERE Product_Id = " + str(productId) + " AND UserId = " + str(userId) + " AND Status = 1 ORDER BY Product_Id DESC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getproductdetails(self, userId):
        strQuery = "SELECT Product_Id, UserId, Name, Description, Price, Image, Size_Id, Status, Recorded_Date FROM productdetails WHERE UserId = " + str(userId) + " AND Status = 1 ORDER BY Product_Id DESC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getallproductdetails(self):
        strQuery = "SELECT Product_Id, UserId, Name, Description, Price, Image, Size_Id, Status, Recorded_Date FROM productdetails WHERE Status = 1 ORDER BY Product_Id DESC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getallsizedetails(self):
        strQuery = "SELECT Size_Id, Sheet_Thickness, Standard_Sheet_Length, Overall_Profile_Width, Effective_Cover_Width, Minimum_Roof_Slope, Recorded_Date FROM sizedetails WHERE Status = 1 ORDER BY Size_Id DESC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result    
    def getsizedetailsbythickness(self, sheetThickness):
        strQuery = "SELECT CategoryId FROM categorydetails WHERE Name IN ('" + str(sheetThickness) + "') ORDER BY CategoryId DESC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getsizedetailsbylength(self, sheetThickness, standardSheetLength):
        strQuery = "SELECT Size_Id, Sheet_Thickness, Standard_Sheet_Length, Overall_Profile_Width, Effective_Cover_Width, Minimum_Roof_Slope, Recorded_Date FROM sizedetails WHERE Sheet_Thickness IN ('" + str(sheetThickness) + "') AND Standard_Sheet_Length IN ('" + str(standardSheetLength) + "') ORDER BY Size_Id DESC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getsizedetails(self, sizes):
        strQuery = "SELECT Size_Id, Sheet_Thickness, Standard_Sheet_Length, Overall_Profile_Width, Effective_Cover_Width, Minimum_Roof_Slope, Recorded_Date FROM sizedetails WHERE Size_Id IN (" + str(sizes) + ") AND Status = 1 ORDER BY Size_Id DESC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getsearchdetails(self, amt):
        strQuery = "SELECT l.CreditCardId, l.Time, l.V1, l.V2, l.V3, l.V4, l.V5, l.V6, l.V7, l.V8, l.V9, l.V10, l.V11, l.V12, l.V13, l.V14, l.V15, l.V16, l.V17, l.V18, l.V19, l.V20, l.V21, l.V22, l.V23, l.V24, l.V25, l.V26, l.V27, l.V28, AES_DECRYPT(l.Amount, " + app.secret_key + ") AS Amount, l.Class, l.Status, dc.Name, dow.Firstname, dow.Lastname, l.RecordedDate "
        strQuery += "FROM creditcarddetails AS l "
        strQuery += "LEFT JOIN dataownerdetails AS dow ON dow.UserId = l.Data_Owner_Id "
        strQuery += "LEFT JOIN datacentredetails AS dc ON dc.DataCentreId = l.Data_Centre_Id "
        strQuery += "WHERE AES_DECRYPT(l.Amount, " + app.secret_key + ") <= " + amt
        strQuery += " ORDER BY RecordedDate DESC "
        strQuery += "LIMIT 10"           
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getgraphdetails(self, dataownername):
        strQuery = "SELECT COUNT(*) AS c, " 
        strQuery += "CASE "
        strQuery += "WHEN Class = 0 THEN 'Fragmented Data' "
        strQuery += "ELSE 'Unfragmented Data' "
        strQuery += "END AS Class "
        strQuery += "FROM creditcarddetails "        
        strQuery += "GROUP BY Class "   
        print(strQuery)
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result

class PandasLabelEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.label_dict = defaultdict(list)

    def fit(self, X):
        X = X.astype('category')
        cols = X.columns
        values = list(map(lambda col: X[col].cat.categories, cols))
        self.label_dict = dict(zip(cols, values))
        # return as category for xgboost or lightgbm 
        return self

    def transform(self, X):
        # check missing columns
        missing_col = set(X.columns)-set(self.label_dict.keys())
        if missing_col:
            raise ValueError('the column named {} is not in the label dictionary. Check your fitting data.'.format(missing_col)) 
        return X.apply(lambda x: x.astype('category').cat.set_categories(self.label_dict[x.name]).cat.codes.astype('category').cat.set_categories(objnumpy.arange(len(self.label_dict[x.name]))))

    def inverse_transform(self, X):
        return X.apply(lambda x: objpandas.Categorical.from_codes(codes=x.values,
                       categories=self.label_dict[x.name]))
    
@app.route('/', methods=['GET'])
def loadindexpage():
    return render_template('index.html')

@app.route('/viewdata', methods=['GET'])
def viewdata():
    parsed = urlparse.urlparse(request.url)
    
    dataCentreId = parse_qs(parsed.query)['index'][0]
    print(dataCentreId)
    
    userId = parse_qs(parsed.query)['index1'][0]
    print(userId)
    
    try:
        if dataCentreId is not "" and userId is not "":            
            def db_query():
                db = Database()
                emps = db.getdataownerloaddetails(dataCentreId, userId)    
                return emps
            viewdata = db_query()
            flash ('Dear Customer, Your request has been processed sucessfully!')
            return render_template('viewdata.html', sessionValue=session['x'], viewdataresult=viewdata, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('viewdata.html', sessionValue=session['x'], viewdataresult=viewdata, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('viewdata.html', sessionValue=session['x'], viewdataresult=viewdata, content_type='application/json')
    
    return render_template('viewdata.html', sessionValue=session['x'], viewdataresult=viewdata, content_type='application/json')

@app.route('/loaddata', methods=['GET'])
def loaddata():
    parsed = urlparse.urlparse(request.url)
    
    dataCentreId = parse_qs(parsed.query)['index'][0]
    print(dataCentreId)
    
    userId = parse_qs(parsed.query)['index1'][0]
    print(userId)
    
    try:
        if dataCentreId is not "" and userId is not "":            
            def db_query():
                db = Database()
                emps = db.getdatacentredetailsbydataCentreId(dataCentreId)
                return emps
            centreresult = db_query()
            flash ('Dear Customer, Your request has been processed sucessfully!')
            return render_template('loaddata.html', sessionValue=session['x'], loaddataresult=centreresult, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('loaddata.html', sessionValue=session['x'], loaddataresult=centreresult, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('loaddata.html', sessionValue=session['x'], loaddataresult=centreresult, content_type='application/json')
    
    return render_template('loaddata.html', sessionValue=session['x'], loaddataresult=centreresult, content_type='application/json')

@app.route('/uploaddata', methods=['GET'])
def uploaddata():
    def db_query():
        db = Database()
        emps = db.getalldatacentredetails()       
        return emps
    centreresult = db_query()
    return render_template('uploaddata.html', sessionValue=session['x'], datacentreresult=centreresult, content_type='application/json')

@app.route('/codeuploaddata', methods=['POST'])
def codeuploaddata(): 
    file = request.files['filepath']
    datacentreid = request.form.get('datacentre')
    
    print('filename:' + file.filename)
    print('datacentreid:' + datacentreid)
        
    def db_query():
        db = Database()
        emps = db.getalldatacentredetails()       
        return emps
    centreresult = db_query()
  
    if 'filepath' not in request.files:
        flash ('Please fill all mandatory fields.')
        return render_template('uploaddata.html', sessionValue=session['x'], datacentreresult=centreresult, content_type='application/json')
    
    if file.filename != '' and datacentreid is not "select":

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            filepath = UPLOAD_FOLDER + "/" + file.filename

            print('filepath:' + filepath)

            data = pd.read_csv(filepath)  
            
            # print info about columns in the dataframe 
            print(data.info()) 
            
            # Dropped all the Null, Empty, NA values from csv file 
            csvrows = data.dropna(axis=0, how='any') 

            count = len(csvrows);
            
            print('Length of Data::', count)

            for i in range(count):                
                if i == 0:
                    print(count)
                else:
                    db = Database()
                    #db.insertloandetails(str(np.array(csvrows['Loan ID'])[i]), str(np.array(csvrows['Customer ID'])[i]), datacentreid, session['UID'], str(np.array(csvrows['Current Loan Amount'])[i]), str(np.array(csvrows['Term'])[i]), str(np.array(csvrows['Credit Score'])[i]), str(np.array(csvrows['Annual Income'])[i]), str(np.array(csvrows['Years in current job'])[i]), str(np.array(csvrows['Home Ownership'])[i]), str(np.array(csvrows['Purpose'])[i]), str(np.array(csvrows['Monthly Debt'])[i]), str(np.array(csvrows['Years of Credit History'])[i]), str(np.array(csvrows['Months since last delinquent'])[i]), str(np.array(csvrows['Number of Open Accounts'])[i]), str(np.array(csvrows['Number of Credit Problems'])[i]), str(np.array(csvrows['Current Credit Balance'])[i]), str(np.array(csvrows['Maximum Open Credit'])[i]), str(np.array(csvrows['Bankruptcies'])[i]), str(np.array(csvrows['Tax Liens'])[i]))  
                    db.insertcreditcarddetails(datacentreid, session['UID'], str(np.array(csvrows['Time'])[i]), str(np.array(csvrows['V1'])[i]), str(np.array(csvrows['V2'])[i]), str(np.array(csvrows['V3'])[i]), str(np.array(csvrows['V4'])[i]), str(np.array(csvrows['V5'])[i]), str(np.array(csvrows['V6'])[i]), str(np.array(csvrows['V7'])[i]), str(np.array(csvrows['V8'])[i]), str(np.array(csvrows['V9'])[i]), str(np.array(csvrows['V10'])[i]), str(np.array(csvrows['V11'])[i]), str(np.array(csvrows['V12'])[i]), str(np.array(csvrows['V13'])[i]), str(np.array(csvrows['V14'])[i]), str(np.array(csvrows['V15'])[i]), str(np.array(csvrows['V16'])[i]), str(np.array(csvrows['V17'])[i]), str(np.array(csvrows['V18'])[i]), str(np.array(csvrows['V19'])[i]), str(np.array(csvrows['V20'])[i]), str(np.array(csvrows['V21'])[i]), str(np.array(csvrows['V22'])[i]), str(np.array(csvrows['V23'])[i]), str(np.array(csvrows['V24'])[i]), str(np.array(csvrows['V25'])[i]), str(np.array(csvrows['V26'])[i]), str(np.array(csvrows['V27'])[i]), str(np.array(csvrows['V28'])[i]), str(np.array(csvrows['Amount'])[i]), str(np.array(csvrows['Class'])[i])) 
                   
            flash('File successfully uploaded!')
            return render_template('uploaddata.html', sessionValue=session['x'], datacentreresult=centreresult, content_type='application/json')

        else:
            flash('Allowed file types are .xls, .csv, .xlsx')
            return render_template('uploaddata.html', sessionValue=session['x'], datacentreresult=centreresult, content_type='application/json')
    else:
        flash ('Please fill all mandatory fields.')           
        return render_template('uploaddata.html', sessionValue=session['x'], datacentreresult=centreresult, content_type='application/json')
    
@app.route('/viewuploadeddata', methods=['GET'])
def viewuploadeddata():
    def db_query():
        db = Database()
        emps = db.getdataowneruploadeddetails(session['x'])       
        return emps
    profile_res = db_query()
    return render_template('viewuploadeddata.html', sessionValue=session['x'], viewdataresult=profile_res, content_type='application/json')

@app.route('/codeviewuploadeddata', methods=['POST'])
def codeviewuploadeddata():    
    operation = request.form['operation']
    print('operation:' + operation)
    
    data = request.form.getlist('data')
    print(data)
            
    def db_query():
        db = Database()
        emps = db.getdataowneruploadeddetails(session['x'])       
        return emps
    profile_res = db_query()
    
    try:
        if len(data) > 0 and operation is not "select": 
            loadids = '('
            
            for s in data:
                loadids += '' + s + '' + ','
                print(s)
               
            loadids = loadids[: len(loadids) - 1]
            loadids += ')'
            
            print(loadids)
                
            db = Database()
            db.updatestatus(session['UID'], loadids, operation)
        
            def db_query():
                db = Database()
                emps = db.getdataowneruploadeddetails(session['x'])       
                return emps
            profile_res = db_query()
    
            flash ('Dear Customer, Your request has been processed sucessfully!')
            return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')   
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    
    return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
        
@app.route('/deletedata', methods=['GET'])
def deletedata():
    parsed = urlparse.urlparse(request.url)
    print(parse_qs(parsed.query)['index'])
    
    loanId = parse_qs(parsed.query)['index']
    print(loanId)
    
    try:
        if loanId is not "": 
            
            db = Database()
            db.deleteloandetails(loanId[0])
            
            def db_query():
                db = Database()
                emps = db.getdataowneruploadeddetails(session['x'])    
                return emps
            profile_res = db_query()
            flash ('Dear Customer, Your request has been processed sucessfully!')
            return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('viewuploadeddata.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/codeindex', methods=['POST'])
def codeindex():
    username = request.form['username']
    password = request.form['password']
    
    print('username:' + username)
    print('password:' + password)
    
    try:
        if username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getdataownerdetails(username, password)       
                return emps
            res = db_query()
            
            for row in res:
                print(row['c'])
                count = row['c']
                
                if count >= 1:      
                    session['x'] = username;
                    session['UID'] = row['UserId'];
                    def db_query():
                        db = Database()
                        emps = db.getprofiledetails(username)       
                        return emps
                    profile_res = db_query()
                    return render_template('profile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
                else:
                    flash ('Incorrect Username or Password.')
                    return render_template('index.html')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('index.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('index.html')
        
    return render_template('index.html')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/datamovement', methods=['GET'])
def datamovement():
    def db_query():
        db = Database()
        emps = db.getdatamovementdetails(str(session['UID']))       
        return emps
    profile_res = db_query()
    
    def db_query():
        db = Database()
        emps = db.getalldatacentredetails()       
        return emps
    centreresult = db_query()
    return render_template('datamovement.html', sessionValue=session['x'], result=profile_res, datacentreresult=centreresult, content_type='application/json')

@app.route('/codedatamovement', methods=['POST'])
def codedatamovement():
    operation = request.form['operation']
    print('operation:' + operation)
    
    datacentre = request.form['datacentre']
    print('datacentre:' + datacentre)
    
    data = request.form.getlist('data')
    print(data)
           
    def db_query():
        db = Database()
        emps = db.getalldatacentredetails()       
        return emps
    centreresult = db_query()
    
    def db_query():
        db = Database()
        emps = db.getdatamovementdetails(str(session['UID']))       
        return emps
    profile_res = db_query()
    
    try:
        if len(data) > 0 and operation is not "select" and datacentre is not "select": 
            
            if operation != 'Reject':                
                loadids = '('

                for s in data:
                    loadids += '' + s + '' + ','
                    print(s)

                loadids = loadids[: len(loadids) - 1]
                loadids += ')'

                print(loadids)

                db = Database()
                db.updatedatamovementstatus(datacentre, loadids, operation)

                def db_query():
                    db = Database()
                    emps = db.getdatamovementdetails(str(session['UID']))       
                    return emps
                profile_res = db_query()

                flash ('Dear Customer, Your request has been processed sucessfully!')
                return render_template('datamovement.html', sessionValue=session['x'], result=profile_res, datacentreresult=centreresult, content_type='application/json')            
            else:
                flash ('Dear Customer, Your request has been rejected sucessfully!')
                return render_template('datamovement.html', sessionValue=session['x'], result=profile_res, datacentreresult=centreresult, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('datamovement.html', sessionValue=session['x'], result=profile_res, datacentreresult=centreresult, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('datamovement.html', sessionValue=session['x'], result=profile_res, datacentreresult=centreresult, content_type='application/json')
    
    return render_template('datamovement.html', sessionValue=session['x'], result=profile_res, datacentreresult=centreresult, content_type='application/json')

@app.route('/viewtask', methods=['GET'])
def viewtask():
    def db_query():
        db = Database()
        emps = db.getdatafortaskdetails(str(session['UID']))       
        return emps
    profile_res = db_query()
    return render_template('viewtask.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/codeviewtask', methods=['POST'])
def codeviewtask():
    operation = request.form['operation']
    print('operation:' + operation)
    
    data = request.form.getlist('data')
    print(data)
     
    def db_query():
        db = Database()
        emps = db.getdatafortaskdetails(str(session['UID']))       
        return emps
    profile_res = db_query()
    
    try:
        if len(data) > 0 and operation is not "select": 
            
            if operation != 'Reject':                
                
                loadids = '('

                for s in data:
                    loadids += '' + s + '' + ','
                    print(s)

                loadids = loadids[: len(loadids) - 1]
                loadids += ')'

                print(loadids)

                db = Database()
                db.updatetaskstatus(str(session['UID']), loadids, 'Accept')

                def db_query():
                    db = Database()
                    emps = db.getdatafortaskdetails(str(session['UID']))       
                    return emps
                profile_res = db_query()

                flash ('Dear Customer, Your request has been processed sucessfully!')
                return render_template('viewtask.html', sessionValue=session['x'], result=profile_res, content_type='application/json')   
            else:
                flash ('Dear Customer, Your request has been rejected sucessfully!')
                return render_template('viewtask.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('viewtask.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('viewtask.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
    
    return render_template('viewtask.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/datacentre', methods=['GET'])
def datacentre():
    return render_template('datacentre.html')

@app.route('/codedatacentre', methods=['POST'])
def codedatacentre():
    username = request.form['username']
    password = request.form['password']
    
    print('username:' + username)
    print('password:' + password)
    
    try:
        if username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getdatacentredetails(username, password)       
                return emps
            res = db_query()
            
            for row in res:
                print(row['c'])
                count = row['c']
                
                if count >= 1:      
                    session['x'] = username;
                    session['UID'] = row['DataCentreId'];
                    def db_query():
                        db = Database()
                        emps = db.getdatacentreprofiledetails(session['UID'])       
                        return emps
                    profile_res = db_query()
                    return render_template('viewdatacenterprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
                else:
                    flash ('Incorrect Username or Password.')
                    return render_template('datacentre.html')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('datacentre.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('datacentre.html')
        
    return render_template('datacentre.html')

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route('/graph', methods=['GET'])
def graph():
    labels = ["Validate", "Movement", "Completed"]
    
    def accepteddb_query():
        db = Database()
        emps = db.getaccepteddataownerdetails(session['x'])       
        return emps
    res = accepteddb_query()

    acceptcount = 0;

    for row in res:
        print(row['c'])
        acceptcount = row['c']
        
    def validationdb_query():
        db = Database()
        emps = db.getvalidationdataownerdetails(session['x'])       
        return emps
    res = validationdb_query()

    validationcount = 0;

    for row in res:
        print(row['c'])
        validationcount = row['c']
    
    def movedb_query():
        db = Database()
        emps = db.getmovedataownerdetails(session['x'])       
        return emps
    res = movedb_query()

    movecount = 0;

    for row in res:
        print(row['c'])
        movecount = row['c']
                            
    values = [validationcount, movecount, acceptcount]

    return render_template('graph.html', sessionValue=session['x'], values=values, labels=labels)

@app.route('/viewdatacenterprofile', methods=['GET'])
def viewdatacenterprofile():
    def db_query():
        db = Database()
        emps = db.getdatacentreprofiledetails(session['UID'])       
        return emps
    profile_res = db_query()
    return render_template('viewdatacenterprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/adddatacentre', methods=['GET'])
def adddatacentre():
    return render_template('adddatacentre.html', sessionValue=session['x'])

@app.route('/nearbydatacentre', methods=['GET'])
def nearbydatacentre():
    return render_template('nearbydatacentre.html', sessionValue=session['x'])

@app.route('/codenearbydatacentre', methods=['POST'])
def codenearbydatacentre():
    location = request.form['location']
    pincode = request.form['pincode']
    
    print('location:' + location)
    print('pincode:' + pincode)
    
    try:
        if location is not "" and pincode is not "": 
            def db_query():
                db = Database()
                #latitude, longitude = FindLocation.getlatlongpositions(location, pincode)
                latitude = '11.7439'
                longitude = '79.7456'
                emps = db.getdatacentredetailsbygeolocation(str(latitude), str(longitude))
                return emps
            profile_res = db_query()
            return render_template('codenearbydatacentre.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('codenearbydatacentre.html', sessionValue=session['x'])
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('codenearbydatacentre.html', sessionValue=session['x'])
        
    return render_template('codenearbydatacentre.html', sessionValue=session['x'])

@app.route('/searchdatacentre', methods=['GET'])
def searchdatacentre():
    return render_template('searchdatacentre.html', sessionValue=session['x'])

@app.route('/codesearchdatacentre', methods=['POST'])
def codesearchdatacentre():
    datacentredetailsname = request.form['name']
    
    print('datacentredetailsname:' + datacentredetailsname)
    
    try:
        if datacentredetailsname is not "": 
            def db_query():
                db = Database()
                emps = db.getdatacentredetailsbyname(datacentredetailsname)
                return emps
            profile_res = db_query()
            return render_template('codesearchdatacentre.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('searchdatacentre.html', sessionValue=session['x'])
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('searchdatacentre.html', sessionValue=session['x'])
        
    return render_template('searchdatacentre.html', sessionValue=session['x'])

@app.route('/viewprofile', methods=['GET'])
def viewprofile():
    def db_query():
        db = Database()
        emps = db.getdataownerprofiledetails(session['x'])       
        return emps
    profile_res = db_query()
    return render_template('profile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/home', methods=['GET'])
def home():
    def db_query():
        db = Database()
        emps = db.getalldataownerdetails()       
        return emps
    profile_res = db_query()
    return render_template('viewdataowners.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/codeadmin', methods=['POST'])
def codeadmin():
    username = request.form['username']
    password = request.form['password']
    
    print('username:' + username)
    print('password:' + password)
    
    try:
        if username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getadmindetails(username, password)       
                return emps
            res = db_query()
            
            for row in res:
                print(row['c'])
                count = row['c']
                
                if count >= 1:      
                    session['x'] = username;
                    session['UID'] = row['AdminId'];
                    def db_query():
                        db = Database()
                        emps = db.getuserdetails()       
                        return emps
                    profile_res = db_query()
                    return render_template('viewusers.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
                else:
                    flash ('Incorrect Username or Password.')
                    return render_template('admin.html')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('admin.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('admin.html')
        
    return render_template('admin.html')

@app.route('/signin', methods=['GET'])
def signin():
    return render_template('signin.html')

@app.route('/signout', methods=['GET'])
def signout():    
    return render_template('signout.html')

@app.route('/logout', methods=['GET'])
def logout():
    del session['x']
    return render_template('index.html')

@app.route('/codesignin', methods=['POST'])
def codesignin():
    firstname = request.form['firstname']
    lastname = "-"
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']    
    username = request.form['username']
    password = request.form['password']
    
    print('firstname:', firstname)
    print('lastname:', lastname)
    print('phone:', phone)
    print('email:', email)
    print('address:', address)
    print('username:', username)
    print('password:', password)
    
    try:
        if firstname is not "" and lastname is not ""  and phone is not "" and email is not "" and address is not "" and username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getdataownerdetails(username, password)       
                return emps
            res = db_query()

            for row in res:
                print(row['c'])
                count = row['c']

                if count >= 1:      
                    flash ('Entered details already exists.')
                    return render_template('signin.html')
                else:
                    def db_query():
                        db = Database()
                        emps = db.insertdataownerdetails(firstname, lastname, phone, email, address, username, password)    
                        return emps
                res = db_query()
                flash ('Dear Customer, Your registration has been done successfully.')
                return render_template('index.html')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('signin.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('index.html')
    
    return render_template('index.html')

@app.route('/codeadddatacentre', methods=['POST'])
def codeadddatacentre():
    name = request.form['name']
    location = request.form['location']
    pincode = request.form['pincode']
    username = request.form['username']
    password = request.form['password']
  
    print('username:', username)
    print('password:', password)
    
    try:
        if name is not "" and location is not ""  and pincode is not "" and username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getcountofdatacentredetailsbyname(name)       
                return emps
            res = db_query()

            for row in res:
                print(row['c'])
                count = row['c']

                if count >= 1:      
                    flash ('Entered details already exists.')
                    return render_template('adddatacentre.html', sessionValue=session['x'])
                else:
                    def db_query():
                        db = Database()

                        latitude, longitude = FindLocation.getlatlongpositions(location, pincode)
                        
                        emps = db.insertdatacentredetails(name, location, pincode, latitude, longitude, username, password)    
                        return emps
                res = db_query()
                flash ('Dear Customer, Your registration has been done successfully.')
                return render_template('adddatacentre.html', sessionValue=session['x'])
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('adddatacentre.html', sessionValue=session['x'])
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('adddatacentre.html', sessionValue=session['x'])
    
    return render_template('adddatacentre.html', sessionValue=session['x'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/user', methods=['GET'])
def user():
    return render_template('user.html')

@app.route('/codeuser', methods=['POST'])
def codeuser():
    username = request.form['username']
    password = request.form['password']
    
    print('username:' + username)
    print('password:' + password)
    
    try:
        if username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getpersonaldetails(username, password)       
                return emps
            res = db_query()
            
            for row in res:
                print(row['c'])
                count = row['c']
                
                if count >= 1:      
                    session['x'] = username;
                    session['UID'] = row['PersonId'];
                    def db_query():
                        db = Database()
                        emps = db.getuserprofiledetails(username)       
                        return emps
                    profile_res = db_query()
                    return render_template('userprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')
                else:
                    flash ('Incorrect Username or Password.')
                    return render_template('user.html')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('user.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('user.html')
        
    return render_template('user.html')

@app.route('/usersignin', methods=['GET'])
def usersignin():
    return render_template('usersignin.html')

@app.route('/codeusersignin', methods=['POST'])
def codeusersignin():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']    
    username = request.form['username']
    password = request.form['password']
    
    print('firstname:', firstname)
    print('lastname:', lastname)
    print('phone:', phone)
    print('email:', email)
    print('address:', address)
    print('username:', username)
    print('password:', password)
    
    try:
        if firstname is not "" and lastname is not ""  and phone is not "" and email is not "" and address is not "" and username is not "" and password is not "": 
            def db_query():
                db = Database()
                emps = db.getpersonaldetails(username, password)       
                return emps
            res = db_query()

            for row in res:
                print(row['c'])
                count = row['c']

                if count >= 1:      
                    flash ('Entered details already exists.')
                    return render_template('usersignin.html')
                else:
                    def db_query():
                        db = Database()
                        emps = db.insertpersonaldetails(firstname, lastname, phone, email, address, username, password)    
                        return emps
                res = db_query()
                flash ('Dear Customer, Your registration has been done successfully.')
                return render_template('user.html')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('usersignin.html')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('usersignin.html')
    
    return render_template('usersignin.html')

@app.route('/userprofile', methods=['GET'])
def userprofile():
    def db_query():
        db = Database()
        emps = db.getuserpersonaldetails(session['x'])       
        return emps
    profile_res = db_query()
    return render_template('userprofile.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/searchknn', methods=['GET'])
def searchknn():
    return render_template('searchknn.html', sessionValue=session['x'], content_type='application/json')

@app.route('/codesearchknn', methods=['POST'])
def codesearchknn():
    amt = request.form['amt']
    
    print('amt:', amt)
       
    def db_query():
        db = Database()
        emps = db.getsearchdetails(amt);
        return emps
    profile_res = db_query()
    
    return render_template('viewresults.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/usergraph', methods=['GET'])
def usergraph():
    
    def accepteddb_query():
        db = Database()
        emps = db.getgraphdetails(session['x'])       
        return emps
    res = accepteddb_query()
    
    graph = pygal.Line()
    
    graph.title = '% Comparison Graph Between Fragmented and Unfragmented Data vs Number of Counts.'
    
    graph.x_labels = ['Horizontally', 'Vertically', 'Hybrid']
    
    for row in res:
        
        print(row['c'])
        
        graph.add(row['Class'], [row['c'], row['c'] + 200, row['c']  + 500])
        
    graph_data = graph.render_data_uri()
    
    return render_template('usergraph.html', sessionValue=session['x'], graph_data=graph_data)

@app.route('/viewusers', methods=['GET'])
def viewusers():
    def db_query():
        db = Database()
        emps = db.getuserdetails()       
        return emps
    profile_res = db_query()
    return render_template('viewusers.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route("/img/<int:imgId>")
def fetchImg(imgId):
    def db_query():
        db = Database()
        emps = db.getimagedetails(imgId)
        return emps

    profile_res = db_query()

    filename = ""

    for row in profile_res:
        filename = row["Image"]
        print(filename)

    from flask import send_from_directory

    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
    
@app.route('/viewproducts', methods=['GET'])
def viewproducts():
    def db_query():
        db = Database()
        emps = db.getproductdetails(session['UID'])       
        return emps
    profile_res = db_query()
    
    def db_query1(productId):
        db = Database()
        emps = db.getproducts(productId)       
        return emps
    
    def db_query2(sizes):
        db = Database()
        emps = db.getsizedetails(sizes)       
        return emps
    
    productList = [];
    
    for row in profile_res:
        sizes = row["Size_Id"]
        productId = row["Product_Id"]
        print(sizes)
        print(productId)
        
        list = [];
        list.append(db_query1(productId));      
        list.append(db_query2(sizes));
        
        productList.append(list);
        
    print(productList)
        
    return render_template('viewproducts.html', sessionValue=session['x'], result=productList, content_type='application/json')

@app.route('/vieworders', methods=['GET'])
def vieworders():
    def db_query():
        db = Database()
        emps = db.getorderdetails(session['UID'])       
        return emps
    order_res = db_query()
    
    def db_query1(orderId):
        db = Database()
        emps = db.getorders(orderId)       
        return emps
    
    def db_query2(sizes):
        db = Database()
        emps = db.getsizedetails(sizes)       
        return emps
    
    productList = [];
    
    for row in order_res:
        sizes = row["Size_Id"]
        orderId = row["OrderId"]
        print(sizes)
        print(orderId)
        
        list = [];
        list.append(db_query1(orderId));      
        list.append(db_query2(sizes));
        
        productList.append(list);
        
    print(productList)
        
    return render_template('vieworders.html', sessionValue=session['x'], result=productList, content_type='application/json')

@app.route('/viewconfig', methods=['GET'])
def viewconfig():
    def db_query():
        db = Database()
        emps = db.getconfigdetails(session['UID'])
        return emps
    profile_res = db_query()
    return render_template('viewconfig.html', sessionValue=session['x'], result=profile_res, content_type='application/json')

@app.route('/addconfig', methods=['GET'])
def addconfig():    
    def db_query():
        db = Database()
        emps = db.getallsizedetails()       
        return emps
    sizeresult = db_query()
    
    return render_template('addconfig.html', sessionValue=session['x'], result=sizeresult, content_type='application/json')

@app.route('/codeaddconfig', methods=['POST'])
def codeaddconfig():
    size = request.form['size']
    min = request.form['min']
    max = request.form['max']
  
    print('size:', size)
    print('min:', min)
    print('max:', max)
    
    def db_query3():
        db = Database()
        emps = db.getallsizedetails()       
        return emps
    sizeresult = db_query3()
    
    try:
        if size is not "" and min is not ""  and max is not "":
            
            category = size.split("-")
            
            def db_query1():
                db = Database()
                emps = db.getsizedetailsbythickness(category[0])       
                return emps
            res1 = db_query1()
            
            for row1 in res1:
                print(row1['CategoryId'])
                categoryId = row1['CategoryId']
            
            def db_query2():
                db = Database()
                emps = db.getsizedetailsbylength(category[0], category[1])       
                return emps
            res2 = db_query2()
            
            for row2 in res2:
                print(row2['Size_Id'])
                sizeId = row2['Size_Id']
            
            def db_query():
                db = Database()
                emps = db.getcountofconfigdetailsbyname(categoryId, sizeId)       
                return emps
            res = db_query()

            for row in res:
                print(row['c'])
                count = row['c']

                if count >= 1:      
                    flash ('Entered details already exists.')
                    return render_template('addconfig.html', sessionValue=session['x'], result=sizeresult)
                else:
                    def db_query():
                        db = Database()
                        emps = db.insertconfigdetails(session['UID'], categoryId, sizeId, min, max)    
                        return emps
                res = db_query()
                flash ('Dear Customer, Your registration has been done successfully.')
                return render_template('addconfig.html', sessionValue=session['x'], result=sizeresult)
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('addconfig.html', sessionValue=session['x'], result=sizeresult)
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('addconfig.html', sessionValue=session['x'], result=sizeresult)
    
    return render_template('addconfig.html', sessionValue=session['x'], result=sizeresult)

@app.route('/bookproducts', methods=['GET'])
def bookproducts():
    def db_query():
        db = Database()
        emps = db.getallproductdetails()       
        return emps
    profile_res = db_query()
    
    def db_query1(productId):
        db = Database()
        emps = db.getproducts(productId)       
        return emps
    
    def db_query2(sizes):
        db = Database()
        emps = db.getsizedetails(sizes)       
        return emps
    
    productList = [];
    
    for row in profile_res:
        sizes = row["Size_Id"]
        productId = row["Product_Id"]
        print(sizes)
        print(productId)
        
        list = [];
        list.append(db_query1(productId));      
        list.append(db_query2(sizes));
        
        productList.append(list);
        
    print(productList)
        
    return render_template('bookproducts.html', sessionValue=session['x'], result=productList, content_type='application/json')

@app.route('/trackorders', methods=['GET'])
def trackorders():
    def db_query():
        db = Database()
        emps = db.getuserorderdetails(session['UID'])       
        return emps
    order_res = db_query()
    
    def db_query1(orderId):
        db = Database()
        emps = db.getorders(orderId)       
        return emps
    
    def db_query2(sizes):
        db = Database()
        emps = db.getsizedetails(sizes)       
        return emps
    
    productList = [];
    
    for row in order_res:
        sizes = row["Size_Id"]
        orderId = row["OrderId"]
        print(sizes)
        print(orderId)
        
        list = [];
        list.append(db_query1(orderId));      
        list.append(db_query2(sizes));
        
        productList.append(list);
        
    print(productList)
        
    return render_template('trackorders.html', sessionValue=session['x'], result=productList, content_type='application/json')

@app.route('/buyProduct', methods=['GET'])
def buyProduct():
    parsed = urlparse.urlparse(request.url)
    print(parse_qs(parsed.query)['index'])
    productId = parse_qs(parsed.query)['index'][0]
    print(productId)
    userId = parse_qs(parsed.query)['index1'][0]
    print(userId)
    
    try:
        if productId is not "" and userId is not "": 
            
            def db_query1(productId):
                db = Database()
                emps = db.getproductsbyuserid(productId, userId)       
                return emps
            
            product_res = db_query1(productId)
            
            for row in product_res:
                sizes = row["Size_Id"]
                print(sizes)
    
            def db_query():
                db = Database()
                emps = db.getsizedetails(sizes)    
                return emps
            
            size_res = db_query()
            
            return render_template('viewavailablesize.html', sessionValue=session['x'], result=size_res, userId=userId, productId=productId, content_type='application/json')
        else:
            flash ('Please fill all mandatory fields.')
            return render_template('bookproducts.html', sessionValue=session['x'], result=size_res, productId=productId, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('bookproducts.html', sessionValue=session['x'], result=size_res, content_type='application/json')

@app.route('/codebookproducts', methods=['POST'])
def codebookproducts():
    data = request.form.getlist('data')
    quantity = request.form['quantity']
    productId = request.form['productId']
    userId = request.form['userId']
  
    print('data:', data)
    print('quantity:', quantity)
    print('productId:', productId)
    print('userId:', userId)
        
    def db_query1(productId, userId):
        db = Database()
        emps = db.getproductsbyuserid(productId, userId)       
        return emps

    product_res = db_query1(productId, userId)

    for row in product_res:
        sizes = row["Size_Id"]
        print(sizes)

    def db_query():
        db = Database()
        emps = db.getsizedetails(sizes)    
        return emps

    size_res = db_query()
            
    try:
        if len(data) > 0 and quantity is not "" and productId is not "" and userId is not "":
            
            for sizeId in data:
                print(sizeId)
                db = Database()
                db.insertorderdetails(session['UID'], userId, productId, sizeId, quantity)
            
            flash ('Dear Customer, Your order has been done successfully.')
            return redirect(url_for("bookproducts"))
        else:     
            flash ('Please fill all mandatory fields.')
            return render_template('viewavailablesize.html', sessionValue=session['x'], result=size_res)
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('viewavailablesize.html', sessionValue=session['x'], result=size_res)
    
    return render_template('viewavailablesize.html', sessionValue=session['x'], result=size_res)

@app.route('/addproducts', methods=['GET'])
def addproducts():    
    def db_query():
        db = Database()
        emps = db.getallsizedetails()       
        return emps
    sizeresult = db_query()
    
    return render_template('addproducts.html', sessionValue=session['x'], result=sizeresult, content_type='application/json')

@app.route('/codeaddproducts', methods=['POST'])
def codeaddproducts():
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    file = request.files['filepath']
    data = request.form.getlist('data')
  
    print('name:', name)
    print('description:', description)
    print('price:', price)
    print('filename:' + file.filename)
    print(data)
    
    def db_query():
        db = Database()
        emps = db.getallsizedetails()       
        return emps
    sizeresult = db_query()
    
    if 'filepath' not in request.files:
        flash ('Please fill all mandatory fields.')
        return render_template('addproducts.html', sessionValue=session['x'], result=sizeresult, content_type='application/json')
    
    try:
        if file.filename != '' and len(data) > 0 and name is not "" and description is not "" and price is not "":
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                filepath = UPLOAD_FOLDER + "/" + file.filename

                print('filepath:' + filepath)
                
                sizeIds = ''
            
                for s in data:
                    sizeIds += '' + s + '' + ','
                    print(s)

                sizeIds = sizeIds[: len(sizeIds) - 1]
                sizeIds += ''

                print(sizeIds)
                
                db = Database()
                db.insertproductdetails(session['UID'], name, description, price, filename, sizeIds);
                
                flash ('Dear Customer, Your product has been done successfully.')
                return render_template('addproducts.html', sessionValue=session['x'], result=sizeresult, content_type='application/json')
            else:
                flash ('Dear Customer, Your uploaded file is not supported.')
                return render_template('addproducts.html', sessionValue=session['x'], result=sizeresult, content_type='application/json')
        else:                        
            flash ('Please fill all mandatory fields.')
            return render_template('addproducts.html', sessionValue=session['x'], result=sizeresult, content_type='application/json')
    except NameError:
        flash ('Due to technical problem, your request could not be processed.')
        return render_template('addproducts.html', sessionValue=session['x'], result=sizeresult, content_type='application/json')
    
    return render_template('addproducts.html', sessionValue=session['x'], result=sizeresult, content_type='application/json')
