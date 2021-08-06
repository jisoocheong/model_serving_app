import psycopg2
from app.config import settings
from app.model_serving_db.creators import *
from app.model_serving_db.schemas import Model
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

    # connect to database and get user
    host = settings.database_host
    port = settings.database_port

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
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
            print(error)
            return result 
    
    blobs_str = blobs_str[:-1] + "]"


    cursor.execute(f'''SELECT * FROM model_table WHERE name = '{name}';''')
    existing_models = cursor.fetchall()

    
    # checking versions
    for model in existing_models:
        model_version = model[4]
        if set(model_version) == set(version):
            conn.close() 
            return result

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




def search_model(search :str):
    """
    This will give a list of models that have the same or similar name as the given search term
    """

    # connect to database and get user
    host = settings.database_host
    port = settings.database_port

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f'''SELECT id, name, version, framework, tags FROM model_table WHERE LOWER(name) = LOWER('{search}');''')

    searched_models = cursor.fetchall()
    conn.close()

    return searched_models 


def get_model_by_id(id: int) :
    """
    Returns the model according to the given id number 
    """

    
    # connect to database and get user
    host = settings.database_host
    port = settings.database_port

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f'''SELECT * FROM model_table WHERE id = {id};''')
    model = cursor.fetchone()
#    print(type(model))
#    print(model)
    result_model = None
    if model is not None:

        result_model = Model(
        username=model[1],
        framework=model[2],
        name=model[3],
        version=model[4],
        size=model[5],
        device_dep=model[6],
        description=model[7],
        tags=model[8],
        input=model[9],
        output=model[10],
        test_code=model[11],
        screenshot=model[12]
            )



#    print(result_model)
    return result_model 

    """
    return Model(
        username=model[1],
        framework=model[2],
        name=model[3],
        version=model[4],
        size=model[5],
        device_dep=model[6],
        description=model[7],
        tags=model[8],
        input=model[9],
        output=model[10],
        test_code=model[11],
        screenshot=model[12]
            )

"""





import psycopg2
import io

import PIL.Image as Image

    


def show_img_by_id(id : int):
    """
    reads blob data of the model with the matching id from the model_table
    Returns the number of images in this model
    """
    # connect to database and get user
    host = settings.database_host
    port = settings.database_port


    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Add row with new model
    cursor.execute(f'''SELECT name, screenshot FROM model_table WHERE id = {id};''')
    pics = cursor.fetchall()[0]

    print(pics)
    #open(f"{pics[0]}.jpeg", 'wb').write(pics[1][0])


    for i in range(len(pics[1])):
        open(f"{pics[0]}_{i}.jpeg", 'wb').write(pics[1][i])




    conn.close()
        

    return len(pics[1])


