#!/bin/bash
PLATFORMS=$1
COMMIT_MESSAGE=$2

echo PLATFORMS:$PLATFORMS >> /tmp/test.txt

for PLATFORM in $(echo $PLATFORMS | tr ',' '\n'); do
  echo PLATFORM:$PLATFORM >> /tmp/test.txt
  plat="${PLATFORM#*/}"
  echo plat:$plat >> /tmp/test.txt
  docker pull  --platform $PLATFORM  ${ALIYUN_REGISTRY}/${ALIYUN_NAME_SPACE}/${COMMIT_MESSAGE}_${plat}
done
