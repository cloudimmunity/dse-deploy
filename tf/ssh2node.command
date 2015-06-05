#!/usr/bin/env bash

set -e

here="$(dirname "$BASH_SOURCE")"
cd $here

ssh ubuntu@52.8.190.240 -p 22 -i atp_labs_env_west_ca.pem





