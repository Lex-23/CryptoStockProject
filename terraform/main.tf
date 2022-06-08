terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  required_version = "~> 1.2.1"
}

provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_vpc" "cryptostock_vpc" {
  cidr_block           = var.vpc_cidr_block
  enable_dns_hostnames = true

  tags = {
    "Name" = "cryptostock_vpc"
  }
}

resource "aws_internet_gateway" "cryptostock_igw" {
  vpc_id = aws_vpc.cryptostock_vpc.id

  tags = {
    Name = "cryptostock_igw"
  }
}

resource "aws_subnet" "cryptostock_public_subnet" {
  count             = var.subnet_count.public
  vpc_id            = aws_vpc.cryptostock_vpc.id
  cidr_block        = var.public_subnet_cidr_blocks[count.index]
  availability_zone = var.aws_availability_zones[count.index]

  tags = {
    Name = "cryptostock_public_subnet_${count.index}"
  }
}

resource "aws_subnet" "cryptostock_private_subnet" {
  count             = var.subnet_count.private
  vpc_id            = aws_vpc.cryptostock_vpc.id
  cidr_block        = var.private_subnet_cidr_blocks[count.index]
  availability_zone = var.aws_availability_zones[count.index]

  tags = {
    Name = "cryptostock_private_subnet_${count.index}"
  }
}

resource "aws_route_table" "cryptostock_public_rt" {
  vpc_id = aws_vpc.cryptostock_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.cryptostock_igw.id
  }
}

resource "aws_route_table_association" "public" {
  count          = var.subnet_count.public
  route_table_id = aws_route_table.cryptostock_public_rt.id
  subnet_id      = aws_subnet.cryptostock_public_subnet[count.index].id
}

resource "aws_route_table" "cryptostock_private_rt" {
  vpc_id = aws_vpc.cryptostock_vpc.id
}

resource "aws_route_table_association" "private" {
  count          = var.subnet_count.private
  route_table_id = aws_route_table.cryptostock_private_rt.id
  subnet_id      = aws_subnet.cryptostock_private_subnet[count.index].id
}

resource "aws_security_group" "cryptostock_web_sg" {
  name        = "cryptostock_web_sg"
  description = "Security group for cryptostock web services"
  vpc_id      = aws_vpc.cryptostock_vpc.id

  ingress {
    description = "Allow all traffic through HTTP"
    cidr_blocks = ["0.0.0.0/0"]
    protocol    = "tcp"
    from_port   = "80"
    to_port     = "80"
  }

  ingress {
    description = "Allow SSH from my PC"
    cidr_blocks = ["${var.my_ip}/32"]
    protocol    = "tcp"
    from_port   = "22"
    to_port     = "22"
  }

  egress {
    description = "allow all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "cryptostock_web_sg"
  }
}

resource "aws_security_group" "cryptostock_db_sg" {
  name        = "cryptostock_db_sg"
  description = "Security group for cryptostock databases"
  vpc_id      = aws_vpc.cryptostock_vpc.id

  ingress {
    description     = "Allow PSQL traffic from only the web sg"
    protocol        = "tcp"
    from_port       = "5432"
    to_port         = "5432"
    security_groups = [aws_security_group.cryptostock_web_sg.id]
  }

  tags = {
    Name = "cryptostock_db_sg"
  }
}

resource "aws_db_subnet_group" "cryptostock_db_subnet_group" {
  name        = "cryptostock_db_subnet_group"
  description = "DB subnet group for cryptostock"

  subnet_ids = [for subnet in aws_subnet.cryptostock_private_subnet : subnet.id]
}

resource "aws_db_instance" "cryptostock_database" {
  identifier             = var.settings.database.identifier
  allocated_storage      = var.settings.database.allocated_storage
  engine                 = var.settings.database.engine
  engine_version         = var.settings.database.engine_version
  instance_class         = var.settings.database.instance_class
  db_name                = var.settings.database.db_name
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.cryptostock_db_subnet_group.name
  vpc_security_group_ids = [aws_security_group.cryptostock_db_sg.id]
  skip_final_snapshot    = var.settings.database.skip_final_snapshot
}

resource "aws_key_pair" "cryptostock_kp" {
  key_name   = "cryptostock_kp"
  public_key = file(var.public_key_name)
}

resource "aws_instance" "cryptostock_web" {
  count                  = var.settings.web_app.count
  ami                    = var.settings.web_app.ami
  instance_type          = var.settings.web_app.instance_type
  subnet_id              = aws_subnet.cryptostock_public_subnet[count.index].id
  key_name               = aws_key_pair.cryptostock_kp.key_name
  vpc_security_group_ids = [aws_security_group.cryptostock_web_sg.id]

  tags = {
    Name = "cryptostock_web_${count.index}"
  }
}

resource "aws_eip" "cryptostock_web_eip" {
  count    = var.settings.web_app.count
  instance = aws_instance.cryptostock_web[count.index].id
  vpc      = true

  tags = {
    Name = "cryptostock_web_eip_${count.index}"
  }
}
