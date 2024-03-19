import mysql.connector

def ping_database():
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="cop4521-2.c5w0oqowm22h.us-east-1.rds.amazonaws.com",
            port="3306",
            user="admin",
            password="masterpassword"
        )
        
        if connection.is_connected():
            print("Successfully connected to the database.")
            # Execute a simple query to ping the database
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("Ping result:", result)
    except mysql.connector.Error as error:
        print("Error connecting to the database:", error)
    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    ping_database()