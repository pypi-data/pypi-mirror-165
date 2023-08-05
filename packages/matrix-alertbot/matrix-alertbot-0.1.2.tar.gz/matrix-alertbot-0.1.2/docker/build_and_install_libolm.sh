#!/usr/bin/env sh
#
# Call with the following arguments:
#
#    ./build_and_install_libolm.sh <libolm version> <git source dir> <python bindings install dir>
#
# Example:
#
#    ./build_and_install_libolm.sh 3.1.4 /usr/local/src/olm /python-bindings
#
# Note that if a python bindings installation directory is not supplied, bindings will
# be installed to the default directory.
#

set -ex

if [[ $# -ne 3 ]]; then
  echo "Usage: $0 <libolm version> <source dir> <install dir>"
  exit 1
fi

version="$1"
src_dir="$2"
install_dir="$3"

# Download the specified version of libolm
git clone -b "$version" https://gitlab.matrix.org/matrix-org/olm.git "$src_dir"
cd "$src_dir"

# Build libolm
cmake . -Bbuild
cmake --build build

# Install
make install

# Build the python3 bindings
cd python
make olm-python3

# Install python3 bindings
mkdir -p "$install_dir" || true
DESTDIR="$install_dir" make install-python3
