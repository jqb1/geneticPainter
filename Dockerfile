FROM jjanzic/docker-python3-opencv

RUN pip install --upgrade pip

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV NAME genetic_painter

CMD ["python", "genetics.py", "-f", "mona_lisa.png"]
