# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "home"
__date__ = "$20 Dec, 2023 3:06:13 PM$"

import pymysql
import schedule
import time

class Database:
    def __init__(self):
        host = "localhost"
        user = "root"
        password = ""
        db = "productionplaning"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
    def getorderdetails(self):
        strQuery = "SELECT OrderId, PersonId, UserId, Product_Id, Size_Id, AES_DECRYPT(Quantity, 1234) AS Quantity, Production_Date, Updated_Date, Delivered, Delivered_Date, Recorded_Date FROM orderdetails WHERE Production_Date IS NULL ORDER BY Recorded_Date ASC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getorderdetailsbyproductid(self, productId, sizeId):
        strQuery = "SELECT OrderId, PersonId, UserId, Product_Id, Size_Id, AES_DECRYPT(Quantity, 1234) AS Quantity, Production_Date, Updated_Date, Delivered, Delivered_Date, Recorded_Date FROM orderdetails WHERE Production_Date IS NULL AND Product_Id = '"+str(productId)+"' AND Size_Id = '"+str(sizeId)+"' ORDER BY Quantity ASC"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def getconfigdetails(self, userId, sizeId):
        strQuery = "SELECT c.ConfigId, ca.Name, s.Standard_Sheet_Length, s.Overall_Profile_Width, s.Effective_Cover_Width, s.Minimum_Roof_Slope, c.Min_Quantity, c.Max_Quantity, c.Recorded_Date "
        strQuery += "FROM configdetails AS c ";
        strQuery += "LEFT JOIN categorydetails AS ca ON ca.CategoryId = c.CategoryId ";
        strQuery += "LEFT JOIN sizedetails AS s ON s.Size_Id = c.Size_Id ";
        strQuery += "LEFT JOIN dataownerdetails AS d ON d.UserId = c.UserId ";
        strQuery += "WHERE d.UserId = '" + str(userId) + "' "
        strQuery += "AND c.Size_Id = '" + str(sizeId) + "' "
        strQuery += "ORDER BY ConfigId DESC ";
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result
    def updateorderdetails(self, orderId, days):
        days=days
        print('orderId::' + str(orderId))
        print('days::' + str(days))
        strQuery = "UPDATE orderdetails SET Production_Date = CURDATE() + INTERVAL (%s) DAY, Updated_Date = CURDATE(), Delivered = 1, Delivered_Date = CURDATE() + INTERVAL (%s) DAY WHERE OrderId = (%s)"
        strQueryVal = (str(days), str(days + 1), str(orderId))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def updateorderdetailsbydate(self, orderId, maxProductionDate, days):
        days=days
        print('orderId::' + str(orderId))
        print('minProductionDate::' + str(maxProductionDate))
        print('days::' + str(days))
        strQuery = "UPDATE orderdetails SET Production_Date = (%s) + INTERVAL (%s) DAY, Updated_Date = CURDATE(), Delivered = 1, Delivered_Date = (%s) + INTERVAL (%s) DAY WHERE OrderId = (%s)"
        strQueryVal = (str(maxProductionDate), str(days), str(maxProductionDate), str(days + 1), str(orderId))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def updatetoomanyorderdetails(self, orderIds, maxProductionDate, days):
        days=days
        print('orderIds::' + str(orderIds))
        print('minProductionDate::' + str(maxProductionDate))
        print('days::' + str(days))
        strQuery = "UPDATE orderdetails SET Production_Date = (%s) + INTERVAL (%s) DAY, Updated_Date = CURDATE(), Delivered = 1, Delivered_Date = (%s) + INTERVAL (%s) DAY WHERE OrderId IN " + str(orderIds)
        strQueryVal = (str(maxProductionDate), str(days), str(maxProductionDate), str(days + 1))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def updatemanyorderdetails(self, orderIds, days):
        
        print('orderId::' + str(orderId))
        print('days::' + str(days))
        strQuery = "UPDATE orderdetails SET Production_Date = CURDATE() + INTERVAL (%s) DAY, Updated_Date = CURDATE(), Delivered = 1, Delivered_Date = CURDATE() + INTERVAL (%s) DAY WHERE OrderId IN " + str(orderIds)
        strQueryVal = (str(days), str(days + 1))
        self.cur.execute(strQuery, strQueryVal)
        self.con.commit()
        return ""
    def getmaxorderdetails(self):
        strQuery = "SELECT Production_Date FROM orderdetails WHERE Production_Date IS NOT NULL ORDER BY Recorded_Date DESC LIMIT 1"
        self.cur.execute(strQuery)
        result = self.cur.fetchall()
        print(result)
        return result

def job():
    print("...Scheduler Starts...")
    
    def db_query():
        db = Database()
        emps = db.getorderdetails()       
        return emps
    res = db_query()
    
    def db_query1(userId, sizeId):
        db = Database()
        emps = db.getconfigdetails(userId, sizeId)       
        return emps
    
    def db_query2():
        db = Database()
        emps = db.getmaxorderdetails()       
        return emps
    
    def db_query3(productId, sizeId):
        db = Database()
        emps = db.getorderdetailsbyproductid(productId, sizeId)       
        return emps
    
    for row in res:
        orderId = row['OrderId']
        userId = row['UserId']
        sizeId = row['Size_Id']
        totalQuantity = row['Quantity']
        productId = row['Product_Id']
        print(orderId)
        print(userId)
        print(sizeId)
        print(totalQuantity)
        print(productId)
        
        maxProductionDate = "";
        config_res = db_query1(userId, sizeId)
        
        for row1 in config_res:
            minQuantity = row1['Min_Quantity']
            maxQuantity = row1['Max_Quantity']
            print(minQuantity)
            print(maxQuantity)
            
            if int(totalQuantity) > maxQuantity: 
                days = int(totalQuantity) / maxQuantity;
                max_res = db_query2()
                
                days=days
                for row2 in max_res:
                    maxProductionDate = row2['Production_Date']
                    
                if maxProductionDate is not "": 
                    db = Database()
                    db.updateorderdetailsbydate(orderId, maxProductionDate, days)
                else:
                    db = Database()
                    db.updateorderdetails(orderId, days)
                    
                print("UPDATED")
            elif int(totalQuantity) >= minQuantity and int(totalQuantity) <= maxQuantity: 
                days = 1;
                max_res = db_query2()
                
                for row5 in max_res:
                    maxProductionDate = row5['Production_Date']

                if maxProductionDate is not "": 
                    db = Database()
                    db.updateorderdetailsbydate(orderId, maxProductionDate, days)
                else:
                    db = Database()
                    db.updateorderdetails(orderId, days)
                print("UPDATED")
            else:
                orderIds = '('
                count = 0;
                product_res = db_query3(productId, sizeId);
                
                for row3 in product_res:
                    ordersimId = row3['OrderId']
                    quantity = row3['Quantity']
                    
                    count += int(quantity);
                        
                    if count <= maxQuantity: 
                        orderIds += '' + str(ordersimId) + '' + ','

                orderIds = orderIds[: len(orderIds) - 1]
                orderIds += ')'
            
                print(orderIds)
                
                if orderIds is not ")":
                    days = 1;
                    max_res = db_query2()

                    for row4 in max_res:
                        maxProductionDate = row4['Production_Date']

                    if maxProductionDate is not "": 
                        db = Database()
                        db.updatetoomanyorderdetails(orderIds, maxProductionDate, days)
                    else:
                        db = Database()
                        db.updatemanyorderdetails(orderIds, days)
                        
                print("UPDATED")
        
    print("...Scheduler Ends...")

schedule.every(1).minutes.do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)