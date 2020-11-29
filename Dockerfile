FROM python
COPY requirements.txt . 
RUN  pip3 install -r requirements.txt
ADD demo.tar.gz /
ENV port=8888
RUN  sed -i '146 s/decode/encode/g' /usr/local/lib/python3.9/site-packages/django/db/backends/mysql/operations.py
CMD python manage.py runserver 0.0.0.0:${port} 

