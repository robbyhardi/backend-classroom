from flask import Flask, request, json, jsonify
import os

app = Flask(__name__)

#=====================function====================================================================================
def readFile(filePath):
    thisData = []
    #kalau file *.json udah ada, di read. kalau file ga ada, return list kosong
    if os.path.exists(filePath):
        thisFile = open(filePath, 'r')
        thisData = json.load(thisFile)
        thisFile.close()

    return thisData

def writeFile(filePath, data):
    thisFile = open(filePath, 'w')
    thisFile.write(json.dumps(data))
    thisFile.close()

#=================================================================================================================
@app.route('/')
def testConnection():
    return "connected"

@app.route('/register', methods=["POST"])
def register():
    body = request.json
    userData = readFile('./users-file.json')
      
    for user in userData:
        if body["username"] in user["username"]:
            return "Username sudah ada, ganti username!"
    
    userData.append(body)
    
    #siapin file buat di write
    userFile = writeFile('./users-file.json', userData)

    return jsonify(body)

@app.route('/login', methods=["POST"]) #login
def login():
    body = request.json

    #siapin file buatt di read
    userData = readFile('./users-file.json')

    for user in userData:

        if body["username"] == user["username"]:
            if body["password"] == user["password"]:
                return "Login Success"
            else:
                return "Login Fail. Wrong Password"
        else:
            pass
    return "Username not found" 

@app.route('/user', methods=["GET"]) #get all user
def getUser():
    #siapin file buat di read
    userData = readFile('./users-file.json')

    return jsonify(userData)

@app.route('/user/<int:id>', methods=["GET"]) #get 1 user
def getUserId(id):
    #siapin file buat di read
    userData = readFile('./users-file.json')

    for user in userData:
        if id == user["userid"]:
            return jsonify(user)
        else:
            pass
    return "User not found"

@app.route('/updateUser/<int:id>', methods=["PUT"]) #update 1 user
def updateUserId(id):
    usersData = getUser().json
    body = request.json

    for user in usersData:
        if id == user["userid"]:
            user["email"] = body["email"]
            user["fullname"] = body["fullname"]
            user["password"] = body["password"]
    
    #update ke file users
    userFile = writeFile('./users-file.json', usersData)
  
    return "Update Success"

@app.route('/outclass/<int:id>', methods=["POST"]) #outclass 1 user
def outClass(id):
    body = request.json

    #kurangin userid ke classes-file
    classesData = readFile('./classes-file.json')

    #kurangin classid ke users-file
    usersData = readFile('./users-file.json')

    for class_ in classesData:
        if id == class_["classid"]:
            for user in usersData:
                if body["userid"] in class_["students"]:
                    class_["students"].remove(body["userid"])
                    break
    
    classesFile = writeFile('./classes-file.json', classesData)

    for user in usersData: 
        if body["userid"] == user["userid"]:
            if id in user["classes_as_student"]:
                user["classes_as_student"].remove(id)

    usersFile = writeFile('./users-file.json', usersData)

    return "Success"

@app.route('/classlist', methods=["GET"]) #get all class
def classList():
    classData = readFile('./classes-file.json')
    
    return jsonify(classData)

@app.route('/class/create', methods=["POST"]) #create class
def createClass():
    #baca file classes
    classData = readFile('./classes-file.json')

    body = request.json
    body["students"] = []
    body["classwork"] = []

    #tambah ke file classes 
    classData.append(body)

    classFile = writeFile('./classes-file.json', classData)

    #baca file users
    usersData = readFile('./users-file.json')

    #tambah classid ke file users
    usersFile = writeFile('./users-file.json', usersData)

    return jsonify(body)
    
@app.route('/class/<int:id>', methods=["GET"]) #get 1 class
def getClassId(id):
    #siapin file classes buat di read
    classData = readFile('./classes-file.json')

    #siapin file users buat di read
    userData = readFile('./users-file.json')

    for classX in classData:
        if id == classX["classid"]:
            classX["students"] = []
            for user in userData:
                if id in user["classes_as_student"]:
                    classX["students"].append(user["fullname"])
            return jsonify(classX) 
    return "Class not found"
 
@app.route('/updateClass/<int:id>', methods=["PUT"]) #update 1 class
def updateClassId(id):
    classesData = classList().json
    body = request.json

    for class_ in classesData:
        if id == class_["classid"]:
            class_["classname"] = body["classname"]
            class_["teachers"] = body["teachers"]
            class_["students"] = body["students"]
            class_["classwork"] = body["classwork"]
    
    #update ke file class
    classesFile = writeFile('./classes-file.json', classesData)
  
    return "Update Success"

@app.route('/deleteClass/<int:id>', methods=['DELETE']) #delete 1 class
def deleteClass(id):
    #read data class
    classesData = classList().json

    for class_ in range(len(classesData)):
        if id == classesData[class_]["classid"]:
            del classesData[class_]
            break
        return "Error. Kelas sudah tidak ada!"
    
    #write data class
    classesFile = writeFile('./classes-file.json', classesData)
    
    #read data classwork
    classesWorkData = getClassWork().json

    for classWork in range(len(classesWorkData)):
        if id == classesWorkData[classWork]["class"]:
            del classesWorkData[classWork]
            break

    #write data classWork
    classesWorkFile = writeFile('./classwork-file.json', classesWorkData)

    #read data user
    usersData = getUser().json

    for user in usersData:
        if id in user["classes_as_student"]:
            user["classes_as_student"].remove(id)
            break

    #write data users
    usersFile = writeFile('./users-file.json', usersData)

    return "Kelas Berhasil Dihapus!"

