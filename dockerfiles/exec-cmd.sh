#import some common variables to build container
source ./vars.sh

if [ "$1" == "-h" ] || [ "$1" == "--help" ] || [ -z $1 ] || [ -z $2 ];then
    echo "usage $0 <work directory> <command>"
    exit
fi

RUNNING=`docker ps -a --format "{{.Names}}:{{.Status}}" | grep ${CONTAINER_NAME} | awk -F: '{print $2}' | awk -F' ' '{print toupper($1)}'`

if [ -z ${RUNNING} ] || [ "${RUNNING}" == "EXITED" ]; then
    echo "Container ${CONTAINER_NAME} is not running"
    exit
else
    RUN_CMD="exec"
    WORKDIR_VAR=$1
    shift
    COMMAND_TO_EXEC=$@
fi

echo "${CONTAINER_CMD} ${RUN_CMD} ${CONTAINER_RUN_ARGS} ${NETWORK_ARG}\
  -w ${WORKDIR_VAR} \
  ${CONTAINER_NAME} \
  ${COMMAND_TO_EXEC}
"
${CONTAINER_CMD} ${RUN_CMD} ${CONTAINER_RUN_ARGS} ${NETWORK_ARG}\
  -w ${WORKDIR_VAR} \
  ${CONTAINER_NAME} \
  ${COMMAND_TO_EXEC}
