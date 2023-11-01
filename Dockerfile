# 
FROM python:3.9

# 
WORKDIR /code

# 
RUN python -m venv venv

RUN .\env_name\Scripts\activate

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./app /code/app

# 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
