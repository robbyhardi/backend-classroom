from flask import Flask, request, json, jsonify

from src.utils.crypt import encrypt, decrypt
from src.utils.file import readFile, writeFile
from src.utils.authorization import encode, decode

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#============================================variable=============================================================
usersFileLocation = 'src/data/users-file.json'
classesFileLocation = 'src/data/classes-file.json'
classesWorkFileLocation = 'src/data/classwork-file.json'

#=================================================================================================================
@app.route('/')
def testConnection():
    return "connected"

@app.route('/register', methods=["POST"])
def register():
    response = {}
    response["message"] = "Username sudah ada, ganti username"
    response["data"] = []

    body = request.json
    userData = readFile(usersFileLocation)
      
    for user in userData:
        if body["username"] in user["username"]:
            return jsonify(response)
        else:
            pass
    
    body["password"] = encrypt(3, body["password"])
    
    response["message"] = "Registration successfully"
    response["data"] = body
    
    userData.append(body)
    
    #siapin file buat di write
    writeFile(usersFileLocation, userData)

    return jsonify(response)

@app.route('/login', methods=["POST"]) #login
def login():
    response = {}
    response["message"] = "Login failed. Username or password is wrong"
    response["data"] = []

    body = request.json

    #siapin file buatt di read
    userData = readFile(usersFileLocation)

    for user in userData:

        if body["username"] == user["username"]:
            if body["password"] == decrypt(3, user["password"]):
                response["message"] = "Login Success, welcome {}".format(user["fullname"])
                response["data"] = user
                response["token"] = encode(user["username"])
                del response["data"]["password"]
            break

    return jsonify(response)

@app.route('/user', methods=["GET"]) #get all user
def getUser():
    response = {}
    response["message"] = "Tidak ada data"
    response["data"] = []

    #siapin file buat di read
    userData = readFile(usersFileLocation)

    if userData != []:
        response["message"] = "Data all user"
        response["data"] = userData

    return jsonify(response)

@app.route('/user/<int:id>', methods=["GET"]) #get 1 user
def getUserId(id):
    response = {}
    response["message"] = "User not found"
    response["data"] = []


    #siapin file buat di read
    userData = readFile(usersFileLocation)

    for user in userData:
        if id == user["userid"]:
            response["message"] = "{} data".format(user["fullname"])
            response["data"] = user
            break

    return jsonify(response)

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
    writeFile(usersFileLocation, usersData)
  
    return "Update Success"

@app.route('/outclass/<int:id>', methods=["POST"]) #outclass 1 user
def outClass(id):
    body = request.json

    response = {}
    response["message"] = "Fail! User is not in the class!"
    response["data"] = []

    #read classes-file
    classesData = readFile(classesFileLocation)

    #read users-file
    usersData = readFile(usersFileLocation)

    for class_ in classesData:
        if id == class_["classid"]:
            for user in usersData:
                if body["userid"] in class_["students"]:
                    response["message"] = "User {} out from the class successfully!".format(body["userid"])
                    response["data"] = body
                    class_["students"].remove(body["userid"])
                    break
               
    writeFile(classesFileLocation, classesData)

    for user in usersData: 
        if body["userid"] == user["userid"]:
            if id in user["classes_as_student"]:
                user["classes_as_student"].remove(id)
                break

    writeFile(usersFileLocation, usersData)

    return jsonify(response)

@app.route('/classlist', methods=["GET"]) #get all class
def classList():
    classData = readFile(classesFileLocation)
    
    return jsonify(classData)

@app.route('/class/create', methods=["POST"]) #create class
def createClass():
    body = request.json
    body["students"] = []
    body["classwork"] = []

    response = {}
    response["message"] = "Create Class Success"
    response["data"] = []

    #baca file classes
    classesData = readFile(classesFileLocation)

    # check apakah kelas sudah ada
    classidAlreadyExist = False
    for class_ in classesData:
        if class_["classid"] == body["classid"]:
            response["message"] = "Class ID {} is already exist".format(body["classid"])
            classidAlreadyExist = True
            break
    
    if not classidAlreadyExist:
        #tambah ke file classes 
        classesData.append(body)
        writeFile(classesFileLocation, classesData)

        #baca file users
        usersData = readFile(usersFileLocation)
        for user in usersData:
            if user["userid"] == body["teachers"]:
                user["classes_as_teacher"].append(body["classid"])
    
        #tambah classid ke file users
        writeFile(usersFileLocation, usersData)

        response["data"] = body

    return jsonify(response)
    
