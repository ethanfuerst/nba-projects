#! /bin/bash

export TZ="America/Chicago"
TOP_LEVEL="$( cd .. && cd .. && pwd )"

echo_time() {
    date +"%d/%m/%Y %H:%M:%S%z $*"
}

source ${TOP_LEVEL}env/bin/activate

activate_venv

echo_time "TEST!"
# python3 ${AUX_SCRIPTS}/reg_logs.py 
echo_time "TEST"

deactivate
echo_time "Finished"