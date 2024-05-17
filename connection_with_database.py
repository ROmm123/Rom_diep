import mysql.connector
import queue
import threading
import time
import os
import logging


def handle_data_for_signin(username, password):
    try:

        # Connect to MySQL database
        conn = mysql.connector.connect(
            host='127.0.0.1',  # host address
            port='3306',  # port number
            user='root',
            password='1234',
            database="datab"

        )

        if conn.is_connected():
            print('Connected to the database',flush=True)

            cursor = conn.cursor()

            query = "SELECT * FROM data WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if not result:
                # Perform signin check here (adding username and password to the database)
                query_for_insert = "INSERT INTO data (username, password) VALUES (%s, %s)"
                cursor.execute(query_for_insert, (username, password))

                # Commit the transaction to apply the changes
                conn.commit()

                print("Sign-in successful!", flush=True)
            else:
                print("this name is already taken try another..",flush=True)

            # Close the cursor and connection
            cursor.close()
            conn.close()
            print('Connection closed',flush=True)

        else:
            print('Failed to connect to MySQL database')

    except mysql.connector.Error as e:
        print(f"Error: {e}",flush=True)


def handle_data_forLogin(username, password):
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',  # host address
            port='3306',  # port number
            user='root',
            password='1234',
            database="datab"

        )

        if conn.is_connected():
            print('Connected to the database', flush=True)

            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()
            # Perform login check here (e.g., check against the database)
            query = "SELECT * FROM data WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                print("Login successful!")
                print(result)
                if result[11] == 0 or result[11] == None:
                    # Delete the record from the 'data' table
                    update_state_query = "UPDATE data SET state = 1 WHERE username = %s AND password = %s"
                    cursor.execute(update_state_query, (username, password))
                    conn.commit()
                    print("State updated ",flush=True)
                else:
                    print("user in game",flush=True)
                    result = None
            else:
                print("Invalid username or password. Please try again.",flush=True)

            # Close the cursor and connection
            cursor.close()
            conn.close()
            print('Connection closed',flush=True)
            return result
        else:
            print('Failed to connect to MySQL database',flush=True)

    except mysql.connector.Error as e:
        print(f"Error: {e}",flush=True)


def handle_data_for_logout(x, y, speedCounter, sizeCounter, shieldCounter, HPCounter_60,
                           HPCounter_30, HPCounter_15, HPCounter_5 , username, password):
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',  # host address
            port='3306',  # port number
            user='root',
            password='1234',
            database="datab"

        )

        if conn.is_connected():
            print('Connected to the database',flush=True)

            cursor = conn.cursor()

            query_for_insert = "UPDATE data set x = %s , y = %s , speed_counter = %s , size_counter = %s , shield_counter = %s , hp_counter_60 = %s,  hp_counter_30 = %s , hp_counter_15 = %s , hp_counter_5 = %s , state = 0 WHERE username = %s and password = %s "
            cursor.execute(query_for_insert,
                           (x, y, speedCounter, sizeCounter, shieldCounter, HPCounter_60 , HPCounter_30 , HPCounter_15 ,HPCounter_5 , username, password))

            # commit the transaction to apply the changes
            conn.commit()

            print("Sign-out successful!",flush=True)

            # close the cursor and connection
            cursor.close()
            conn.close()
            print('Connection closed',flush=True)
        else:
            print('Failed to connect to MySQL database',flush=True)

    except mysql.connector.Error as e:
        print(f"Error: {e}",flush=True)