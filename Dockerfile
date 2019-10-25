FROM tiangolo/uwsgi-nginx-flask
COPY setup.py /app
COPY create_mock.py /app
COPY alembic.ini /app
COPY uwsgi-me.sh /app
COPY /migrations /app/migrations
COPY /cebulany /app/cebulany
WORKDIR /app
RUN python setup.py install
EXPOSE 5000
RUN alembic upgrade head
RUN python create_mock.py > mock.csv
CMD ./uwsgi-me.sh