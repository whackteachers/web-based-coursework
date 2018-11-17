from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
	def home():
	return render_template('home.html')

#Set file reading and writing function	
def writeFile(aList,aFile):
    with open(aFile, 'w', newline='') as outFile: 
        write=csv.writer(outFile)
        write.writerows(aList)
	return
def readFile(aFile):
    with open(aFile, 'r') as inFile:
         reader = csv.reader(inFile) 
         detailList = [row for row in reader]
    return detailList
	
@app.route('/addDetails')
		def addDetails:
			checkIn=requet.form[('checkIn')]
			checkOut=requet.form[('checkOut')]
			title=requet.form[('title')]
			firstName=requet.form[('firstName')]
			adultsNumbers=requet.form[('adultsNumbers')]
			childrenNumbers=requet.form[('childrenNumbers')]
			email=requet.form[('email')]
			newDetail=[checkIn,checkOut,title,firstName,adultsNumbers,childrenNumbers,email]	
			fileName='static\\requestDetail.csv'
			detailList=readFile(fileName)
			detailList.append(newDetail)
			
			writeFile(detailList,fileName)
			return render_template('requesting.html',detailList =detailList)
if __name__ == '__main__':
 app.run(debug = True)
