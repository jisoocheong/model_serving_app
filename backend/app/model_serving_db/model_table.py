import psycopg2

from .creators import global_config, create_model_serving_db, create_model_table
from .schemas import Model


def add_model(username: str, framework: str, name: str, version: list, size: str, device_dep: list, description: str, tags: list, input: str, output: str, test_code: str, screenshot: list, model_files: list):
    """
    Adds the given model to the model_table. 
    Note that the screenshots will be a list of the path to file of the image
    Returns true if the model is successfully added, false otherwise
    """


    def _get_version_zip(version: str):
        """
        Helper method to return the path of where the version's zip file is  
        """

        for zip_file in model_files:
            if zip_file[-len(version)-4:-4] == version:
                return zip_file




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
            drawing = open(img, 'rb').read()
            blob = psycopg2.Binary(drawing)
            blobs_str = blobs_str + f"{blob},"
        except Exception as error:
            print(error)
            return result 
    
    blobs_str = blobs_str[:-1] + "]"


    # Get blobs of model_files
    model_str = "["
    for model_file in model_files:
        try:
            f = open(model_file, 'rb').read()
            blob = psycopg2.Binary(f)
            model_str = model_str + f"{blob},"
        except Exception as error:
            print(error)
            return result 
    
    model_str = model_str[:-1] + "]"


    for ver in version:
        # check if name and version already exists
        cursor.execute(f'''SELECT * FROM model_table WHERE name = '{name}' AND version = '{ver}';''')
        existing_models = cursor.fetchall()

        if len(existing_models) == 0:

            # get size of model file for that version

            size = 0
            filename = _get_version_zip(ver)
            if filename is None:
                print("file for version " + ver + " was not found")
                continue 
            zip_obj = zipfile.ZipFile(filename, "r")
            name_list = zip_obj.namelist()
            zf = zipfile.ZipFile(filename)
            for content in name_list:
                info = zf.getinfo(content)
                size += info.file_size

            size = round (size/ 1000000, 4)
            #close the file object
            zip_obj.close()
            zf.close()

            # add model to the db
            cursor.execute('''SELECT id FROM model_table ORDER BY id DESC LIMIT 1;''')
            highest_id = cursor.fetchone()
            highest_id = 0 if highest_id is None else int(highest_id[0])
            cursor.execute('''INSERT INTO model_table(id, adder_username, framework, name,''' + \
                ''' version, size, device_dependency, description, tags, input, output, test_code, screenshot, model_files) ''' + \
                        f'''VALUES ({highest_id + 1}, '{username}', '{framework}', '{name}', '{ver}', '{size}' ''' + \
                        f''', ARRAY{device_dep}, '{description}', ARRAY{tags}, '{input}', '{output}', ''' + \
                        f''''{test_code}', ARRAY{blobs_str}, ARRAY{model_str});''')


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
    cursor.execute(f'''SELECT id, name, version, framework, tags FROM model_table WHERE LOWER(name) = LOWER('{search}');''')

    searched_models = cursor.fetchall()
    conn.close()

    return searched_models 


def get_model_by_id(id: int) :
    """
    Returns the model according to the given id number 
    """
    import base64
    
    # connect to database and get user
    host = global_config.database_host
    port = global_config.database_port

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(f'''SELECT * FROM model_table WHERE id = {id};''')
    model = cursor.fetchone()
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
        test_code=model[11],
        screenshot=base64_imgs,
        model_files=model[13]
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

