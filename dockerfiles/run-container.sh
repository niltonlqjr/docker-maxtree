#############################################################################
#                                                                           #
# Run a docker container with environmnet variables needed to disccofan.    #
# Also maps /home/mpi/host from container to user home                      #
#                                                                           #
#############################################################################

#import some common variables to build container
source ./vars.sh

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
    CONTAINER_RUN_ARGS="-it --name ${CONTAINER_NAME} "
    VOLUME_ARG="--volume ${HOME}:/home/${CONTAINER_USER}/host"
    VOLUME_ARG=${VOLUME_ARG}" --volume /mnt:/mnt"
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
    CONTAINER_RUN_ARGS="-i "
    VOLUME_ARG=""
    COMMAND_TO_EXEC=""
    CONTAINER=$CONTAINER_NAME
    NETWORK_ARG=""
else
    RUN_CMD="exec"
    CONTAINER_RUN_ARGS="-it"
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
