FROM locustio/locust

#RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install locust-plugins

RUN ln -s /home/locust_test/chromedriver  /usr/bin/

