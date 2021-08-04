import psycopg2

from app.config import settings
from app.security import get_password_hash
from .schemas import UserInDB
from .creators import create_model_serving_db, create_user_table


def get_user(username: str):
    # Creates db and table if those don't already exist
    create_model_serving_db()
    create_user_table()

    # connect to database and get user
    host="127.0.0.1"
    port="5432"
    print(settings)
    #host = settings.database_host
    #port = settings.database_port
    
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f'''SELECT * FROM user_table WHERE username = '{username}';''')

    existing_user = cursor.fetchone()

    # Close the connection
    conn.close()

    # return user
    return UserInDB(
        username=existing_user[1],
        email=existing_user[2], 
        hashed_password=existing_user[3])


def create_user(username: str, email: str, password: str):
    # Creates db and table if those don't already exist
    create_model_serving_db()
    create_user_table()


    # connect to database and get user
    host = settings.database_host
    port = settings.database_port
    
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    # Add row with new user if it doesnt already exists
    hashed_password = get_password_hash(password)
    cursor.execute('''SELECT id FROM user_table ORDER BY id DESC LIMIT 1;''')
    highest_id = cursor.fetchone()
    highest_id = 0 if highest_id is None else int(highest_id[0])

    cursor.execute(f'''SELECT * FROM user_table WHERE username = '{username}' OR email = '{email}';''')
    existing_user = cursor.fetchone()
    if existing_user is None:
        cursor.execute(f'''INSERT INTO user_table(id, username, email, password_hash, logged_in) VALUES ({highest_id + 1}, '{username}', '{email}', '{hashed_password}', true);''')
        print("Successfully added a new user")

    existing_user = cursor.fetchone()
    
    # Close the connection
    conn.close()

    # return user
    return UserInDB(
        username=existing_user[1],
        email=existing_user[2],
        hashed_password=existing_user[3])
