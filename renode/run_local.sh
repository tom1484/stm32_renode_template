WORKSPACE_PATH=$1
PROJECT_NAME=$2
MACHINE_NAME=$3

docker run -i --rm --net=host \
    -v $WORKSPACE_PATH:/home/developer antmicro/renode:latest \
        renode --console \
        -e "\$bin=\$CWD/build/Debug/$PROJECT_NAME" \
        -e "\$name=$MACHINE_NAME" \
        -e "include \$CWD/renode/config/debug.resc"
