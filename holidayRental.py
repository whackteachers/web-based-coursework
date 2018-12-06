import csv
import ctypes
from flask import Flask, render_template
from flask import request
from ctypes import *
from datetime import datetime

app = Flask(__name__)

enterTime = datetime.now().month
#respective periods for rates:
#(previous year)december-january, Feburary, March-April, May-June, July-August, September-November
rates = [1.25,1,1.15,1,1.3,0.9]
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
#open homepage
@app.route('/')
def home(): 
	reviewFile='static\\reviews.csv'
	detailList= readFile(reviewFile)
	return render_template('home.html',detailList=detailList,displayPrice=price)

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
    
    return render_template('request.html', simList=simList, price=price, price_rates=rates)

#turn to attactions page
@app.route('/attractions', methods = ['GET'])
def attractions():
	return render_template('attractions.html')

	
#botton to submit detail 
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
    
    newDetail=[checkIn,checkOut,title,firstName,adultsNumbers,childrenNumbers,email,phoneNo,confirmation]	
    simDetail=[checkIn,checkOut,confirmation]
    #write information into csv file
    fileName='static\\requestDetail.csv'
    detailList=readFile(fileName)
    detailList.append(newDetail)
    writeFile(detailList,fileName)
	#write information without personal details into another csv file
    simFile='static\\simDetail.csv'
    simList=readFile(simFile)
    simList.append(simDetail)
    writeFile(simList,simFile)
    #alert that the information has been submitted
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, 'Your request has been sent to the admin, please check your email later!', 'Nearly finish', 0)
    #send information without personal details to html
    requestFile='static\\simDetail.csv'
    simList= readFile(requestFile)
    
    return render_template('request.html',simList=simList, price=priceAfter)

	#function for reviews submit bottpn
@app.route('/addReviews', methods= ['POST','GET'])
def addReviews():
	reviewerName=request.form[('reviewerName')]
	review=request.form[('review')]
	stars=request.form[('stars')]
	title=request.form[('title')]
	currentTime=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
	currentTime+='posted on '
	newReview=[reviewerName,stars,title,review,currentTime]
	#write reviews into csv file
	fileName='static\\reviews.csv'
	detailList=readFile(fileName)
	detailList.append(newReview)
	writeFile(detailList,fileName)
	#send reviws to html 
	reviewFile='static\\reviews.csv'
	detailList= readFile(reviewFile)
	
	return render_template('home.html',detailList=detailList)

	
	#admin login fuction
@app.route('/adminLogin', methods= ['POST','GET'])
def adminLogin():
	username=request.form['username']
	password=request.form['password']
	#check if username and password are both correct
	if (username=='admin'and password=='123456'):
		return render_template('adminPage.html')
		
	else:
		message='Username or password is not correct!Try again'
		return render_template('loginPage.html',message=message)
	
	#turn to admin login page
@app.route('/loginPage', methods = ['GET'])
def loginPage():
	return render_template('loginPage.html')
	
	#turn to admin page and display request details
@app.route('/adminPage', methods = ['GET'])
def adminPage():
	requestFile='static\\requestDetail.csv'
	requestList= readFile(requestFile)
	return render_template('adminPage.html',requestList=requestList)
if __name__ == '__main__':
 app.run(debug = True)