@app.route('/classwork/create', methods=["POST"]) #create classwork
def createClassWork():
    body = request.json

    classWorkData = readFile('./classwork-file.json')
    
    classWorkData.append(body)

    classWorkFile = writeFile('./classwork-file.json', classWorkData)

    #read data
    classesData = classList().json

    for class_ in classesData:
        if class_["classid"] == body["class"]:
            class_["classwork"].append(body["workid"])

    #write data
    classesFile = writeFile('./classes-file.json', classesData)

    return jsonify(body)

@app.route('/classworklist', methods=["GET"]) #get all classwork
def getClassWork():
    #siapin file buat di read
    classWorkData = readFile('./classwork-file.json')
    
    return jsonify(classWorkData)

@app.route('/classwork/<int:id>', methods=["GET"]) #get 1 classwork
def getClassWorkId(id):
    #siapin file buat di read
    classWorkData = readFile('./classwork-file.json')

    for classwork in classWorkData:
        if id == classwork["workid"]:
            return jsonify(classwork) 
        else:
            pass
    return "Class not found"

@app.route('/classwork/assign/<int:id>', methods=["POST"]) #assign classwork
def assignClassWork(id):
    body = request.json

    #siapin data classwork
    classWorkData = getClassWork().json

    #siapin data user
    usersData = getUser().json

    for classwork in classWorkData:
        if id == classwork["workid"]:
            for user in usersData:
                if body["userid"] == user["userid"]:
                    classwork["answer"].append(body)
     
    classWorkFile = writeFile('./classwork-file.json', classWorkData)

    return jsonify(body)

@app.route('/classwork/update/<int:id>', methods=["POST"]) #update classork
def updateClassWork(id):
    body = request.json

    #read data classwork
    classesWorkData = getClassWork().json

    for classWork in classesWorkData:
        if id == classWork["workid"]:
            classWork["question"] = body["question"]

    #write data classwork
    classesWorkFile = writeFile('./classwork-file.json', classesWorkData)

    return "Update question success!"

@app.route('/classwork/delete/<int:id>', methods=["DELETE"]) #delete 1 classwork
def deleteClassWork(id):
    #read-write data classwork
    classesWorkData = getClassWorkId(id).json
    
    del classesWorkData

    #write data classwork
    classesWorkFile = writeFile('./classwork-file.json', classesWorkData)

    #read data class
    classesData = classList().json

    for class_ in classesData:
        if id in class_["classwork"]:
            class_["classwork"].remove(id)
            break

    #write data class
    classesFile = writeFile('./classes-file.json', classesData)

    return "Classwork Berhasil Dihapus!"


@app.route('/joinClass', methods=["POST"]) #join class student
def joinClass():
    body = request.json

    #nambahin userid ke classes-file
    classesData = readFile('./classes-file.json')

    for class_ in classesData:
        if body["classid"] == class_["classid"]:
            if (body["userid"] not in class_["students"]) and (body["userid"] not in class_["teachers"]):
                class_["students"].append(body["userid"])
    
    classesFile = writeFile('./classes-file.json', classesData)

    #nambahin classid ke users-file
    usersData = readFile('./users-file.json')
    
    for user in usersData: 
        if body["userid"] == user["userid"]:
            if (body["classid"] not in user["classes_as_student"]) and (body["classid"] not in user["classes_as_teacher"]):
                user["classes_as_student"].append(body["classid"])
    
    usersFile = writeFile('./users-file.json', usersData)

    return "Success"

@app.route('/joinClassTeacher', methods=["POST"]) #join class teacher
def joinClassTeacher():
    body = request.json

    #nambahin userid ke classes-file
    classesData = readFile('./classes-file.json')

    for class_ in classesData:
        if body["classid"] == class_["classid"]:
            if (body["userid"] not in class_["teachers"]) and (body["userid"] not in class_["students"]):
                class_["teachers"].append(body["userid"])
            else:
                return "Join failed! Anda sudah terdaftar!"
    
    classesFile = writeFile('./classes-file.json', classesData)

    #nambahin classid ke users-file
    usersData = readFile('./users-file.json')
    
    for user in usersData: 
        if body["userid"] == user["userid"]:
            if (body["classid"] not in user["classes_as_student"]) and (body["classid"] not in user["classes_as_teacher"]):
                user["classes_as_teacher"].append(body["classid"])
            else:
                return "Join failed! Anda sudah terdaftar!"
    
    usersFile = writeFile('./users-file.json', usersData)

    return "Success"

@app.errorhandler(404)
def error404(e):
    messages = {
        "statusCode": 404,
        "message": "URL ga ketemu"
    }
    return jsonify(messages)