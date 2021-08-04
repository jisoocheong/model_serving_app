import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from app.model_serving_db.creators import *
#from creators import *

def add_user(username: str, email: str, password: str):
    """
    Adds the given user to the user_table. 
    Returns true if the user is successfully added, false otherwise
    """
    # Creates db and table if those don't already exist
    create_model_serving_db()
    create_user_table()


    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host="127.0.0.1", port="5432")
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()


    result = False
    # Add row with new user if it doesnt already exists
    pass_hash = generate_password_hash(password)
    cursor.execute('''SELECT id FROM user_table ORDER BY id DESC LIMIT 1;''')
    highest_id = cursor.fetchone()
    highest_id = 0 if highest_id is None else int(highest_id[0])

    cursor.execute(f'''SELECT * FROM user_table WHERE username = '{username}' OR email = '{email}';''')
    existing_user = cursor.fetchone()
    if existing_user is None:
        result = True 
        cursor.execute(f'''INSERT INTO user_table(id, username, email, password_hash, logged_in) VALUES ({highest_id + 1}, '{username}', '{email}', '{pass_hash}', true);''')
        print("Successfully added a new user")


    # Close the connection
    conn.close()
    return result



def check_valid_login(username: str, password: str):
    """
    Returns true if given the right username and password, false otherwise 
    """
        
    # Creates db and table if those don't already exist
    create_model_serving_db()
    create_user_table()


    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host="127.0.0.1", port="5432")
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()


    # Get row of the user
    cursor.execute(f'''SELECT * FROM user_table WHERE username = '{username}';''')
    existing_user = cursor.fetchone()
    if existing_user is None:
        print("Not a valid username")
        return False

    pass_hash = existing_user[3]
    result = check_password_hash(pass_hash, password)

    if result:
        print("Successful Login")
    else:
        print("Wrong password")
    return result















