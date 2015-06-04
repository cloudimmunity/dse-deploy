## OVERVIEW

These scripts will create a DataStax Enterprise (DSE) cluster with one node in your AWS VPC environment.

It's meant for development/testing only!

## REQUIREMENTS

1. Installed Vagrant (get it from http://www.vagrantup.com/downloads.html)
2. Installed vagrant-aws plugin (vagrant plugin install vagrant-aws)
3. Installed Fabric (run ./prep.sh once / dependencies: python, pip)
4. DataStax Enterprise credentials
5. AWS security group that allows DSE ports (tcp ports 8888, 8983, 9042, and 9160)

## CONFIGURATION VARIABLES

Stored in `vars.json` (by default).

Replace "<INSERT_VALUE_HERE>" with your values.

You can use a relative path in the "ssh.private_key_path" field (e.g., "./my_private_key.pem")

Feel free to change other values too :-)

#### Important Config Variables

* dse.username
* dse.password
* ssh.private_key_path
* aws.access_key_id
* aws.secret_access_key
* aws.keypair_name
* aws.subnet_id
* aws.security_groups - user security group IDs

#### Other Config Variables

* dse.cluster_name
* dse.solr
* dse.spark
* ssh.username
* ssh.port
* aws.ami - default: ami-df6a8b9b (Ubuntu 14.04)
* aws.instance_type - default: m3.large
* aws.region - default: us-west-1
* aws.associate_public_ip

## CREATING YOUR DSE NODE

Execute ./up.sh (or click on up.common if you are using a Mac).

Once the node is up and running the `node.json` file will contain the information you need to connect to the new node.

## DESTROYING YOUR DSE NODE

Execute ./down.sh (or click on down.common if you are using a Mac).

