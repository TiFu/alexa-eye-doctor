scp -r -i ~/.ssh/key.pem ./server/ ubuntu@ec2-34-244-32-53.eu-west-1.compute.amazonaws.com:/home/ubuntu/

scp -r -i ~/.ssh/key.pem ./doctor-frontend ubuntu@ec2-34-244-32-53.eu-west-1.compute.amazonaws.com:/home/ubuntu/server/public/

scp -r -i ~/.ssh/key.pem ./patient-frontend/ ubuntu@ec2-34-244-32-53.eu-west-1.compute.amazonaws.com:/home/ubuntu/server/public/

