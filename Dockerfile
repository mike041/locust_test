FROM locustio/locust

#RUN /usr/local/bin/python -m pip install --upgrade pip
ADD ./  /home/locust_test/

WORKDIR /home/locust_test/

RUN pip install -r requirements.txt

#RUN sudo ln -s /home/locust_test/chromedriver  /usr/bin/

