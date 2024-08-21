#/bin/bash
echo $PLATFORMS >> /tmp/test.txt
for PLATFORM in $(echo $PLATFORMS | tr ',' '\n'); do
  plat=${PLATFORM#*/}
  echo "docker pull --platform ${PLATFORM} ${ALIYUN_REGISTRY}/${ALIYUN_NAME_SPACE}/${COMMIT_MESSAGE}_${plat}" >> /tmp/test.txt
done
###
