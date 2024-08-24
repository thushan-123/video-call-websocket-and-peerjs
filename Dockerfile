FROM python:3.11

# set the working dir in the container to app

WORKDIR /app

# copy requirment.txt  file from the local dir to /app dir

COPY requirements.txt .

# install the python dependencies

RUN pip install  -r requirements.txt

# copy another files to /app dir

COPY . /app


# start the uvicorn cmd

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
