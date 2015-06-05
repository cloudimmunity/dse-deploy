provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region = "${var.region}"
}

resource "aws_security_group" "dse_node_sg" {
    name = "dse_node_sg"
    description = "DSE ports"
    vpc_id = "${var.vpc}"
    
    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    
    ingress {
        from_port = 8888
        to_port = 8888
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 9042
        to_port = 9042
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port = 9160
        to_port = 9160
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
      from_port = 0
      to_port = 65535
      protocol = "tcp"
      self = true
    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags {
      Name = "dse_node_sg"
    }
}

resource "aws_instance" "dse_node" {
  ami = "${var.ami}"
  instance_type = "${var.instance_type}"
  key_name = "${var.key_name}"

  tags {
      Name = "${var.node_name}"
  }

  subnet_id = "${var.vpc_subnet}"
  security_groups = ["${aws_security_group.dse_node_sg.id}"]
  
  connection {
    user = "${var.ssh_user}"
    key_file = "${var.key_path}"
  }

  provisioner "remote-exec" {
    script = "./provision_begin.sh"
  }

  provisioner "remote-exec" {
    inline = [
        "echo \"deb http://${var.dse_un}:${var.dse_pw}@debian.datastax.com/enterprise stable main\" | sudo tee -a /etc/apt/sources.list.d/datastax.sources.list"
    ]
  }

  provisioner "remote-exec" {
    script = "./provision_end.sh"
  }
}
