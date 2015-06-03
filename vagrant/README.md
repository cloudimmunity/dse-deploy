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

Stored in vars.json (by default).

Replace "<INSERT_VALUE_HERE>" with your values.

You can use a relative path in the "ssh.private_key_path" field (e.g., "./my_private_key.pem")

Feel free to change other values too :-)

## STARTING A DSE NODE

Execute ./up.sh (or click on up.common if you are using a Mac).

Once the node is up and running the node.json file will contain the information you need to connect to the new node.