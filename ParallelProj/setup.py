"""2/21/2024 The program in this file is the individual work of Rafael Cardoso RDC21C"""

import sqlite3

conn = sqlite3.connect('task_Manager.db')
print('Opened database successfully')

conn.execute('CREATE TABLE Tasks (Id INTEGER PRIMARY KEY, Name VARCHAR(100), Description VARCHAR(200),'
             ' CreationDate DATE, DueDate DATE, Priority INT, User_id INT, FOREIGN KEY(User_id) REFERENCES Users(Id))')
print('Created table 1')

conn.execute('CREATE TABLE Users (Id INT, Password VARCHAR(30))')
print('Created table 2')

conn.execute('CREATE TABLE Assignments (Id INT, User_id INT, Task_id INT, FOREIGN KEY(User_id) REFERENCES Users(Id))')
print('Created table 3')

conn.close()
