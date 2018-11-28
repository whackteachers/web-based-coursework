import csv
import ctypes
from flask import Flask, render_template
from flask import request
from ctypes import *
from datetime import datetime

app = Flask(__name__)
@app.route('/')
def home(): 
    return render_template('home.html')

#Set file reading and writing function	

def readFile(aFile):
    with open(aFile, 'r') as inFile:
         reader = csv.reader(inFile) 
         detailList = [row for row in reader]
    return detailList
	
def writeFile(aList,aFile):
     with open(aFile, 'w', newline='') as outFile: 
        write=csv.writer(outFile)
        write.writerows(aList)
     return	
	 
	 
#turn to rental page and display rental details
@app.route('/rentalDetail', methods = ['GET'])
def rentalDetail():
    requestFile='static\\requestDetail.csv'
    detailList= readFile(requestFile)
    checkInTime=[row[0]for row in detailList]
    checkOutTime=[row[1]for row in detailList]
    confirmation=[row[7]for row in detailList]
    return render_template('request.html', checkInTime=checkInTime,checkOutTime=checkOutTime,confirmation=confirmation)
    
@app.route('/attractions', methods = ['GET'])
def attractions():
	return render_template('attractions.html')
	
@app.route('/addDetails', methods= ['POST','GET'])
def addDetails():
    checkIn=request.form[('checkIn')]
    checkOut=request.form[('checkOut')]
    title=request.form[('title')]
    firstName=request.form[('firstName')]
    adultsNumbers=request.form[('adultsNumbers')]
    childrenNumbers=request.form[('childrenNumbers')]
    email=request.form[('email')]
    confirmation='unconfirmed'
    newDetail=[checkIn,checkOut,title,firstName,adultsNumbers,childrenNumbers,email,confirmation]	
    fileName='static\\requestDetail.csv'
    detailList=readFile(fileName)
    detailList.append(newDetail)
    writeFile(detailList,fileName)
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, 'Your request has been sent to the admin, please check your email later!', 'Nearly finish', 0)
    requestFile='static\\requestDetail.csv'
    detailList= readFile(requestFile)
    checkInTime=[row[0]for row in detailList]
    checkOutTime=[row[1]for row in detailList]
    confirmation=[row[7]for row in detailList]
    #calculate the total price  
    d1 = datetime.strptime(CheckIn, "%d/%m/%Y")
    d2 = datetime.strptime(CheckOut, "%d/%m/%Y")
    totalPrice=(abs((d2 - d1).days))*71
    return render_template('request.html',checkInTime=checkInTime,checkOutTime=checkOutTime,confirmation=confirmation,totalPrice=totalPrice)


    
    
    
	
if __name__ == '__main__':
 app.run(debug = True)
