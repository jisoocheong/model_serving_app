import psycopg2
from app.model_serving_db.creators import *
#from creators import *

def add_model(username: str, framework: str, name: str, version: list, size: str, device_dep: list, description: str, tags: list, input: str, output: str, test_code: str, screenshot: list):
    """
    Adds the given model to the model_table. 
    Note that the screenshots will be a list of the path to file of the image
    Returns true if the model is successfully added, false otherwise
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


    # Get blobs of screenshots
    blobs_str = "["
    for img in screenshot:
        try:
            drawing = open(img, 'rb').read()
            blob = psycopg2.Binary(drawing)
            blobs_str = blobs_str + f"{blob},"
        except Exception as error:
            return result 
    
    blobs_str = blobs_str[:-1] + "]"

    cursor.execute(f'''SELECT * FROM model_table WHERE name = '{name}';''')
    existing_model = cursor.fetchone()
    if existing_model is None:
        result = True
        cursor.execute('''INSERT INTO model_table(id, adder_username, framework, name,''' + \
                ''' version, size, device_dependency, description, tags, input, output, test_code, screenshot) ''' + \
                        f'''VALUES ({highest_id + 1}, '{username}', '{framework}', '{name}', ARRAY{version}, '{size}' ''' + \
                        f''', ARRAY{device_dep}, '{description}', ARRAY{tags}, '{input}', '{output}', ''' + \
                        f''''{test_code}', ARRAY{blobs_str});''')
         
        print("Successfully added a new model")

    # Close the connection
    conn.close()
    return result



