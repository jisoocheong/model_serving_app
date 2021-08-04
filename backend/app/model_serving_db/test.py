#from user_table import *
#from model_table import *
import psycopg2
import io

import PIL.Image as Image

#add_user("jisoo", "jc@nc.com", "some pass")
#print(add_model("jisoo", "tensorflow", "stylegan2", ["anime", "toonify"], "various sizes", ['GPU'], "description", ["image generation", "face"], "latents:[None, 512] float32", "Base64 encoded RGB images: [None,] String", "some test code", ["img/cat.jpeg", "img/pikachu.png"])) 
    

#from creators import *

def show_img(name: str):
    """
    reads blob data from the model_table
    """
    # Creates db and table if those don't already exist

    # Establishing the connection
    conn = psycopg2.connect(database="model_serving_db", user="postgres", password="password", host="127.0.0.1", port="5432")
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Add row with new model
    cursor.execute('''SELECT screenshot FROM model_table;''')
    pic = cursor.fetchone()[0]

    print((pic[0]))
    open("img/new_img.jpeg", 'wb').write(pic[0])


    #bytearray(first_pic)
    #Bimage = Image.open(io.BytesIO(bytearray(first_pic)))
    conn.close()
    #return image
        
show_img("name")
