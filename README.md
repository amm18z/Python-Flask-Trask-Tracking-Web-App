# COP4521-Group-Project
## Description
A simple task tracker web application that allows users to perform CRUD operations on tasks. Users should be able to add, view, edit, and delete tasks. With additional features such as: task prioritization, categorization, , due dates, Google Calendar support, and a viewable calendar. This app supports 3 roles: Free, Premium, and Admin.
## Libraries Used By This Project
* datetime: used to get the current date time in order to save the moment that a task is created
* flask: used to create a flask application for our application
* mysql.connector: used to connect the python program to the mysql database
* contextlib: used because mysql.connector does not natively support context manager switching and the closing function of this library helps close the connection without issues
* hashlib:
* os:
