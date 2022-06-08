# secrets.tfvars

db_username    = "db_username"
db_password    = "db_password"
my_ip          = "your_local_ip"
aws_access_key = "your_aws_access_key"
aws_secret_key = "your_aws_secret_key"

# for create key pair used cmd:
ssh-keygen -t rsa -b 4096 -m pem -f name_kp && openssl rsa -in name_kp -outform pem && chmod 400 name_kp &&
mv name_kp name_kp.pem
