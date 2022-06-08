variable "aws_region" {
  default = "us-east-2"
}

variable "vpc_cidr_block" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

// Number of public and private subnets
variable "subnet_count" {
  description = "Number of subnets"
  type        = map(number)
  default = {
    public  = 1,
    private = 2
  }
}

// conf settings for the EC2 and RDS instances
variable "settings" {
  description = "Configuration settings"
  type        = map(any)
  default = {
    "database" = {
      identifier          = "cryptostock-db-01"
      allocated_storage   = 20
      engine              = "postgres"
      engine_version      = "13.4"
      instance_class      = "db.t3.micro"
      db_name             = "cryptostock_db"
      skip_final_snapshot = true
    },
    "web_app" = {
      count         = 1
      ami           = "ami-0eea504f45ef7a8f7"
      instance_type = "t2.micro"
    }
  }
}

variable "public_subnet_cidr_blocks" {
  description = "Available CIDR blocks for public subnets"
  type        = list(string)
  default = [
    "10.0.1.0/24",
    "10.0.2.0/24",
    "10.0.3.0/24",
    "10.0.4.0/24"
  ]
}

variable "private_subnet_cidr_blocks" {
  description = "Available CIDR blocks for private subnets"
  type        = list(string)
  default = [
    "10.0.101.0/24",
    "10.0.102.0/24",
    "10.0.103.0/24",
    "10.0.104.0/24"
  ]
}

variable "aws_availability_zones" {
  description = "Available AWS zones"
  type        = list(string)
  default = [
    "us-east-2a",
    "us-east-2b",
    "us-east-2c"
  ]
}

// curl http://checkip.amazonaws.com
variable "my_ip" {
  description = "Your IP adress"
  type        = string
  sensitive   = true
}

// value must storing in secret file
variable "db_username" {
  description = "DB master user"
  type        = string
  sensitive   = true
}

// value must storing in secret file
variable "db_password" {
  description = "DB master user password"
  type        = string
  sensitive   = true
}

// value must storing in secret file
variable "aws_access_key" {
  description = "Access key to AWS account"
  type        = string
  sensitive   = true
}

// value must storing in secret file
variable "aws_secret_key" {
  description = "Secret key to AWS account"
  type        = string
  sensitive   = true
}

variable "public_key_name" {
  description = "Name of public key for EC2 access"
  type        = string
  default     = "cryptostock_kp.pub"
}
