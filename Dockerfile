# set base image
FROM python:3.8

LABEL maintainer="juyoung.kim517@gmail.com"

# set the working directory in the container
WORKDIR /project

# Copy requirement files and install dependencies. Use build cache to avoid reinstalling dependencies.
COPY requirements.txt requirements.txt

RUN pip install -r ./requirements.txt --ignore-installed

# Copy project
COPY . .

RUN pip install -r ./requirements.txt

# command to run on container start
CMD [ "python", "app.py" ]
