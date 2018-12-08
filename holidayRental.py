import csv
import ctypes
from flask import Flask, render_template
from flask import request
from ctypes import *
from datetime import datetime

app = Flask(__name__)

enterTime = datetime.now().month
price = 71
tempBookings = []
pricing = []
reviewFile='static\\reviews.csv'
simFile='static\\simDetail.csv'
requestFile='static\\requestDetail.csv'

#respective rates for different months:
#(previous year)december-january, Feburary, March-April, May-June, July-August, September-November
def processPrice(month):
	rates = [1.25,1,1.15,1,1.3,0.9]
	if (month in (12,1)):
		applyRates = rates[0]
	elif (month in (2)):
		applyRates = rates[1]
	elif (month in (3,4)):
		applyRates = rates[2]
	elif (month in (5,6)):
		applyRates = rates[3]
	elif (month in (7,8)):
		applyRates = rates[4]
	elif (month in (9,10,11)):
		applyRates = rates[5]
	
	return round(price* applyRates,2)
	
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
	simFile='static\\simDetail.csv'
	simList= readFile(simFile)
	if not tempBookings:
		tempBookings.clear()
		pricing.clear()
	return render_template('request.html', simList=simList, tempBookings=tempBookings)

#turn to local attactions page
@app.route('/attractions', methods = ['GET'])
def attractions():
	return render_template('attractions.html')

@app.route('/backToRequest', methods= ['POST','GET'])
def backToRequest():
	simFile='static\\simDetail.csv'
	simList= readFile(simFile)
	return render_template('request.html', simList=simList, tempBookings=tempBookings)

@app.route('/bookingSummary', methods= ['POST','GET'])
def bookingSummary():
	#extract all input values in request.html
	checkIn=request.form['checkIn']
	checkOut=request.form['checkOut']
	title=request.form['title']
	firstName=request.form['firstName']
	adultsNumbers=request.form['adultsNumbers']
	childrenNumbers=request.form['childrenNumbers']
	email=request.form['email']
	phoneNo=request.form['phoneNo']
	confirmation='unconfirmed'
	#gather all the details 
	tempDetails = [checkIn,checkOut,title,firstName,adultsNumbers,childrenNumbers,email,phoneNo,confirmation]
	tempBookings.extend(tempDetails)
	
	requestFile='static\\requestDetail.csv'
	allBookings=readFile(requestFile)
	#check if all the details apart from email and phone number are the same
	for line in allBookings:
		if(line[:6]==tempBookings[:6]):
			#prompt message to remind the user of double booking
			dbMessage = "Double Booking: You have already made this booking!"
			simFile='static\\simDetail.csv'
			simList=readFile(simFile)
			return render_template('request.html', simList=simList, Message=dbMessage, tempBookings=tempBookings)
	#calculate the staying time and total price 
	d1 = datetime.strptime(checkIn, "%d/%m/%Y")
	d2 = datetime.strptime(checkOut, "%d/%m/%Y")
	nightPrice = processPrice(d1.month)
	stay = (d2 - d1).days
	totalPrice = stay*nightPrice
	
	#gather all the price information
	tempPricing = [nightPrice, stay, totalPrice]
	pricing.extend(tempPricing)
	return render_template('bookingSummary.html', tempDetails=tempDetails, pricing=pricing)
	
#botton to submit detail 
@app.route('/addDetails', methods= ['POST','GET'])
def addDetails():
	#copy the tempDetails into new a booking detail
	newDetail=tempBookings
	simDetail=[newDetail[0],newDetail[1],newDetail[len(newDetail)-1]]
	#write information into csv file
	requestFile='static\\requestDetail.csv'
	detailList=readFile(requestFile)
	detailList.append(newDetail)
	writeFile(detailList,requestFile)
	#write information without personal details into another csv file
	simFile='static\\simDetail.csv'
	simList=readFile(simFile)
	simList.append(simDetail)
	writeFile(simList,simFile)
	#alert that the information has been submitted
	MessageBox = ctypes.windll.user32.MessageBoxW
	MessageBox(None, 'Your request has been sent to the admin, please check your email later!', 'Nearly finish', 0)
	#send information without personal details to html
	simList= readFile(simFile)
	
	return render_template('request.html',simList=simList,)

#function for reviews submit bottpn
@app.route('/addReviews', methods= ['POST','GET'])
def addReviews():
	reviewerName=request.form[('reviewerName')]
	review=request.form[('review')]
	stars=request.form[('stars')]
	title=request.form[('title')]
	currentTime=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
	newReview=[reviewerName,stars,title,review,currentTime]
	#write reviews into csv file
	reviewFile='static\\reviews.csv'
	detailList=readFile(reviewFile)
	detailList.append(newReview)
	writeFile(detailList,reviewFile)
	#send reviws to html
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
