#! /bin/fish

# source this script to set the required environment variables
# requirebe by Gurobi. This script suppos a "defaul" linux installation.

set -l curr_vers /opt/gurobi*
set LD_LIBRARY_PATH "$LD_LIBRARY_PATH":"$curr_vers/linux64/lib"
export LD_LIBRARY_PATH

set GRB_LICENSE_FILE ~/.gurobi/gurobi.lic
export GRB_LICENSE_FILE






