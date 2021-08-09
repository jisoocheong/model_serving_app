import psycopg2

from config import settings as global_config


def create_model_serving_db():
    """
    Establishes a database for this model serving app 
    """
    host = global_config.database_host
    port = global_config.database_port

    # Establishing the connection
    conn = psycopg2.connect(database="postgres", user="postgres", password="password", host=host, port=port)
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
    return


def create_user_table():
    """
    Creates a table for users 
    """
    host = global_config.database_host
    port = global_config.database_port

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
    
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()


    # Creating a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_table(id INT PRIMARY KEY NOT NULL, username TEXT NOT NULL UNIQUE, email TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, logged_in BOOLEAN)''')


    # Close connection
    conn.close()
    return


def create_model_table():
    """
    Creates a table for users 
    """
    
    host = global_config.database_host
    port = global_config.database_port

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
    
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()


    # Creating a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS model_table(id INT PRIMARY KEY NOT NULL, ''' + \
            '''adder_username TEXT NOT NULL, ''' + \
            '''framework TEXT NOT NULL, ''' + \
            '''name TEXT NOT NULL, ''' + \
            '''version TEXT NOT NULL, ''' + \
            '''size TEXT NOT NULL, ''' + \
            '''device_dependency TEXT[] NOT NULL, ''' + \
            '''description TEXT NOT NULL, ''' + \
            '''tags TEXT[] NOT NULL, ''' + \
            '''input TEXT NOT NULL, ''' + \
            '''output TEXT NOT NULL, ''' + \
            '''test_code TEXT NOT NULL, ''' + \
            '''screenshot BYTEA[] NOT NULL, ''' + \
            '''model_files BYTEA NOT NULL''' + \
            ''' )''')


    # Close connection
    conn.close()
    return
