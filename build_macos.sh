#!/usr/bin/env bash

version=$(cat ./app/VERSION.txt)

pyinstaller ./app/app.py \
  --name "Maze" \
  --noconfirm \
  --noconsole \
  --add-data "./app/data/.gitkeep:data/.gitkeep" \
  --add-data "./app/images/*:images" \
  --add-data "./app/resources/default_config.cfg:resources" \
  --icon "./app/images/icon.png" \
  --clean \

retval=$?

if [ $retval -ne 0 ]; then
  echo "Build exited with error code: "$retval
  exit
fi

cd dist || exit
zip -9Tr ./maze_macos_"$version".zip ./Maze.app
cd .. || exit
