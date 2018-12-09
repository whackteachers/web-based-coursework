import csv
import ctypes
from flask import Flask, render_template
from flask import request
from ctypes import *
from datetime import datetime

app = Flask(__name__)
#----Global variables----
#base price of property
price = 71
#buffer list to store booking details before actually writing to csv files
tempBookings = []
pricing = []
#file name variable for all functions
reviewFile='static\\reviews.csv'
simFile='static\\simDetail.csv'
requestFile='static\\requestDetail.csv'
#----Global variables----

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
	#round off the price to 2 decimal place to avoid long number
	return round(price* applyRates,2)
	
#open homepage
@app.route('/')
def home():
	detailList= readFile(reviewFile)
	for line in detailList:
		line[1]= int(line[1])
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
	 
def reset():
	if tempBookings:
		del tempBookings[:]
		del pricing[:]
	return
#turn to rental page and display rental details
@app.route('/rentalDetail', methods = ['GET'])
def rentalDetail():
	simList= readFile(simFile)
	#clear the temporary lists
	reset()
	return render_template('request.html', simList=simList, tempBookings=tempBookings)

#turn to local attactions page
@app.route('/attractions', methods = ['GET'])
def attractions():
	return render_template('attractions.html')

@app.route('/backToRequest', methods= ['POST','GET'])
def backToRequest():
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
	
	allBookings=readFile(requestFile)
	#check if all the details apart from email and phone number are the same
	for line in allBookings:
		if(all(line[i]==tempBookings[i] for i in range(6))):
			#prompt message to remind the user of double booking
			dbMessage = "Double Booking: You have already made this booking!"
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
	detailList=readFile(requestFile)
	detailList.append(newDetail)
	writeFile(detailList,requestFile)
	#write information without personal details into another csv file
	simList=readFile(simFile)
	simList.append(simDetail)
	writeFile(simList,simFile)
	#clear the temporary lists
	reset()
	#alert that the information has been submitted
	Message = "Your request has been sent to the admin, please check your email later!"
	#send information without personal details to html
	simList= readFile(simFile)
	
	return render_template('request.html',simList=simList,Message=Message, tempBookings=tempBookings)

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
	detailList=readFile(reviewFile)
	detailList.append(newReview)
	writeFile(detailList,reviewFile)
	#send reviws to html
	detailList= readFile(reviewFile)
	for line in detailList:
		line[1]= int(line[1])
	
	return render_template('home.html',detailList=detailList)

	
	#admin login fuction
@app.route('/adminLogin', methods= ['POST','GET'])
def adminLogin():
	username=request.form['username']
	password=request.form['password']
	#check if username and password are both correct
	if (username=='admin'and password=='123456'):
		requestList= readFile(requestFile)
		return render_template('adminPage.html',requestList=requestList)
		
	else:
		message='Username or password is not correct!Try again'
		return render_template('loginPage.html',message=message)
	
	#turn to admin login page
@app.route('/loginPage', methods = ['GET'])
def loginPage():
	return render_template('loginPage.html')
	
#turn to admin page and display request details
@app.route('/adminPage', methods = ['POST','GET'])
def adminPage():
	requestList = readFile(requestFile)
	return render_template('adminPage.html',requestList=requestList)
@app.route('/confirmBookings', methods = ['POST','GET'])
def	confirmBookings():
	#get the index of booking that needs confirmBookings
	indexes = request.form.getlist('bkLine')
	#convert result from string to int 
	indexes = list(map(int, indexes))
	#update the respective booking line status in both simplified and full booking detail files
	updateStatus(requestFile,indexes)
	updateStatus(simFile,indexes)
	
	#get the updated version of booking details
	updateList= readFile(requestFile)
	success_message = "You have successfully confirmed " + str(len(indexes)) + " booking(s)!"
	return render_template('adminPage.html',requestList=updateList,success_message=success_message)

def updateStatus(fp, select):
	#buffer out all contents
	oldList=readFile(fp)
	#clear all the content in csv
	open(fp,'w').truncate()
	#edit the respective row booking status to confirmed if selected
	for idx,line in enumerate(oldList):
		if (idx in select):
			line[len(line)-1] = 'confirmed'

	#write the updated list back to csv
	writeFile(oldList,fp)
	return select

if __name__ == '__main__':
 app.run(debug = True)
