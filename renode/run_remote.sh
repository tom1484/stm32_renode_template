WORKSPACE_PATH=$1
PROJECT_NAME=$2
MACHINE_NAME=$3
GDB_PORT=$4

REMOTE_PATH="~/.cache/STM32$WORKSPACE_PATH"
REMOTE_HOST=$5

ssh $REMOTE_HOST \
    "docker run -i --rm --net=host \
        -v $REMOTE_PATH:/home/developer antmicro/renode:latest \
            renode --console \
            -e '\$bin=\$CWD/build/Debug/$PROJECT_NAME'\
            -e '\$name=$MACHINE_NAME'\
            -e '\$port=$GDB_PORT'\
            -e 'include \$CWD/renode/config/debug.resc'"
