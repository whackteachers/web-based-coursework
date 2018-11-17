import csv
from flask import Flask, render_template
from flask import request
app = Flask(__name__)
def readFile(aFile):
    with open(aFile, 'r') as inFile:
         reader = csv.reader(inFile) 
         skillList = [row for row in reader]
    return skillList
def writeFile(aList,aFile):
    with open(aFile, 'w', newline='') as outFile: 
        write=csv.writer(outFile)
        write.writerows(aList)
    return
@app.route('/')
def home(): 
    return render_template('home.html')


@app.route('/skills', methods = ['GET'])
def skills():
    skillFile='static\\skills.csv'
    skillList= readFile(skillFile)
    return render_template('skills.html', skillList=skillList)

@app.route('/addSkill',methods= ['POST'])
def addSkill():
    skillName= request.form[('skillName')]
    rating= request.form[('rating')]
    newSkill=[skillName,rating]
    skillFile='static\\skills.csv'
    skillList= readFile(skillFile)
    skillList.append(newSkill)
    
    writeFile(skillList,skillFile)
    
    return render_template('skills.html', skillList=skillList)
    
    
    

    


    
if __name__ == '__main__':
    app.run(debug = True)
