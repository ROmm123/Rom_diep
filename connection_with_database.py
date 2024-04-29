import mysql.connector


# Connect to MySQL database
def insert_to_database():      #todo //insert quary + sign in script
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Host address
        port='3306',  # Port number
        user='root',
        password='1234',
        database="game_database"
    )


def handle_data_forLogin(username, password):
    conn = mysql.connector.connect(
        host='127.0.0.1',  # Host address
        port='3306',  # Port number
        user='root',
        password='1234',
        database="game_database"
    )

    if conn.is_connected():
        print('Connected to the database')

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Define a function to perform the login operation

        # Perform login check here (e.g., check against the database)
        query = "SELECT * FROM data WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        result = cursor.fetchone()

        if result:
            print("Login successful!")
            print(result)
        else:
            print("Invalid username or password. Please try again.")

        # Close the cursor and connection
        cursor.close()
        conn.close()
        print('Connection closed')
    else:
        print('Failed to connect to MySQL database')
