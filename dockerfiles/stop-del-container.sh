#import some common variables to build container
source ./vars.sh

RUNNING=`docker ps -a --format "{{.Names}}:{{.Status}}" |grep ${CONTAINER_NAME} | awk -F: '{print $2}' | awk -F' ' '{print toupper($1)}'`

if [ ! -z $RUNNING ]; then
    echo "Container ${CONTAINER_NAME} status: ${RUNNING}"
    if [ "$RUNNING" == "UP" ]; then
        echo "stopping ${CONTAINER_NAME}"
        docker stop ${CONTAINER_NAME}
    fi
    echo "deleting ${CONTAINER_NAME}"
    docker rm ${CONTAINER_NAME}
else
    echo "Container ${CONTAINER_NAME} does not exist"
fi
