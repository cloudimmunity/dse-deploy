## OVERVIEW

These scripts will create a DataStax Enterprise (DSE) cluster with one node in your AWS VPC environment.

It's meant for development/testing only!

## REQUIREMENTS

1. Installed Terraform (get it from http://terraform.io/downloads )
2. Installed Fabric (run `./prep.sh` once / dependencies: python, pip)
4. DataStax Enterprise credentials

## CONFIGURATION VARIABLES

The configuration variables you'll need to update are stored in `terraform.tfvars.json`.

Replace "<INSERT_VALUE_HERE>" with your values.

You can use a relative path in the "key_path" field (e.g., "./my_private_key.pem")

Feel free to change other values too :-)

Note that the terraform spec (`aws.tf`) also creates a security group for you. If you want to use an existing security group then you'll need to remove the `dse_node_sg` aws security group resource in the `aws.tf` file and you'll need to reconfigure the `security_groups` field in the `dse_node` aws instance resource.

If you do want to use an existing security group make sure you can access these tcp ports: 8888, 8983, 9042, and 9160

#### Important Config Variables

* dse_un - your DSE username
* dse_pw - your DSE password
* key_path
* key_name
* access_key - AWS access key ID
* secret_key - AWS secret access key
* vpc - AWS VPC ID
* vpc_subnet - AWS VPC subnet ID

#### Other Config Variables

* dse_cluster_name
* dse_solr
* dse_spark
* ssh_user
* ssh_port
* ami - AWS AMI ID / default: ami-df6a8b9b (Ubuntu 14.04)
* instance_type - AWS instance type name / default: m3.large
* region - AWS region / default: us-west-1
* node_name - AWS instance name

## CREATING YOUR DSE NODE

Execute `./up.sh` (or click on up.common if you are using a Mac).

Once the node is up and running the `terraform.tfstate` file will contain the information about the newly created node.

Now you can access OpsCenter by going to http://<node_address>:8888

## DESTROYING YOUR DSE NODE

Execute `./down.sh` (or click on down.common if you are using a Mac).

You might have to execute `./down.sh` more than once if Terraform fails to remove all resources it created.


