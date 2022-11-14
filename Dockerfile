FROM centos:7

ADD ./chromedriver /home/locust_test/
ADD ./Python-3.8.8.tar.xz /home/locust_test/
ADD ./google-chrome.repo /home/locust_test/

WORKDIR /home/locust_test
RUN yum install java-11-openjdk-devel.x86_64 -y
RUN cd /home/locust_test && echo $PWD
RUN ls -al
RUN mv  ./google-chrome.repo /etc/yum.repos.d/google-chrome.repo

RUN yum -y install google-chrome-stable --nogpgcheck

#安装python3.8.8
RUN yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make -y


RUN Python-3.8.8/configure prefix=/usr/local/python3 && make && make install && rm -rf ./Python-3.8.8


RUN ln -s /usr/local/python3/bin/python3 /usr/bin/python3
RUN ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
RUN /usr/local/python3/bin/python3.8 -m pip install --upgrade pip


#安装chrome_driver
RUN ln -s /home/locust_test/chromedriver  /usr/bin/

RUN pip3 install -r  requirements.txt


CMD ["/bin/bash"]
