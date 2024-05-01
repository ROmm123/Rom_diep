import mysql.connector


# Connect to MySQL database
def handle_data_for_signin(username, password):
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',  # Host address
            port='3306',  # Port number
            user='root',
            password='1234',
            database="game_database"
        )

        if conn.is_connected():
            print('Connected to the database')

            cursor = conn.cursor()

            # Perform signin check here (adding username and password to the database)
            query_for_insert = "INSERT INTO data (username, password) VALUES (%s, %s)"
            cursor.execute(query_for_insert, (username, password))

            # Commit the transaction to apply the changes
            conn.commit()

            print("Sign-in successful!")

            # Close the cursor and connection
            cursor.close()
            conn.close()
            print('Connection closed')
        else:
            print('Failed to connect to MySQL database')

    except mysql.connector.Error as e:
        print(f"Error: {e}")


def handle_data_forLogin(username, password):
    try:
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

            # Perform login check here (e.g., check against the database)
            query = "SELECT * FROM data WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                print("Login successful!")
                print(result)
                # Delete the record from the 'data' table
                delete_query = "DELETE FROM data WHERE username = %s AND password = %s"
                cursor.execute(delete_query, (username, password))
                conn.commit()  # Commit changes after delete
                print("Record removed from database.")
            else:
                print("Invalid username or password. Please try again.")

            # Close the cursor and connection
            cursor.close()
            conn.close()
            print('Connection closed')
        else:
            print('Failed to connect to MySQL database')

    except mysql.connector.Error as e:
        print(f"Error: {e}")
