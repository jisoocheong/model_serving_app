from user_table import *
from model_table import *
import psycopg2

add_user("jisoo", "jc@nc.com", "some pass")
print(add_model("jisoo", "tensorflow", "stylegan2", ["anime", "toonify"], "various sizes", ['GPU'], "description", ["image generation", "face"], "latents:[None, 512] float32", "Base64 encoded RGB images: [None,] String", "some test code", ["img/cat.jpeg", "img/pikachu.png"])) 
    


