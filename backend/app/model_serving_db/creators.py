import psycopg2


def create_model_serving_db():
    """
    Establishes a database for this model serving app 
    """

    # Establishing the connection
    conn = psycopg2.connect(database="postgres", user="postgres", password="password", host="127.0.0.1", port="5432")
    conn.autocommit = True


    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()


    # Preparing  query to create a database if it doesn't already exist
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'model_serving_db'")
    exists = cursor.fetchone()
    sql = "RAISE NOTICE 'model_serving_db already exists'"
    if not exists:
        sql = '''CREATE DATABASE model_serving_db'''
        
        # Creating a database
        cursor.execute(sql)
        print("Database created successfully............")


    # Close connection
    conn.close()
        


def create_user_table():
    """
    Creates a table for users 
    """

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host="127.0.0.1", port = "5432")
    conn.autocommit = True
    
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()


    # Creating a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_table(id INT PRIMARY KEY NOT NULL, username TEXT NOT NULL UNIQUE, email TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, logged_in BOOLEAN)''')


    # Close connection
    conn.close()
    


def create_model_table():
    """
    Creates a table for users 
    """

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host="127.0.0.1", port = "5432")
    conn.autocommit = True
    
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()


    # Creating a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS model_table(id INT PRIMARY KEY NOT NULL)''')


    # Close connection
    conn.close()

