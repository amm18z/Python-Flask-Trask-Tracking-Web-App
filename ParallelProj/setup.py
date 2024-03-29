"""3/27/2024 The program in this file is the work of Aidan McGill, Judas McCall Smith, and Rafael Cardoso"""

import mysql.connector as msc

def setup_database():
    try:
        # Connect to the database
        conn = msc.connect(
            host="cop4521-2.c5w0oqowm22h.us-east-1.rds.amazonaws.com",
            port="3306",
            user="admin",
            password="masterpassword"
        )
        
        if conn.is_connected():
            print("Successfully connected to the database.")
            # Execute a simple query to ping the database
            cur = conn.cursor()

            cur.execute("USE TaskTracker")

            cur.execute("CREATE TABLE IF NOT EXISTS Users ("
                        "Id INT AUTO_INCREMENT PRIMARY KEY,"
                        "UserName VARCHAR(20),"
                        "PasswordHash VARCHAR(500),"
                        "Salt VARCHAR(100),"
                        "CONSTRAINT username_unique UNIQUE (UserName) )")
            print('Created table Users')

            cur.execute("CREATE TABLE IF NOT EXISTS Tasks ("
                        "Id INT AUTO_INCREMENT PRIMARY KEY,"
                        "Name VARCHAR(100),"
                        "Description VARCHAR(200),"
                        "CreationDate DATE,"
                        "DueDate DATE,"
                        "Priority INT,"
                        "User_id INT,"
                        "FOREIGN KEY(User_id) REFERENCES Users(Id) )")
            print('Created table Tasks')

            cur.execute("CREATE TABLE IF NOT EXISTS Assignments ("
                        "Id INT AUTO_INCREMENT PRIMARY KEY,"
                        "User_id INT, Task_id INT,"
                        "FOREIGN KEY(User_id) REFERENCES Users(Id) )")
            print('Created table Assignments')

            cur.execute("CREATE ROLE IF NOT EXISTS FreeUserRole")
            cur.execute("GRANT SELECT, INSERT ON TaskTracker.Tasks TO FreeUserRole")

            cur.execute("CREATE ROLE IF NOT EXISTS PremiumUserRole")
            cur.execute("GRANT SELECT, INSERT, UPDATE, DELETE ON TaskTracker.Tasks TO PremiumUserRole")

            cur.execute("CREATE ROLE IF NOT EXISTS AdministratorRole")
            cur.execute("GRANT ALL PRIVILEGES ON TaskTracker.* TO AdministratorRole")

            conn.commit()

    except msc.Error as error:
        print("Error connecting to the database:", error)
    finally:
        # Close the database connection
        if conn.is_connected():
            cur.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    setup_database()