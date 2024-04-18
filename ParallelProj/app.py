from datetime import datetime

from flask import Flask, render_template, request, flash
import mysql.connector as msc
from contextlib import closing
import hashlib
import os

# because mysql.connector.connection() objects are pooled, for thread safety, make sure to only call connection() in a 'with' statement (preferred because close() is called automatically upon exiting with block)
# OR have a finally: block after a try: block, and call myConnection.close() in the finally: block
# see for more details on 'Context Managers and Python's with Statement': https://realpython.com/python-with-statement/

currentUser = ""  # used to keep track of currently logged in user throughout program (To match TaskTracker.Users tuple with MySQL 'CREATE USER' user)
# not sure if this is properly 'distributed'. Is currentUser unique to each flask website connection, or shared across all of them? Bad if shared
# Just learned the following: "When running the development server - which is what you get by running app.run(), you get a single synchronous process, which means at most 1 request is being processed at a time."
# okay so as long as we don't have to deploy the flask application itself, it seems we can check the distributed box by just using locks and transactions with database queries
currentId = -1  # Currently the app has no way of getting the id to the task and as such every task is shown instead of only the tasks of the current user

app = Flask(__name__)
app.secret_key = "anystringhere"  # if this is removed flashes don't work


@app.route('/')
def LoginPage():
    global currentUser
    global currentId
    currentUser = ""  # this line means this route can be used to log out, in addition to logging in
    currentId = -1
    return render_template('login.html')


@app.route('/loginForm', methods=['POST', 'GET'])
def loginForm():
    global currentUser  # must explicitly use global keyword if using the global variable 'currentUser' in a function
    global currentId

    if request.method == 'POST':

        uname = request.form['Username']
        pword = request.form['Password']

        with closing(msc.connect(host="cop4521-2.c5w0oqowm22h.us-east-1.rds.amazonaws.com", port="3306", user="admin",
                                 password="masterpassword", database='TaskTracker')) as con:
            cur = con.cursor()

            try:
                cur.execute("SELECT UserName, PasswordHash, Salt, Id FROM Users WHERE UserName = %s LIMIT 1", (uname,))
                row = cur.fetchone()
                tempPHash = row[1]
                tempSalt = row[2]
                currentId = row[3]

            except:
                flash("User " + uname + " does not exist.")
                con.close()  # just to be safe, must explicitly close connection before rendering any other templates
                return render_template('login.html')

            else:
                if (tempPHash == hashlib.sha256(tempSalt.encode('utf-8') + pword.encode('utf-8')).hexdigest()):
                    currentUser = uname
                    # after this, database connection should be using current user, not admin user
                    return render_template('index.html', curUser=currentUser)
                else:
                    flash("Login failed.")
                    return render_template('login.html')


@app.route('/createAccountPage')
def createAccountPage():
    return render_template('createAccount.html')


@app.route('/createAccountForm', methods=['POST', 'GET'])
def createAccountForm():
    if request.method == 'POST':

        uname = request.form['Username']
        pword = request.form['Password']

        # create mysql user which will exist alongside user
        # user's mysql username will be used for sql queries
        # so must keep track of currently logged in user
        # db username VARCHAR will have to be the same as mysql USER
        # db user = one that we check to see if exists in users table
        # mysql user = one that can receieve roles and permissions via mysql commands
        # username must be the same for both

        with closing(msc.connect(host="cop4521-2.c5w0oqowm22h.us-east-1.rds.amazonaws.com", port="3306", user="admin",
                                 password="masterpassword", database='TaskTracker')) as con:
            cur = con.cursor()

            try:
                salt = os.urandom(
                    16).hex()  # 16 bytes = 128 bits (not sure if database is getting/storing salts correctly: must check on this) converted to hex because mySQL can't handle urandom bytes object
                pwordHash = hashlib.sha256(
                    salt.encode() + pword.encode()).hexdigest()  # salt plus utf-8 encoded password hashed and converted to hexadecimal

                cur.execute("INSERT INTO Users (UserName, PasswordHash, Salt) VALUES (%s, %s, %s)",
                            (uname, pwordHash, salt))
                con.commit()

            except msc.Error as err:
                # print("Error executing MySQL query:", err.msg)
                # print("Error code:", err.errno)
                # print("SQLSTATE:", err.sqlstate)
                con.rollback()
                flash('Account creation failed.')
                return render_template('createAccount.html')

            else:
                # cur.execute("CREATE USER %s", (uname,))        # currently causes exception if MySQL user already exists, should use another try...except...else to handle this error
                # cur.execute("GRANT FreeUserRole TO %s", (uname,))      # currently admin user can't grant roles or privileges to users for some reason, given error: mysql.connector.errors.ProgrammingError: 1227 (42000): Access denied; you need (at least one of) the WITH ADMIN, ROLE_ADMIN, SUPER privilege(s) for this operation
                con.commit()
                flash('Account ' + uname + ' created sucessfully.')
                return render_template('login.html')


