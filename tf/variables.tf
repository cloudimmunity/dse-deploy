variable "access_key" {}
variable "secret_key" {}

variable "region" {
    default = "us-west-1"
}

variable "vpc" {
    description = "VPC to use."
}

variable "vpc_subnet" {
    description = "VPC subnet to use."
}

variable "ami" {
    description = "AMI to use."
    default = "ami-df6a8b9b"
}

variable "instance_type" {
    description = "Intance type to use."
    default = "m3.large"
}

variable "key_name" {
    description = "Name of the SSH keypair to use in AWS."
}

variable "key_path" {
    description = "Path to the private portion of the SSH key specified."
}

variable "ssh_user" {
    description = "ssh user."
    default = "ubuntu"
}

variable "ssh_port" {
    description = "ssh port."
    default = 22
}

variable "dse_un" {}
variable "dse_pw" {}

variable "node_rkey" {
    description = "aws_instance resource key."
    default = "dse_node"
}

variable "node_name" {
    description = "aws_instance name."
    default = "DSE Node"
}



