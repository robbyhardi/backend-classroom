from flask import Flask, request, json, jsonify
import os

app = Flask(__name__)

@app.route('/')
def testConnection():
    return "connected"

@app.route('/register', methods=["POST"])
def register():
    body = request.json
    userData = []

    if os.path.exists('./users-file.json'):
        userFile = open('./users-file.json', 'r')
        userData = json.load(userFile)

    userData.append(body)
    
    #siapin file buat di write
    userFile = open('./users-file.json','w')
    userFile.write(json.dumps(userData))
    userFile.close()


    return jsonify(body)

@app.route('/login', methods=["POST"]) #login
def login():
    body = request.json

    #siapin file buatt di read
    userFile = open('./users-file.json', 'r')
    userData = json.load(userFile)
    userFile.close()

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
    #siapin file buatt di read
    userFile = open('./users-file.json', 'r')
    userData = json.load(userFile)
    userFile.close()

    return jsonify(userData)

@app.route('/user/<int:id>', methods=["GET"]) #get 1 user
def getUserId(id):
    #siapin file buat di read
    userFile = open('./users-file.json', 'r')
    userData = json.load(userFile)
    userFile.close()

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
    usersFile = open('./users-file.json', 'w')
    usersFile.write(json.dumps(usersData))
    usersFile.close()
  
    return "Update Success"

@app.route('/classlist', methods=["GET"]) #get all class
def classList():
    classFile = open('./classes-file.json', 'r')
    classData = json.load(classFile)
    classFile.close()

    return jsonify(classData)

@app.route('/class/create', methods=["POST"]) #create class
def createClass():
    classData = []
    
    #baca file classes
    if os.path.exists('./classes-file.json'):  
        classFile = open('./classes-file.json', 'r')
        classData = json.load(classFile)

    body = request.json
    body["students"] = []
    body["classwork"] = []

    #tambah ke file classes 
    classData.append(body)

    classFile = open('./classes-file.json','w')
    classFile.write(json.dumps(classData))
    classFile.close()

    #baca file users
    usersFile = open('./users-file.json', 'r')
    usersData = json.load(usersFile)

    #tambah classid ke file users
    usersFile = open('./users-file.json', 'w')
    usersFile.write(json.dumps(usersData))
    usersFile.close()

    return jsonify(body)
    
@app.route('/class/<int:id>', methods=["GET"]) #get 1 class
def getClassId(id):
    #siapin file buat di read
    classFile = open('./classes-file.json', 'r')
    classData = json.load(classFile)
    classFile.close()

    #siapin file buat di read
    userFile = open('./users-file.json', 'r')
    userData = json.load(userFile)
    userFile.close()

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
    classesFile = open('./classes-file.json', 'w')
    classesFile.write(json.dumps(classesData))
    classesFile.close()
  
    return "Update Success"

@app.route('/classwork/create', methods=["POST"]) #create classwork
def createClassWork():
    body = request.json
    classWorkData= []

    if os.path.exists('./classwork-file.json'):
        classWorkFile = open('./classwork-file.json', 'r')
        classWorkData = json.load(classWorkFile)
    
    classWorkData.append(body)

    classWorkFile = open('./classwork-file.json', 'w')
    classWorkFile.write(json.dumps(classWorkData))
    classWorkFile.close()

    #read data
    classesData = classList().json

    for class_ in classesData:
        if class_["classid"] == body["class"]:
            class_["classwork"].append(body["workid"])

    #write data
    classesFile = open('./classes-file.json', 'w')
    classesFile.write(json.dumps(classesData))
    classesFile.close()

    return jsonify(body)

@app.route('/classworklist', methods=["GET"]) #get all classwork
def getClassWork():
    #siapin file buat di read
    classWorkFile = open('./classwork-file.json', 'r')
    classWorkData = json.load(classWorkFile)
    classWorkFile.close()

    return jsonify(classWorkData)

@app.route('/classwork/assign/<int:id>', methods=["POST"]) #assign classwork
def assignClassWork():
    classWorkData = getClassWork().json

@app.route('/joinClass', methods=["POST"]) #join class student
def joinClass():
    body = request.json

    #nambahin userid ke classes-file
    classesFile = open('./classes-file.json','r')
    classesData = json.load(classesFile)

    for class_ in classesData:
        if body["classid"] == class_["classid"]:
            if (body["userid"] not in class_["students"]) and (body["userid"] not in class_["teachers"]):
                class_["students"].append(body["userid"])
    
    classesFile = open('./classes-file.json', 'w')
    classesFile.write(json.dumps(classesData))
    classesFile.close()

    #nambahin classid ke users-file
    usersFile = open('./users-file.json', 'r')
    usersData = json.load(usersFile)
    
    for user in usersData: 
        if body["userid"] == user["userid"]:
            if (body["classid"] not in user["classes_as_student"]) and (body["classid"] not in user["classes_as_teacher"]):
                user["classes_as_student"].append(body["classid"])
    
    usersFile = open('./users-file.json', 'w')
    usersFile.write(json.dumps(usersData))
    usersFile.close()

    return "Success"

@app.route('/joinClassTeacher', methods=["POST"]) #join class teacher
def joinClassTeacher():
    body = request.json

    #nambahin userid ke classes-file
    classesFile = open('./classes-file.json','r')
    classesData = json.load(classesFile)

    for class_ in classesData:
        if body["classid"] == class_["classid"]:
            if (body["userid"] not in class_["teachers"]) and (body["userid"] not in class_["students"]):
                class_["teachers"].append(body["userid"])
            else:
                return "Join failed! Anda sudah terdaftar!"
    
    classesFile = open('./classes-file.json', 'w')
    classesFile.write(json.dumps(classesData))
    classesFile.close()

    #nambahin classid ke users-file
    usersFile = open('./users-file.json', 'r')
    usersData = json.load(usersFile)
    
    for user in usersData: 
        if body["userid"] == user["userid"]:
            if (body["classid"] not in user["classes_as_student"]) and (body["classid"] not in user["classes_as_teacher"]):
                user["classes_as_teacher"].append(body["classid"])
            else:
                return "Join failed! Anda sudah terdaftar!"
    
    usersFile = open('./users-file.json', 'w')
    usersFile.write(json.dumps(usersData))
    usersFile.close()

    return "Success"
