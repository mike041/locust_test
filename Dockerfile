FROM locustio/locust

#RUN /usr/local/bin/python -m pip install --upgrade pip
ADD ./  /home/locust_test/
RUN pip install locust-plugins

RUN sudo ln -s /home/locust_test/chromedriver  /usr/bin/

