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

3. Run the client-side React app in a different terminal window:

    ```sh
    $ cd frontend
    $ npm install
    $ npm start
    ```

    Navigate to [http://localhost:3000](http://localhost:3000)