@app.route('/class/<int:id>', methods=["GET"]) #get 1 class
def getClassId(id):
    response = {}
    response["message"] = "Class with classid {} is not found.".format(id)
    response["data"] = []

    #siapin file classes buat di read
    classData = readFile(classesFileLocation)

    #siapin file users buat di read
    userData = readFile(usersFileLocation)

    for classX in classData:
        if id == classX["classid"]:
            classX["students"] = []
            response["message"] = "Class {} found successfully!".format(id)
            response["data"] = classX
            for user in userData:
                if id in user["classes_as_student"]:
                    classX["students"].append(user["fullname"])
            return jsonify(response) 
    return jsonify(response)
 
@app.route('/updateClass/<int:id>', methods=["PUT"]) #update 1 class
def updateClassId(id):
    classesData = classList().json
    body = request.json

    response = {}
    response["message"] = "Unknown error. No changes"
    response["data"] = []


    for class_ in classesData:
        if id == class_["classid"]:
            class_["classname"] = body["classname"]
            response["message"] = "Class update successfully!"
            response["data"] = body
            break
    
    #update ke file class
    writeFile(classesFileLocation, classesData)
  
    return jsonify(response)

@app.route('/deleteClass/<int:id>', methods=['DELETE']) #delete 1 class
def deleteClass(id):
    response = {}
    response["message"] = "Error. Kelas sudah tidak ada!"
    response["data"] = []

    #read data class
    classesData = readFile(classesFileLocation)

    for class_ in range(len(classesData)):
        if id == classesData[class_]["classid"]:
            response["message"] = "Class {} deleted successfully!".format(id)
            response["data"] = classesData[class_]
            del classesData[class_]
            break
        # return "Error. Kelas sudah tidak ada!"
    
    #write data class
    writeFile(classesFileLocation, classesData)
    
    #read data classwork
    classesWorkData = readFile(classesWorkFileLocation)

    for classWork in range(len(classesWorkData)):
        if id == classesWorkData[classWork]["class"]:
            del classesWorkData[classWork]
            break

    #write data classWork
    writeFile(classesWorkFileLocation, classesWorkData)

    #read data user
    usersData = readFile(usersFileLocation)

    for user in usersData:
        if id in user["classes_as_student"]:
            user["classes_as_student"].remove(id)
            break

    #write data users
    writeFile(usersFileLocation, usersData)

    return jsonify(response)

@app.route('/classwork/create', methods=["POST"]) #create classwork
def createClassWork():
    body = request.json

    response = {}
    response["message"] = "{} is wrong class id!".format(body["class"])
    response["data"] = []
   
    
    #read data
    classWorkData = readFile(classesWorkFileLocation)
    classesData = classList().json

    for class_ in classesData:
        if class_["classid"] == body["class"]:
            class_["classwork"].append(body["workid"])
            classWorkData.append(body)


            response["message"] = "Classwork {} created successfully!".format(body["workid"])
            response["data"] = body


            #write data
            writeFile(classesWorkFileLocation, classWorkData)
            writeFile(classesFileLocation, classesData)

    return jsonify(response)

@app.route('/classworklist', methods=["GET"]) #get all classwork
def getClassWork():
    #siapin file buat di read
    classWorkData = readFile(classesWorkFileLocation)
    
    return jsonify(classWorkData)

@app.route('/classwork/<int:id>', methods=["GET"]) #get 1 classwork
def getClassWorkId(id):
    response = {}
    response["message"] = "Classwork not found"
    response["data"] = []

    #siapin file buat di read
    classWorkData = readFile(classesWorkFileLocation)

    for classwork in classWorkData:
        if id == classwork["workid"]:
            response["message"] = "Classwork {} found successfully!".format(classwork["workid"])
            response["data"] = classwork
            return jsonify(response) 
        else:
            pass
    return jsonify(response)

