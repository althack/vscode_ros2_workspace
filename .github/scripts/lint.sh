#!/bin/bash
set -e

LINTER="$1"

./setup.sh

case "$LINTER" in
  "uncrustify"|"cppcheck"|"cpplint")
    if [ -z "$(find src/ -name '*.cpp' -o -name '*.hpp' -o -name '*.c' -o -name '*.h')" ]; then
      echo "No C/C++ files found. Skipping $LINTER."
      exit 0
    fi
    ;;
  "flake8"|"pep257")
    if [ -z "$(find src/ -name '*.py')" ]; then
      echo "No Python files found. Skipping $LINTER."
      exit 0
    fi
    ;;
esac

source "/opt/ros/$ROS_DISTRO/setup.bash"
"ament_${LINTER}" src/
