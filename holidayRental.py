import csv
from flask import Flask, render_template
from flask import request
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
	 
	 
@app.route('/addDetails')
def addDetails():
	checkIn=request.form[('checkIn')]
	checkOut=request.form[('checkOut')]
	title=request.form[('title')]
	firstName=request.form[('firstName')]
	adultsNumbers=request.form[('adultsNumbers')]
	childrenNumbers=request.form[('childrenNumbers')]
	email=request.form[('email')]
	newDetail=[checkIn,checkOut,title,firstName,adultsNumbers,childrenNumbers,email]	
	fileName='static\\requestDetail.csv'
	detailList=readFile(fileName)
	detailList.append(newDetail)
			
	writeFile(detailList,fileName)
	return render_template('requesting.html',detailList =detailList)
	
	
if __name__ == '__main__':
 app.run(debug = True)
