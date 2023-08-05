# To build the image, run `docker build` command from the root of the
# repository:
#
#    docker build -f docker/Dockerfile .
#
# There is an optional PYTHON_VERSION build argument which sets the
# version of python to build against. For example:
#
#    docker build -f docker/Dockerfile --build-arg PYTHON_VERSION=3.10 .
#
# An optional LIBOLM_VERSION build argument which sets the
# version of libolm to build against. For example:
#
#    docker build -f docker/Dockerfile --build-arg LIBOLM_VERSION=3.2.10 .
#


##
## Creating a builder container
##

# We use an initial docker container to build all of the runtime dependencies,
# then transfer those dependencies to the container we're going to ship,
# before throwing this one away
ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-alpine as builder

##
## Build libolm for matrix-nio e2e support
##

# Install libolm build dependencies
ARG LIBOLM_VERSION=3.2.10
RUN apk add --no-cache \
    make \
    cmake \
    gcc \
    g++ \
    git \
    libffi-dev \
    yaml-dev \
    python3-dev

ENV PROJECT_DIR="/opt/matrix_alertbot"
ENV LIBOLM_SRC_DIR="/usr/local/src/olm"
ENV LIBOLM_INSTALL_DIR="/opt/olm"
ENV VIRTUAL_ENV="${PROJECT_DIR}/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python -m venv "${VIRTUAL_ENV}"

WORKDIR "${PROJECT_DIR}"
# Build libolm
#
# Also build the libolm python bindings and place them at /python-libs
# We will later copy contents from both of these folders to the runtime
# container
COPY docker/build_and_install_libolm.sh /scripts/
RUN /scripts/build_and_install_libolm.sh "${LIBOLM_VERSION}" "${LIBOLM_SRC_DIR}" "${LIBOLM_INSTALL_DIR}"

# Install python runtime modules. We do this before copying the source code
# such that these dependencies can be cached
# This speeds up subsequent image builds when the source code is changed
RUN mkdir -p ./matrix_alertbot/
COPY matrix_alertbot/__init__.py ./matrix_alertbot/
COPY README.md matrix-alertbot ./

# Build the dependencies
COPY setup.py setup.cfg ./
RUN pip install --no-warn-script-location ".[e2e]"

# Now copy the source code
COPY *.py *.md *.in ./
COPY matrix_alertbot/*.py ./matrix_alertbot/
COPY matrix_alertbot/resources ./matrix_alertbot/resources

# And build the final module
RUN pip install --no-warn-script-location ".[e2e]"

COPY tests ./tests

##
## Creating the runtime container
##

# Create the container we'll actually ship. We need to copy libolm and any
# python dependencies that we built above to this container
FROM python:${PYTHON_VERSION}-alpine

ENV PROJECT_DIR="/opt/matrix_alertbot"
ENV VIRTUAL_ENV="${PROJECT_DIR}/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR "${PROJECT_DIR}"

# Copy python dependencies from the "builder" container
COPY --from=builder "${PROJECT_DIR}" "${PROJECT_DIR}"

# Copy libolm from the "builder" container
COPY --from=builder /usr/local/lib/libolm* /usr/local/lib/

# Install any native runtime dependencies
RUN apk add --no-cache libstdc++

# Specify a volume that holds the config file, SQLite3 database,
# and the matrix-nio store
VOLUME ["/data"]

# Start the bot
CMD ["matrix-alertbot", "/data/config.yaml"]
