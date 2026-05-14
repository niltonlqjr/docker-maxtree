#############################################################################
#                                                                           #
# Run a docker container with environmnet variables needed to disccofan.    #
# Also maps /home/mpi/host from container to user home                           #
#                                                                           #
#############################################################################

#import some common variables to build container
source ./vars.sh


# args used to run container

if [ -z $1 ]
then
    ports_lists=("7233" "7234")
else
    ports_lists="$@"
fi

RUNNING=`docker ps -a --format "{{.Names}}:{{.Status}}" | grep ${CONTAINER_NAME} | awk -F: '{print $2}' | awk -F' ' '{print toupper($1)}'`

if [ -z $RUNNING ]
then
    RUN_CMD="run"
    CONTAINER_RUN_ARGS="-d -it --name ${CONTAINER_NAME} "
    VOLUME_ARG="--volume ${HOME}:/home/${CONTAINER_USER}/host"
    COMMAND_TO_EXEC=""
    CONTAINER=$CONTAINER_IMAGE
    NETWORK_ARG=""

    for port in ${ports_list}
    do
        NETWORK_ARG=${NETWORK_ARG}" -p ${port}:${port}"
    done

    ENV_VAR="--env ${CONTAINER_ENV_VARS}"
    WORKDIR_VAR="--workdir /home/${CONTAINER_USER}"
elif [ "$RUNNING" == "EXITED" ]; then
    RUN_CMD="start"
    CONTAINER_RUN_ARGS=""
    VOLUME_ARG=""
    COMMAND_TO_EXEC=""
    CONTAINER=$CONTAINER_NAME
    NETWORK_ARG=""
    ENV_VAR=""
    WORKDIR_VAR=""
else
    RUN_CMD="exec"
    CONTAINER_RUN_ARGS="-d"
    VOLUME_ARG=""
    COMMAND_TO_EXEC="/bin/bash"
    CONTAINER=$CONTAINER_NAME
    NETWORK_ARG=""
    ENV_VAR="--env ${CONTAINER_ENV_VARS}"
    WORKDIR_VAR="--workdir /home/${CONTAINER_USER}"
fi


#run container
echo "${CONTAINER_CMD} ${RUN_CMD} ${CONTAINER_RUN_ARGS} ${NETWORK_ARG}\
  ${ENV_VAR} \
  ${WORKDIR_VAR} \
  ${VOLUME_ARG} \
  ${CONTAINER} \
  ${COMMAND_TO_EXEC}
"
${CONTAINER_CMD} ${RUN_CMD} ${CONTAINER_RUN_ARGS} ${NETWORK_ARG}\
  ${ENV_VAR} \
  ${WORKDIR_VAR} \
  ${VOLUME_ARG} \
  ${CONTAINER} \
  ${COMMAND_TO_EXEC}
