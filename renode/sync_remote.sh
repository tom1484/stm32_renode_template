WORKSPACE_PATH=$1
PROJECT_NAME=$2

REMOTE_PATH="~/.cache/STM32$WORKSPACE_PATH"
REMOTE_HOST="tomchen@churong.cc"

# Sync the built binary to the remote path
BUILD_PATH="build/Debug"
ssh $REMOTE_HOST "mkdir -p $REMOTE_PATH/$BUILD_PATH/"
rsync -avz --delete $WORKSPACE_PATH/$BUILD_PATH/$PROJECT_NAME.elf $REMOTE_HOST:$REMOTE_PATH/$BUILD_PATH/

# Sync the renode config to the remote path
ssh $REMOTE_HOST "mkdir -p $REMOTE_PATH/renode/"
rsync -avz --delete $WORKSPACE_PATH/renode/config $REMOTE_HOST:$REMOTE_PATH/renode/
