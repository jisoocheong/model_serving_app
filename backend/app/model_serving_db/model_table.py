import psycopg2
from app.model_serving_db.creators import *

def add_model(framework: str, name: str, version: list, size: str, device_dep: list, description: str, tags: list, input: str, output: str, test_code: str, screenshot: list):
    """
    Adds the given model to the model_table. 
    """
    # Creates db and table if those don't already exist
    create_model_serving_db()
    create_model_table()


    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host="127.0.0.1", port="5432")
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()


    result = False
    # Add row with new model
    cursor.execute('''SELECT id FROM model_table ORDER BY id DESC LIMIT 1;''')
    highest_id = cursor.fetchone()
    highest_id = 0 if highest_id is None else int(highest_id[0])

    cursor.execute(f'''INSERT INTO model_table(id, framework, name, version, size, device_dep, description, tags, input, output, test_code, screenshot) VALUES ({highest_id + 1}, '{framework}', '{name}', '{version}', '{size}', '{device_dep}', '{description}', '{tags}', '{input}', '{output}', '{test_code}', '{screenshot}');''')
        print("Successfully added a new model")

    # Close the connection
    conn.close()



