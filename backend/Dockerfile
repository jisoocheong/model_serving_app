FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# NOTE: docker build context should be on ./backend

# install python requirements
RUN pip install --no-cache-dir \
    python-multipart \
    psycopg2 \
    python-jose[cryptography] \
    passlib[bcrypt] \
    aiofiles \ 
    pillow \
    pydantic[dotenv]

# copy sources
COPY ./app /app
WORKDIR /app

# run
EXPOSE 8000
CMD [ "uvicorn", "example_api:app", "--host=0.0.0.0", "--port=8000"]