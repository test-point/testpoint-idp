FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD src /code/
ADD requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

RUN python manage.py collectstatic --noinput

CMD ["/bin/bash","/code/docker-gunicorn.sh"]