@app.route('/classwork/assign/<int:id>', methods=["POST"]) #assign classwork
def assignClassWork(id):
    body = request.json

    #siapin data classwork
    classWorkData = readFile(classesWorkFileLocation)

    #siapin data user
    usersData = readFile(usersFileLocation)

    for classwork in classWorkData:
        if id == classwork["workid"]:
            for user in usersData:
                if body["userid"] == user["userid"]:
                    classwork["answer"].append(body)
     
    writeFile(classesWorkFileLocation, classWorkData)
    response = {}
    response["message"] = "Answer sent successfully!"
    response["body"] = body

    return jsonify(response)

@app.route('/classwork/update/<int:id>', methods=["POST"]) #update classork
def updateClassWork(id):
    body = request.json

    #read data classwork
    classesWorkData = readFile(classesWorkFileLocation)

    for classWork in classesWorkData:
        if id == classWork["workid"]:
            classWork["question"] = body["question"]

    #write data classwork
    writeFile(classesWorkFileLocation, classesWorkData)

    response = {}
    response["message"] = "Update question on work id {} success!".format(id)
    response["data"] = body

    return jsonify(response)

@app.route('/classwork/delete/<int:id>', methods=["DELETE"]) #delete 1 classwork
def deleteClassWork(id):
    response = {}
    response["message"] = "Error. Classwork is already deleted!"
    response["data"] = []

    #read-write data classwork
    classesWorkData = readFile(classesWorkFileLocation)
    
    for classWork in range(len(classesWorkData)):
        if id == classesWorkData[classWork]["workid"]:
            response["message"] = "Classwork {} deleted successfuly!".format(id)
            response["data"] = classesWorkData[classWork]
            del classesWorkData[classWork]
            break
        # return "Error. Classwork sudah tidak ada!"

    #write data classwork
    writeFile(classesWorkFileLocation, classesWorkData)

    #read data class
    classesData = readFile(classesFileLocation)

    for class_ in classesData:
        if id in class_["classwork"]:
            class_["classwork"].remove(id)
            break

    #write data class
    writeFile(classesFileLocation, classesData)

    return jsonify(response)

@app.route('/joinClass', methods=["POST"]) #join class student
def joinClass():
    body = request.json

    #nambahin userid ke classes-file
    classesData = readFile(classesFileLocation)

    for class_ in classesData:
        if body["classid"] == class_["classid"]:
            if (body["userid"] not in class_["students"]) and (body["userid"] not in class_["teachers"]):
                class_["students"].append(body["userid"])
    
    writeFile(classesFileLocation, classesData)

    #nambahin classid ke users-file
    usersData = readFile(usersFileLocation)
    
    for user in usersData: 
        if body["userid"] == user["userid"]:
            if (body["classid"] not in user["classes_as_student"]) and (body["classid"] not in user["classes_as_teacher"]):
                user["classes_as_student"].append(body["classid"])
    
    writeFile(usersFileLocation, usersData)

    response = {}
    response["message"] = "User {} joined to {} class".format(body["userid"], body["classid"])
    response["data"] = body

    return jsonify(response)

@app.route('/joinClassTeacher', methods=["POST"]) #join class teacher
def joinClassTeacher():
    body = request.json

    #nambahin userid ke classes-file
    classesData = readFile(classesFileLocation)

    for class_ in classesData:
        if body["classid"] == class_["classid"]:
            if (body["userid"] not in class_["teachers"]) and (body["userid"] not in class_["students"]):
                class_["teachers"].append(body["userid"])
            else:
                return "Join failed! Anda sudah terdaftar!"
    
    classesFile = writeFile(classesFileLocation, classesData)

    #nambahin classid ke users-file
    usersData = readFile(usersFileLocation)
    
    for user in usersData: 
        if body["userid"] == user["userid"]:
            if (body["classid"] not in user["classes_as_student"]) and (body["classid"] not in user["classes_as_teacher"]):
                user["classes_as_teacher"].append(body["classid"])
            else:
                return "Join failed! Anda sudah terdaftar!"
    
    usersFile = writeFile(usersFileLocation, usersData)

    return "Success"

@app.errorhandler(404)
def error404(e):
    messages = {
        "statusCode": 404,
        "message": "URL ga ketemu"
    }
    return jsonify(messages)