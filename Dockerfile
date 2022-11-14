FROM locustio/locust

#RUN /usr/local/bin/python -m pip install --upgrade pip
ADD ./  /home/locust_test/
RUN pip install locust-plugins
#安装sudo
RUN yum install sudo -y

RUN sudo ln -s /home/locust_test/chromedriver  /usr/bin/

