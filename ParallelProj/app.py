from datetime import date

from flask import Flask, render_template, request
import sqlite3 as sql


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/newtask')
def new_task():
    return render_template('addTask.html')


@app.route('/addtask', methods=['POST', 'GET'])
def addtsk():
    if request.method == 'POST':
        try:
            nm = request.form['Name']
            dscp = request.form['Description']
            dd = request.form['DueDate']
            pr = request.form['Priority']
            with sql.connect("task_Manager.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO Tasks (Name,Description,CreationDate,DueDate,Priority) VALUES (?,?,?,?,?)",
                            (nm, dscp, date.today(), dd, pr))

                con.commit()

        except:
            con.rollback()

        finally:
            con.close()
            return render_template('index.html')


@app.route('/listtask', methods=['GET'])
def listtask():
    con = sql.connect("task_Manager.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    if request.method == 'GET':
        cur.execute("SELECT Name, DueDate, Description, Priority FROM Tasks")

        rows = cur.fetchall()

        return render_template("listTasks.html", rows=rows)

    else:
        return "This route only accepts GET requests."


@app.route('/deletetask', methods=['POST', 'GET'])
def deletetask():
    con = sql.connect("task_Manager.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT Name FROM Tasks")

    rows = cur.fetchall()

    return render_template("deleteTask.html", rows=rows)


@app.route('/updatetask', methods=['POST', 'GET'])
def updatetask():
    con = sql.connect("task_Manager.db")
    con.row_factory = sql.Row
    cur = con.cursor()

    cur.execute("SELECT Name FROM Tasks")

    rows = cur.fetchall()

    return render_template("updateTask.html", rows=rows)

@app.route('/updatingtask', methods=['POST', 'GET'])
def updatingtsk():
    if request.method == 'POST':
        try:
            # noinspection PyUnresolvedReferences
            nm = request.form.get('Name')
            with sql.connect("task_Manager.db") as con:
                cur = con.cursor()
                cur.execute("DELETE FROM Tasks WHERE Name = ?", (nm,))
                con.commit()

        except:
            con.rollback()

        finally:
            return render_template('updateThisTask.html')

@app.route('/deletingtask', methods=['POST', 'GET'])
def deletingtsk():
    if request.method == 'POST':
        try:
            nm = request.form.getlist('Name')
            with sql.connect("task_Manager.db") as con:
                cur = con.cursor()
                for taskName in nm:
                    cur.execute("DELETE FROM Tasks WHERE Name = ?", (taskName,))
                con.commit()

        except:
            con.rollback()

        finally:
            return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
