source ./vars.sh

DOCKERFILE_NAME='Dockerfile'

#args used to build dockerfile
CONTAINER_BUILD_ARGS="--build-arg UID=$HOST_UID --build-arg GID=$HOST_GID --build-arg VOLUME_DIR=$VOLUME_DIR"

${CONTAINER_CMD} ${BUILD_CMD} ${CONTAINER_BUILD_ARGS} -t ${CONTAINER_IMAGE} -f ${DOCKERFILE_NAME} ${CONTEXT_PATH}