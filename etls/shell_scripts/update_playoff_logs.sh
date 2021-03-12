#! /bin/bash

export TZ="America/Chicago"
TOP_LEVEL="$( cd .. && cd .. && pwd )"

echo_time() {
    date +"%d/%m/%Y %H:%M:%S%z $*"
}

source ${TOP_LEVEL}/env/bin/activate

echo_time "starting script"
python3 ${TOP_LEVEL}/etls/playoff_logs.py 
echo_time "done running script"

deactivate
echo_time "Finished"
