#一、压测完整部署步骤：
##1.安装docker
yum -y install docker
##2.编写测试脚本locustfile.py
##3.建立master镜像
sudo docker run -p 8089:8089 -p 5557:5557 -v $PWD/locustfile.py:/home/locust/locustfile.py locustio/locust -f /home/locust/locustfile.py --master
##4.建立8个worker镜像（注意每个镜像修改映射的物理机端口）
sudo docker run -p 8090:8090 -p 5558:5558 -d -v $PWD/locustfile.py:/home/locust/locustfile.py locustio/locust -f /home/locust/locustfile.py --worker --master-host=43.138.46.68 --master-port 5557

#通过docker-compose执行，启用一个master和4个worker，并自动执行

docker-compose up --scale worker=4
