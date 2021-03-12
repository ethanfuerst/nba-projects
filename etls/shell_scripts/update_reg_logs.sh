#! /bin/bash

export TZ="America/Chicago"
TOP_LEVEL="$( cd .. && cd .. && pwd )"
VENV_NAME="venv"

echo_time() {
    date +"%d/%m/%Y %H:%M:%S%z $*"
}

activate_venv() {
    if [ "${ISWINDOWS}" = true ]; then
        source ${PROJ_ROOT}/${VENV_NAME}/Scripts/activate
    else
        source ${PROJ_ROOT}/${VENV_NAME}/bin/activate
    fi
}

source ${TOP_LEVEL}env/bin/activate

activate_venv

echo_time "TEST!"
# python3 ${AUX_SCRIPTS}/reg_logs.py 
echo_time "TEST"

deactivate
echo_time "Finished"