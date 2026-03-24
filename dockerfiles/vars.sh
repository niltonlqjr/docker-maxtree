VOLUME_DIR="${HOME}"                            # Mappped volume
WORK_DIR="${HOME}"                              # Directory that will be used to executables
CONTAINER_CMD="docker"                          # Container application
BUILD_CMD="build"                               # Container application build command
CONTEXT_PATH="../"                              # dockerfile context path
IMAGE_NAME="libvips"                          # name of the container
IMAGE_VERSION="22.04"                           # version of image
CONTAINER_IMAGE=${IMAGE_NAME}:${IMAGE_VERSION}  # Name of image to be generated
CONTAINER_NAME="LIBVIPS"

CONTAINER_USER="experiments"			# username in container 

HOST_UID=$(id -u) # get user ID from system to use in docker 
HOST_GID=$(id -g) # get user ID from system to use in docker



