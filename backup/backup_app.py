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


    return jsonify(body)


@app.route('/login', methods=["POST"])
def login():
    body = request.json

    #siapin file buatt di read
    userFile = open('./users-file.json', 'r')
    userData = json.load(userFile)

    for user in userData:

        if body["username"] == user["username"]:
            if body["password"] == user["password"]:
                return "Login Success"
            else:
                return "Login Fail. Wrong Password"
        else:
            pass
    return "Username not found" 

@app.route('/user', methods=["GET"])
def getUser():
    #siapin file buatt di read
    userFile = open('./users-file.json', 'r')
    userData = json.load(userFile)

    return jsonify(userData)

# @app.route('/class', methods=["POST"])
# def createClass():
#     body = request.json
    
#     #siapin file buat di write
#     userFile = open('./class-file.json', 'w')
#     userFile.write(json.dumps(body))

#     return jsonify(body)

@app.route('/classlist', methods=["GET"])
def classList():
    classFile = open('./classes-file.json', 'r')
    classData = json.load(classFile)

    return jsonify(classData)

@app.route('/class/create', methods=["POST"])
def createClass():
    body = request.json
    classData = []

    if os.path.exists('./classes-file.json'):  
        classFile = open('./classes-file.json', 'r')
        classData = json.load(classFile)

    classData.append(body)

    classFile = open('./classes-file.json','w')
    classFile.write(json.dumps(classData))

    return jsonify(body)
    
@app.route('/user/<x>', methods=["GET"])
def getUserId(x):
    x = int(x)
    #siapin file buat di read
    userFile = open('./users-file.json', 'r')
    userData = json.load(userFile)

    for user in userData:
        if x == user["userid"]:
            return jsonify(user)
        else:
            pass
    return "User not found"

@app.route('/class/<z>', methods=["GET"])
def getClassId(z):
    z = int(z)
    #siapin file buat di read
    classFile = open('./classes-file.json', 'r')
    classData = json.load(classFile)

    for classX in classData:
        if z == classX["classid"]:
            return jsonify(classX)
        else:
            pass
    return "Class not found"

@app.route('/class/classwork/create', methods=["POST"])
def createClassWork():
    body = request.json
    classWorkData= []

    if os.path.exists('./classwork-file.json'):
        classWorkFile = open('./classwork-file.json', 'r')
        classWorkData = json.load(classWorkFile)
    
    classWorkData.append(body)

    classWorkFile = open('./classwork-file.json', 'w')
    classWorkFile.write(json.dumps(classWorkData))

    return jsonify(body)

