#!/usr/bin/env bash
set -e

echo "preparing AWS infrastructure..."
terraform plan
terraform apply
terraform show

echo "preparing DSE services..."
fab tf_node_env tf_dse_prepare

echo "starting DSE services..."
fab tf_node_env dse_start

echo "checking the DSE service status..."
fab tf_node_env dse_status

echo "[ok] done!"
