#!/usr/bin/env bash
set -e

echo "starting a node..."
vagrant up --provider=aws
fab save_node_info

echo "preparing DSE services..."
fab node_env dse_prepare

echo "starting DSE services..."
fab node_env dse_start

echo "checking the DSE service status..."
fab node_env dse_status

echo "[ok] done!"
