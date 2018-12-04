import csv
import ctypes
from flask import Flask, render_template
from flask import request
from ctypes import *
from datetime import datetime

app = Flask(__name__)

enterTime = datetime.now().month
rates = [1.25,1.15,1.3,0.9]
price = 71
if (enterTime in (12,1)):
	applyRates = rates[0]
elif (enterTime in (3,4)):
	applyRates = rates[1]
elif (enterTime in (7,8)):
	applyRates = rates[2]
elif (enterTime in (9,10,11)):
	applyRates = rates[3]
priceAfter = round(71* applyRates,2)

@app.route('/')
def home(): 
	reviewFile='static\\reviews.csv'
	detailList= readFile(reviewFile)
	return render_template('home.html',detailList=detailList,displayPrice=priceAfter)

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
    requestFile='static\\simDetail.csv'
    simList= readFile(requestFile)
    
    return render_template('request.html', simList=simList	, price=priceAfter)
    
@app.route('/attractions', methods = ['GET'])
def attractions():
	return render_template('attractions.html')
	
@app.route('/addDetails', methods= ['POST','GET'])
def addDetails():
    checkIn=request.form['checkIn']
    checkOut=request.form['checkOut']
    title=request.form['title']
    firstName=request.form['firstName']
    adultsNumbers=request.form['adultsNumbers']
    childrenNumbers=request.form['childrenNumbers']
    email=request.form['email']
    phoneNo=request.form['phoneNo']
    confirmation='unconfirmed'
    
    # checkInDate = datetime.strptime(CheckIn, '%d/%m/%Y')
    # checkOutDate = datetime.strptime(CheckOut, '%d/%m/%Y')
    
    newDetail=[checkIn,checkOut,title,firstName,adultsNumbers,childrenNumbers,email,phoneNo,confirmation]	
    simDetail=[checkIn,checkOut,confirmation]
    
    fileName='static\\requestDetail.csv'
    detailList=readFile(fileName)
    detailList.append(newDetail)
    writeFile(detailList,fileName)
	
    simFile='static\\simDetail.csv'
    simList=readFile(simFile)
    simList.append(simDetail)
    writeFile(simList,simFile)
    
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, 'Your request has been sent to the admin, please check your email later!', 'Nearly finish', 0)
    
    requestFile='static\\simDetail.csv'
    simList= readFile(requestFile)
    # checkInTime=[row[0]for row in detailList]
    # checkOutTime=[row[1]for row in detailList]
    # confirmation=[row[7]for row in detailList]
    #calculate the total price
    # d1 = datetime(checkInDate, "%d/%m/%Y")
    # d2 = datetime(checkOutDate, "%d/%m/%Y")
    # totalPrice=(abs((d2 - d1).days))*priceAfter
    return render_template('request.html',simList=simList, price=priceAfter)

@app.route('/addReviews', methods= ['POST','GET'])
def addReviews():
	reviewerName=request.form[('reviewerName')]
	review=request.form[('review')]
	stars=request.form[('stars')]
	title=request.form[('title')]
	currentTime=datetime.now().strftime('%d-%m-%Y %H:%M:%S')
	newReview=[reviewerName,stars,title,review,currentTime]
	
	fileName='static\\reviews.csv'
	detailList=readFile(fileName)
	detailList.append(newReview)
	writeFile(detailList,fileName)
	
	reviewFile='static\\reviews.csv'
	detailList= readFile(reviewFile)
	
	return render_template('home.html',detailList=detailList)
    
	
if __name__ == '__main__':
 app.run(debug = True)
