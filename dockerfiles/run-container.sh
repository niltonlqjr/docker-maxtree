#############################################################################
#                                                                           #
# Run a docker container with environmnet variables needed to disccofan.    #
# Also maps /home/mpi/host from container to user home                           #
#                                                                           #
#############################################################################

#import some common variables to build container
source ./vars.sh

ip=$1

# args used to run container


RUNNING=`docker ps -a |grep ${CONTAINER_NAME} | awk -F\  '{print $NF}'`

if [ -z $RUNNING ]
then
    RUN_CMD="run"
    CONTAINER_RUN_ARGS="-it --rm --name ${CONTAINER_NAME} "
    VOLUME_ARG="--volume ${HOME}:/home/${CONTAINER_USER}/host"
    VOLUME_ARG=${VOLUME_ARG}" --volume /mnt:/mnt"
    COMMAND_TO_EXEC=""
    CONTAINER=$CONTAINER_IMAGE

    # arg to use network of host machine
    # to use this configuration, the machine must have a mpi user that is can
    # connect to other cluster machines through ssh with public private key.
    NETWORK_ARG="--network host"
else
    RUN_CMD="exec"
    CONTAINER_RUN_ARGS="-it"
    VOLUME_ARG=""
    COMMAND_TO_EXEC="/bin/bash"
    CONTAINER=$CONTAINER_NAME

    NETWORK_ARG=""
fi

#run container
echo "${CONTAINER_CMD} ${RUN_CMD} ${CONTAINER_RUN_ARGS} ${NETWORK_ARG}\
  --env "SHELL=/bin/bash" \
  --workdir /home/${CONTAINER_USER} \
  ${VOLUME_ARG} \
  ${CONTAINER} \
  ${COMMAND_TO_EXEC}
"
${CONTAINER_CMD} ${RUN_CMD} ${CONTAINER_RUN_ARGS} ${NETWORK_ARG}\
  --env "SHELL=/bin/bash" \
  --workdir /home/${CONTAINER_USER} \
  ${VOLUME_ARG} \
  ${CONTAINER} \
  ${COMMAND_TO_EXEC}
