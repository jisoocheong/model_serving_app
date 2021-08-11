import psycopg2
from fastapi import File, UploadFile
from typing import List
from .creators import global_config, create_model_serving_db, create_model_table
from .schemas import Model


def add_model(username: str, framework: str, name: str, version: str, device_dep: list, description: str, tags: list, input: str, output: str, test_code: UploadFile = File(...), screenshot: List[UploadFile] = File(...), model_file: UploadFile = File(...)):
    """
    Adds the given model to the model_table. 
    Returns true if the model is successfully added, false otherwise
    """

    import zipfile
    # Creates db and table if those don't already exist
    create_model_serving_db()
    create_model_table()

    # connect to database and get user
    host = global_config.database_host
    port = global_config.database_port

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    result = False
   
    # Get blobs of screenshots
    blobs_str = "["
    for img in screenshot:
        try:
            drawing = img.file.read()
            blob = psycopg2.Binary(drawing)
            blobs_str = blobs_str + f"{blob},"
        except Exception as error:
            print(error)
            return result 
    
    blobs_str = blobs_str[:-1] + "]"


    # check if name and version already exists
    cursor.execute(f'''SELECT * FROM model_table WHERE name = '{name}' AND version = '{version}';''')
    existing_models = cursor.fetchall()

    if len(existing_models) == 0:
        # model file
        model_content = model_file.file.read()
        size = len(model_content)
        size = round (size/1000000, 4)
        model_blob = psycopg2.Binary(model_content)

        # test code file
        test_code_content = test_code.file.read()
        test_blob = psycopg2.Binary(test_code_content)



        # add model to the db
        cursor.execute('''SELECT id FROM model_table ORDER BY id DESC LIMIT 1;''')
        highest_id = cursor.fetchone()
        highest_id = 0 if highest_id is None else int(highest_id[0])
        cursor.execute('''INSERT INTO model_table(id, adder_username, framework, name,''' + \
                ''' version, size, device_dependency, description, tags, input, output, test_code, screenshot, model_files) ''' + \
                        f'''VALUES ({highest_id + 1}, '{username}', '{framework}', '{name}', '{version}', '{size}' ''' + \
                        f''', ARRAY{device_dep}, '{description}', ARRAY{tags}, '{input}', '{output}', ''' + \
                        f'''{test_blob}, ARRAY{blobs_str}, {model_blob});''')
        result = True


    if result:
        print("Successfully added a new model")

    # Close the connection
    conn.close()
    return result



def search_model(search :str):
    """
    This will give a list of models that have the same or similar name as the given search term
    """

    # connect to database and get user
    host = global_config.database_host
    port = global_config.database_port

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f'''SELECT id, name, version, framework, tags, description FROM model_table WHERE LOWER(name) LIKE LOWER('{search}%');''')

    searched_models = cursor.fetchall()
    conn.close()

    return searched_models 


def get_model(name: str, version: str) :
    """
    Returns the model according to the given name and version 
    """
    import base64
    # connect to database and get user
    host = global_config.database_host
    port = global_config.database_port

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f'''SELECT * FROM model_table WHERE name = '{name}' AND version = '{version}';''')
    model = cursor.fetchone()
    print(model)
    result_model = None
    if model is not None:

        # converting screenshots to base64
        base64_imgs = []
        for img in model[12]:
            base64_imgs.append(base64.b64encode(img).decode("utf-8"))

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
        test_code=f'{model[11]}',
        screenshot=base64_imgs,
        model_files= f'{model[13]}'
            )

    return result_model 


def show_img_by_id(id : int):
    """
    reads blob data of the model with the matching id from the model_table
    Returns the number of images in this model
    """
    import io
    import PIL.Image as Image

    # connect to database and get user
    host = global_config.database_host
    port = global_config.database_port

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    # Add row with new model
    cursor.execute(f'''SELECT name, screenshot FROM model_table WHERE id = {id};''')
    pics = cursor.fetchall()[0]

    for i in range(len(pics[1])):
        open(f"{pics[0]}_{i}.jpeg", 'wb').write(pics[1][i])
    conn.close()
        

    return len(pics[1])


def get_first_img(id: int):
    """
    Returns the path to the image
    """
    # connect to database and get user
    host = global_config.database_host
    port = global_config.database_port

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    # Add row with new model
    cursor.execute(f'''SELECT name, screenshot FROM model_table WHERE id = {id};''')
    pics = cursor.fetchall()[0]

    conn.close()
    open(f"{pics[0]}.jpeg", 'wb').write(pics[1][0])
    return f"{pics[0]}.jpeg"


def remove_model(name: str, version: str):
    """
    Removes the model from model_table given the name and version
    """
    # connect to database and get user
    host = global_config.database_host
    port = global_config.database_port

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f'''DELETE FROM model_table WHERE name = '{name}' AND version = '{version}';''')
        
    conn.close()


def edit_model(id: int, changes: dict):
    """
    Makes changes to model 'id'. The changes dictionary must have keys of 
    column name and values of the new change
    """

    # connect to database and get user
    host = global_config.database_host
    port = global_config.database_port

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    
    cursor.execute(f'''SELECT * FROM model_table WHERE id = {id};''')
    model = cursor.fetchone()

    for col_name in changes:
        if col_name == "model_files":
            remove_model(model[3], model[4])
            add_model(model[1], model[2], model[3], model[4], model[6], model[7], model[8], model[9], model[10], model[11], model[12], changes[col_name])
        elif col_name == "screenshot":
            remove_model(model[3], model[4])
            add_model(model[1], model[2], model[3], model[4], model[6], model[7], model[8], model[9], model[10], model[11], changes[col_name], model[13])

        elif type(changes[col_name]) == str:
            cursor.execute(f'''UPDATE model_table SET {col_name} = '{changes[col_name]}' WHERE id = {id};''')
        elif type(changes[col_name]) == list:
            cursor.execute(f'''UPDATE model_table SET {col_name} = ARRAY{changes[col_name]} WHERE id = {id};''')
        else:
            cursor.execute(f'''UPDATE model_table SET {col_name} = {changes[col_name]} WHERE id = {id};''')
     
    conn.close()




