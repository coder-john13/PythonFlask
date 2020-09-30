from flask import Flask, request, render_template, session
import os


app = Flask(__name__)

app.secret_key = os.urandom(16)

@app.route("/")
def hello():
	return "Hello World!"


@app.route('/assignment11.html',methods=["GET","POST"])
def start():
    username = None
    password = None
    first = None
    last = None
    create = False
    attempted = False
    #print(request.args)
    #print("The session data:", session)
    if "edit" in request.args:
        #print("preparing to edit the form...")
        #print("final step to editing...")
        #print(request.args)
        session["fname"] = request.args["fname"]
        session["lname"] = request.args["lname"]
        session["color"] = request.args["color"]
        session["title"] = request.args["title"]
        session["image"] = request.args["image"]

        with open('assignment11-account-info.txt','r') as file:
            data = file.readlines()

        for line in range(0,len(data)):
            token = data[line].split(";")
            if token[0] == session["username"]:
                #print("user found for replacement")
                data[line] = session["username"]+ ";" + session["password"]+ ";" + session["fname"] + ";" + session["lname"]\
                             +";"+ session["color"]+ ";" + session["title"] + ";" + session["image"] + '\n'

        with open('assignment11-account-info.txt', "w") as file:
            file.writelines(data)
        return render_template("session.html")

    if "logout" in request.args:
        #print("LOGING OUT")
        session.clear()
        return render_template('startup.html')

    if "un" in request.args and "pw" in request.args and "fname" in request.args and "lname" in request.args:
        #print("CREATING A NEW USER")
        username = request.args["un"]
        password = request.args["pw"]
        first = request.args["fname"]
        last = request.args["lname"]
        if username == "" or password == "" or first == "" or last == "":
            #print("cannot create user because a field is blank")
            return render_template("blank.html")
        with open('assignment11-account-info.txt', "r") as file:
            for line in file:
                lst = line.split(";")
                if lst[0] == username:
                    #print("there is already someone with this username")
                    return render_template("UsernameTaken.html")


        session["username"] = username
        session["password"] = password
        session["fname"] = first
        session["lname"] = last
        session["color"] = "white"
        session["title"] = "Welcome to " + first + " "+ last + "'s Assignment 11 web site!"
        session["image"] = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Stick_Figure.svg/1200px-Stick_Figure.svg.png"

        #add user to the list
        with open('assignment11-account-info.txt', "r") as file:
            data = file.readlines()
        #print("the data from the file:\n",data)
        newInfo = username+";"+password+";"+first+";"+last+";"+ session["color"]+";"+session["title"]+";"+session["image"] + '\n'
        data.append(newInfo)
        #print("the data after being appended:\n",data)
        with open('assignment11-account-info.txt', "w") as file:
            file.writelines(data)
        #print("user added")
        return render_template("session.html")

    elif "un" in request.args and "pw" in request.args:
        #print("ATTEMPTING TO LOG YOU IN")
        username = request.args["un"]
        password = request.args["pw"]
        #check the list
        with open('assignment11-account-info.txt', "r") as file:
            for line in file:
                lst = line.split(";")
                if lst[0] == username and lst[1] == password:
                    #print("user found")
                    session["username"] = username
                    session["password"] = password
                    session["fname"] = lst[2]
                    session["lname"] = lst[3]
                    session["color"] = lst[4]
                    session["title"] = lst[5]
                    session["image"] = lst[6]
                    return render_template("session.html")

        #print("password and username combination not found")
        return render_template("passwordIncorrect.html")

    if bool(session):
        return render_template("session.html")

    #print("GOING INTO DEFUALT MODE")
    return render_template('startup.html',attempt=attempted)






