import os
import sys
import time
import json
from pprint import pprint
import uuid

from fabric.api import *
from fabric.contrib.files import exists, append, contains, sed, comment

def load_terraform_state():
  fname = os.path.join(os.path.dirname(os.path.abspath(__file__)),'terraform.tfstate')
  return json.load(open(fname, 'r'))

def load_terraform_tfvars():
  fname = os.path.join(os.path.dirname(os.path.abspath(__file__)),'terraform.tfvars.json')
  return json.load(open(fname, 'r'))

def get_node_addresses(node_name):
  tfstate = load_terraform_state()
  instance_name = 'aws_instance.%s' % node_name
  if instance_name not in tfstate['modules'][0]['resources']:
    return None
  
  info = {}
  info['private_ip'] = tfstate['modules'][0]['resources'][instance_name]['primary']['attributes']['private_ip']
  info['public_ip'] = tfstate['modules'][0]['resources'][instance_name]['primary']['attributes']['public_ip']
  return info

def get_tf_node_info():
  vinfo = load_terraform_tfvars()
  nkey = None #'dse_node'
  if 'node_rkey' in vinfo:
    nkey = vinfo['node_rkey']
  
  sinfo = get_node_addresses(nkey)
  
  if sinfo is not None and vinfo is not None:
    return {'host': sinfo['public_ip'], 'port': vinfo['ssh_port'], 'user': vinfo['ssh_user'], 'idfile': vinfo['key_path']}
  else:
    return None

def get_node_info():
  info = local('vagrant ssh-config',capture=True).stdout.splitlines()
  while True:
    if not info[0].startswith('Host '):
      info.pop(0)
    else:
      break

  host = info[1].split()[1]
  user = info[2].split()[1]
  port = info[3].split()[1]
  idfile = info[7].split()[1]
  
  return {'host': host, 'port': port, 'user': user, 'idfile': idfile}

def save_node_info():
  info = get_node_info()
  fname = os.path.join(os.path.dirname(os.path.abspath(__file__)),'node.json')
  with open(fname,'w') as f:
    f.write('%s\n' % json.dumps(info,indent=2))

def load_node_info():
  fname = os.path.join(os.path.dirname(os.path.abspath(__file__)),'node.json')
  return json.load(open(fname, 'r'))

def load_vars():
  fname = os.path.join(os.path.dirname(os.path.abspath(__file__)),'vars.json')
  return json.load(open(fname, 'r'))

def node_env():
  info = get_node_info()

  host = '%s:%s' % (info['host'],info['port'])
  env.hosts = [host]
  env.user = info['user']
  env.key_filename = [info['idfile']]
  env.disable_known_hosts = True

def tf_node_env():
  info = get_tf_node_info()

  host = '%s:%s' % (info['host'],info['port'])
  env.hosts = [host]
  env.user = info['user']
  env.key_filename = [info['idfile']]
  env.disable_known_hosts = True

default_opscenter_cluster_config = """
[jmx]
username =
password =
port = 7199

[cassandra]
username =
seed_hosts = 127.0.0.1
api_port = 9160
password =
"""

def dse_prepare_common(node,vars):
  broadcast_rpc_address_line = 'broadcast_rpc_address: %s' % node['host']
  cluster_name = 'NODE'
  if 'cluster_name' in vars['dse']:
    cluster_name = vars['dse']['cluster_name']
  
  opscenter_cluster_config_name = '/etc/opscenter/clusters/%s.conf' % cluster_name
  cluster_name_line = '%s CLUSTER' % cluster_name
  
  if ('solr' in vars['dse']) and vars['dse']['solr']:
    sed('/etc/default/dse',before='SOLR_ENABLED=0',after='SOLR_ENABLED=1',use_sudo=True, backup='')
  
  if ('spark' in vars['dse']) and vars['dse']['spark']:
    sed('/etc/default/dse',before='SPARK_ENABLED=0',after='SPARK_ENABLED=1',use_sudo=True, backup='')
  
  sed('/etc/dse/cassandra/cassandra.yaml',before="Test Cluster",after=cluster_name_line,use_sudo=True, backup='')
  sed('/etc/dse/cassandra/cassandra.yaml',before="rpc_address: localhost",after="rpc_address: 0.0.0.0",use_sudo=True, backup='')
  sed('/etc/dse/cassandra/cassandra.yaml',before="# broadcast_rpc_address: 1.2.3.4",after=broadcast_rpc_address_line,use_sudo=True, backup='')
  append('/var/lib/datastax-agent/conf/address.yaml','stomp_interface: 127.0.0.1',True)
  
  if not exists(opscenter_cluster_config_name,True):
    sudo('mkdir /etc/opscenter/clusters')
  
  append(opscenter_cluster_config_name,default_opscenter_cluster_config,True)
  time.sleep(8)

def tf_dse_prepare():
  vinfo = load_terraform_tfvars()
  vars = {'dse': {}}
  vars['dse']['cluster_name'] = vinfo['dse_cluster_name']
  vars['dse']['solr'] = bool(vinfo['dse_solr'])
  vars['dse']['spark'] = bool(vinfo['dse_spark'])
  dse_prepare_common(get_tf_node_info(),vars)

def dse_prepare():
  dse_prepare_common(get_node_info(),load_vars())

def dse_stop():
  sudo('service opscenterd stop')
  sudo('service dse stop')
  sudo('service datastax-agent stop')

def dse_start():
  sudo('service dse start')
  sudo('service opscenterd start')
  sudo('service datastax-agent start')

def dse_status():
  with settings(warn_only=True):
    while True:
      res = sudo('service dse status')
      if ' is running' in res:
        break;
      else:
        print 'wait and try again (service dse status)'
        time.sleep(3)
    
    while True:
      res = sudo('service datastax-agent status')
      if ' is running' in res:
        break;
      else:
        print 'wait and try again (service datastax-agent status)'
        time.sleep(3)
    
    while True:
      res = sudo('service opscenterd status')
      if ' is running' in res:
        break;
      else:
        print 'wait and try again (service datastax-agent status)'
        time.sleep(3)

    while True:
      res = sudo('nodetool status')
      if 'Status=' in res:
        time.sleep(3)
        break;
      else:
        print 'wait and try again (nodetool status)'
        time.sleep(3)

###############################################################################
