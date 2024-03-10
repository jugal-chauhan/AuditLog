AWS EC2 connection success

Commands : 

sudo yum update -y

sudo amazon-linux-extras install docker 

sudo service docker start

sudo usermod -a -G docker ec2-user

pwd

mkdir auditlog

cd auditlog

pwd (returns : /home/ec2-user/auditlog)

(upload pim file)

chmod 600 flask-app-ec2-key.pem

scp -i flask-app-ec2-key.pem Dockerfile docker-compose.yml app.py app_database.py requirements.txt ec2-user@3.145.12.117:/home/ec2-user/auditlog

(upload successful, go back to EC2)

sudo docker build -t ec2-flask:v2.0 -f Dockerfile .

sudo docker images

sudo docker run -d -p 80:5001 ec2-flask:v1.0 

# past public IP address to check


sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
