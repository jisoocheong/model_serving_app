# Model Serving App

This web app provides a platform for specific users to add, share, and edit ML models. 

## Code Setup

1. Run the server-side FastAPI app in one terminal window:

    ```sh
    $ cd backend
    $ python3.9 -m venv venv
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt
    (venv)$ python main.py
    ```

2. Starting up PostgreSQL:

    Navigate to [https://www.postgresql.org/download/] and select download depending on the OS

<!--  3. Run the client-side React app in a different terminal window:

    ```sh
    $ cd frontend
    $ npm install
    $ npm start
    ```

    Navigate to [http://localhost:3000](http://localhost:3000) -->


## Config

The environment variables are in the 'backend/app/.env_backend' and some can be tweaked


## Run with docker-compose

- Checkout the 'docker-compose.yml' for detailed configuration.

```bash
# if it needs to be built,
$ docker-compose up -d --build

# if it only needs to run
$ docker-compose up -d

```
- This will run the container for the backend side and the database
- Access the site at 'localhost:48000/docs'.  

## Connect to PostgreSQL Database Server

```sh
$ docker exec -it model_serving_app_database_1 /bin/bash
:/# psql -U postgres
```

- '\l' to list databases
- '\c' to connect to a database
- '\d' to list tables in the connected database

## Project Support and Development

This project has been developed as part of my internship at the [NCSOFT](http://global.ncsoft.com/global/) Vision AI Lab in summer 2021.




