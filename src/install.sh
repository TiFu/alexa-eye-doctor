scp -r -i ~/.ssh/key.pem ./server/ ubuntu@ec2-34-240-125-211.eu-west-1.compute.amazonaws.com:/home/ubuntu/

scp -r -i ~/.ssh/key.pem ./doctor-frontend/ ubuntu@ec2-34-240-125-211.eu-west-1.compute.amazonaws.com:/home/ubuntu/server/public/doctor-frontend/

scp -r -i ~/.ssh/key.pem ./patient-frontend/ ubuntu@ec2-34-240-125-211.eu-west-1.compute.amazonaws.com:/home/ubuntu/server/public/patient-frontend/

