FROM tiangolo/uwsgi-nginx-flask:python3.6
COPY . /app
WORKDIR /app
ENV PYTHONUNBUFFERED 1
RUN pip3 install --disable-pip-version-check -r /app/requirements.txt
