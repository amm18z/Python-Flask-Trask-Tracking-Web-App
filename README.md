# COP4521-Group-Project
## Description
A simple task tracker web application that allows users to perform CRUD operations on tasks. Users should be able to add, view, edit, and delete tasks. With additional features such as: task prioritization, categorization, , due dates, Google Calendar support, and a viewable calendar. This app supports 3 roles: Free, Premium, and Admin.
## Libraries Used By This Project
* datetime: used to get the current date time in order to save the moment that a task is created
* flask: used to create a flask application for our application
* mysql.connector: used to connect the python program to the mysql database
* contextlib: used because mysql.connector does not natively support context manager switching and the closing function of this library helps close the connection without issues
* hashlib: used hashlib's sha256() hash function to produce password digest
* os: used os's urandom() function to cryptographically securely produce 16 bytes of random numbers for the salt
## Resources Used
* https://dev.mysql.com/doc/
* https://docs.python.org/3/library/contextlib.html
## Features
* Create, Read, Update, and Delete Tasks
* Add a Task to Google Calendar
* Create, Update, and Delete Categories of Tasks
* Viewable Calendar
## Division of Labor
### Stefano Sanidas
* Created the various HTML files used in the program, created the SQL Queries for the CRUD functionality, and created the Add Task to Google Calendar feature
### Aidan McGill
* Implemented User Authentication (pasword salting and hashing - login and createAccount html templates + relevant routing and logic code), worked on Role Based Access Control, and implemented Updating for tasks (U in CRUD).
### Judas McCall Smith
* Created and maintained the database via AWS, created the initial category.html page and backend, the debug page "alltables", and updated the database throughout to reflect changes. 
### Rafael Cardoso
* Created the overall CRUD structure for the application, established Role Based Access Control functionality for switching between roles and lightly assisted with the implementation of User Authentication. 
### Preston Byk
*