@app.route('/home')
def home():
    global currentUser
    return render_template('index.html', curUser=currentUser)


@app.route('/newtask')
def new_task():
    rows = []
    with closing(msc.connect(host="cop4521-2.c5w0oqowm22h.us-east-1.rds.amazonaws.com",port="3306",user="admin",password="masterpassword", database='TaskTracker')) as con:
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM Categories")
        rows = cur.fetchall()
    return render_template('addTask.html', cats=rows)


@app.route('/changepriv')
def change_priv():
    return (render_template('changePrivileges.html'))


@app.route('/becomefree')
def become_free():
    flash('Changed user to a free user')
    return render_template('changePrivileges.html')


@app.route('/becomepremium')
def become_premium():
    flash('Changed user to a premium user')
    return render_template('changePrivileges.html')


@app.route('/addtask', methods=['POST', 'GET'])
def addtask():
    global currentUser
    global currentId
    if request.method == 'POST':

        nm = request.form['Name']
        dscp = request.form['Description']
        dd = request.form['DueDate']
        pr = request.form['Priority']
        cid = request.form['CategoryID']
        with closing(msc.connect(host="cop4521-2.c5w0oqowm22h.us-east-1.rds.amazonaws.com", port="3306", user="admin",
                                 password="masterpassword", database='TaskTracker')) as con:

            try:
                current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                cur = con.cursor()
                print("before insert tasks")
                cur.execute("INSERT INTO Tasks (Name,Description,CreationDate,DueDate,Priority,Categories_Id) VALUES (%s,%s,%s,%s,%s,%s)"
                            , (nm, dscp, current_time, dd, pr, cid))
                con.commit()
                print("before select tasks")
                cur.execute(
                    "SELECT Id FROM Tasks WHERE Name=%s AND Description=%s AND DueDate=%s AND Priority=%s AND Categories_Id=%s AND CreationDate=%s",
                    (nm, dscp, dd, pr, cid, current_time))
                id = cur.fetchone()
                print(id[0])
                print("before insert assignments")
                cur.execute("INSERT INTO Assignments (Tasks_Id,Users_Id) VALUES (%s,%s)", (id[0], currentId))
                con.commit()

            except:
                print("womp womp")
                con.rollback()

            finally:
                # con.close()    # realized that con.close() is unneccesary if connect() is preceded by the 'with' keyword. ( close() is automatically called upon exiting with block )
                return render_template('index.html', curUser=currentUser)


@app.route('/listtask/<order>/<sort>', methods=['GET'])
def listtask(order, sort):
    global currentId
    if request.method == 'GET':
        with closing(msc.connect(host="cop4521-2.c5w0oqowm22h.us-east-1.rds.amazonaws.com", port="3306", user="admin",
                                 password="masterpassword", database='TaskTracker')) as con:
            cur = con.cursor(dictionary=True)
            if order == "a":
                if sort == "id":
                    cur.execute("SELECT Tasks.Id, Tasks.Name, Tasks.Description, Tasks.CreationDate, Tasks.DueDate, "
                                "Tasks.Priority, Tasks.Categories_Id FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                                "Assignments.Tasks_Id=Tasks.Id ORDER BY Tasks.Id ASC", (currentId,))
                elif sort == "name":
                    cur.execute("SELECT Tasks.Id, Tasks.Name, Tasks.Description, Tasks.CreationDate, Tasks.DueDate, "
                                "Tasks.Priority FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                                "Assignments.Tasks_Id=Tasks.Id ORDER BY Tasks.Name ASC", (currentId,))
                elif sort == "descr":
                    cur.execute("SELECT Tasks.Id, Tasks.Name, Tasks.Description, Tasks.CreationDate, Tasks.DueDate, "
                                "Tasks.Priority FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                                "Assignments.Tasks_Id=Tasks.Id ORDER BY Tasks.Description ASC", (currentId,))
                elif sort == "creation_date":
                    cur.execute("SELECT Tasks.Id, Tasks.Name, Tasks.Description, Tasks.CreationDate, Tasks.DueDate, "
                                "Tasks.Priority FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                                "Assignments.Tasks_Id=Tasks.Id ORDER BY Tasks.CreationDate ASC", (currentId,))
                elif sort == "due_date":
                    cur.execute("SELECT Tasks.Id, Tasks.Name, Tasks.Description, Tasks.CreationDate, Tasks.DueDate, "
                                "Tasks.Priority FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                                "Assignments.Tasks_Id=Tasks.Id ORDER BY Tasks.DueDate ASC", (currentId,))
                elif sort == "priority":
                    cur.execute("SELECT Tasks.Id, Tasks.Name, Tasks.Description, Tasks.CreationDate, Tasks.DueDate, "
                                "Tasks.Priority FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                                "Assignments.Tasks_Id=Tasks.Id ORDER BY Tasks.Priority ASC", (currentId,))
                else:
                    cur.execute("SELECT Tasks.Id, Tasks.Name, Tasks.Description, Tasks.CreationDate, Tasks.DueDate, "
                                "Tasks.Priority FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                                "Assignments.Tasks_Id=Tasks.Id ORDER BY Tasks.Id ASC", (currentId,))

            elif order == "d":
                if sort == "id":
                    cur.execute("SELECT Tasks.Id, Tasks.Name, Tasks.Description, Tasks.CreationDate, Tasks.DueDate, "
                                "Tasks.Priority FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                                "Assignments.Tasks_Id=Tasks.Id ORDER BY Tasks.Id DESC", (currentId,))
                elif sort == "name":
                    cur.execute("SELECT Tasks.Id, Tasks.Name, Tasks.Description, Tasks.CreationDate, Tasks.DueDate, "
                                "Tasks.Priority FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                                "Assignments.Tasks_Id=Tasks.Id ORDER BY Tasks.Name DESC", (currentId,))
                elif sort == "descr":
                    cur.execute("SELECT Tasks.Id, Tasks.Name, Tasks.Description, Tasks.CreationDate, Tasks.DueDate, "
                                "Tasks.Priority FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                                "Assignments.Tasks_Id=Tasks.Id ORDER BY Tasks.Description DESC", (currentId,))
                elif sort == "creation_date":
                    cur.execute("SELECT Tasks.Id, Tasks.Name, Tasks.Description, Tasks.CreationDate, Tasks.DueDate, "
                                "Tasks.Priority FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                                "Assignments.Tasks_Id=Tasks.Id ORDER BY Tasks.CreationDate DESC", (currentId,))
                elif sort == "due_date":
                    cur.execute("SELECT Tasks.Id, Tasks.Name, Tasks.Description, Tasks.CreationDate, Tasks.DueDate, "
                                "Tasks.Priority FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                                "Assignments.Tasks_Id=Tasks.Id ORDER BY Tasks.DueDate DESC", (currentId,))
                elif sort == "priority":
                    cur.execute("SELECT Tasks.Id, Tasks.Name, Tasks.Description, Tasks.CreationDate, Tasks.DueDate, "
                                "Tasks.Priority FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                                "Assignments.Tasks_Id=Tasks.Id ORDER BY Tasks.Priority DESC", (currentId,))
                else:
                    cur.execute("SELECT Tasks.Id, Tasks.Name, Tasks.Description, Tasks.CreationDate, Tasks.DueDate, "
                                "Tasks.Priority FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                                "Assignments.Tasks_Id=Tasks.Id ORDER BY Tasks.Id DESC", (currentId,))
            rows = cur.fetchall()

            return render_template("listTasks.html", rows=rows)

    else:
        return "This route only accepts GET requests."


@app.route('/deletetask', methods=['POST', 'GET'])
def deletetask():
    global currentId
    with closing(msc.connect(host="cop4521-2.c5w0oqowm22h.us-east-1.rds.amazonaws.com", port="3306", user="admin",
                             password="masterpassword", database='TaskTracker')) as con:
        cur = con.cursor(dictionary=True)

        cur.execute("SELECT Tasks.Id, Tasks.Name FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                    "Assignments.Tasks_Id=Tasks.Id", (currentId,))

        rows = cur.fetchall()

        return render_template("deleteTask.html", rows=rows)


@app.route('/updatetask', methods=['POST', 'GET'])
def updatetask():
    global currentId
    with closing(msc.connect(host="cop4521-2.c5w0oqowm22h.us-east-1.rds.amazonaws.com", port="3306", user="admin",
                             password="masterpassword", database='TaskTracker')) as con:
        cur = con.cursor(dictionary=True)

        cur.execute("SELECT Tasks.Id, Tasks.Name FROM Tasks CROSS JOIN Assignments ON Assignments.Users_Id=%s AND "
                    "Assignments.Tasks_Id=Tasks.Id", (currentId,))

        rows = cur.fetchall()

        return render_template("updateTask.html", rows=rows)


@app.route('/updatingtask', methods=['POST', 'GET'])
def updatingtsk():
    if request.method == 'POST':
        # noinspection PyUnresolvedReferences
        id = request.form.get('Id')
        print(id)

        with closing(msc.connect(host="cop4521-2.c5w0oqowm22h.us-east-1.rds.amazonaws.com", port="3306", user="admin",
                                 password="masterpassword", database='TaskTracker')) as con:
            cur = con.cursor()

            try:
                cur.execute("DELETE FROM Tasks WHERE Tasks.Id = %s", (id,))
                con.commit()
                cur.execute("DELETE FROM Assignments WHERE Assignments.Tasks_Id = %s", (id,))
                con.commit()

            except:
                print("womp womp")
                con.rollback()

            finally:
                return render_template('updateThisTask.html')


@app.route('/deletingtask', methods=['POST', 'GET'])
def deletingtsk():
    global currentUser
    if request.method == 'POST':

        id = request.form.get('Id')
        print(id)

        with closing(msc.connect(host="cop4521-2.c5w0oqowm22h.us-east-1.rds.amazonaws.com", port="3306", user="admin",
                                 password="masterpassword", database='TaskTracker')) as con:
            cur = con.cursor()

            try:
                cur.execute("DELETE FROM Tasks WHERE Tasks.Id = %s", (id,))
                con.commit()
                cur.execute("DELETE FROM Assignments WHERE Assignments.Tasks_Id = %s", (id,))
                con.commit()

            except:
                print("womp womp")
                con.rollback()

            finally:
                return render_template('index.html', curUser=currentUser)

@app.route('/categories', methods=['POST', 'GET'])
def categories():
    if request.method == 'POST':
        with closing(msc.connect(host="cop4521-2.c5w0oqowm22h.us-east-1.rds.amazonaws.com",port="3306",user="admin",password="masterpassword", database='TaskTracker')) as con:
            cur = con.cursor(dictionary=True)
            try:
                if request.form['Action'] == 'Add':
                    cur.execute("INSERT INTO Categories(Name) VALUES(%s)", (request.form['Name'],))
                elif request.form['Action'] == 'Delete':
                    cur.execute("DELETE FROM Categories WHERE Id = %s", (request.form['Id'],))
                elif request.form['Action'] == 'Update':
                    cur.execute("UPDATE Categories SET Name = %s WHERE Id = %s", (request.form['Name'], request.form['Id']))
                con.commit()
            except:
                con.rollback()

    with closing(msc.connect(host="cop4521-2.c5w0oqowm22h.us-east-1.rds.amazonaws.com",port="3306",user="admin",password="masterpassword", database='TaskTracker')) as con:
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM Categories")
        rows = cur.fetchall()
        return render_template('categories.html', rows=rows)

@app.route('/alltables', methods=['POST', 'GET'])
def allTables():
    with closing(msc.connect(host="cop4521-2.c5w0oqowm22h.us-east-1.rds.amazonaws.com",port="3306",user="admin",password="masterpassword", database='TaskTracker')) as con:
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM Assignments")
        assi = cur.fetchall()
        cur.execute("SELECT * FROM Categories")
        cats = cur.fetchall()
        cur.execute("SELECT * FROM Tasks")
        tsks = cur.fetchall()
        cur.execute("SELECT * FROM Users")
        usrs = cur.fetchall()
        return render_template('allTables.html', assignments = assi, categories=cats, tasks = tsks, users = usrs)

if __name__ == '__main__':
    app.run(debug=True)
