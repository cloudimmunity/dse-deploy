#!/usr/bin/env bash
set -e

echo "destroying AWS infrastructure..."
terraform plan -destroy
terraform destroy

echo "[ok] done!"
