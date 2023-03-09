#!/usr/bin/env bash

images=()

# 获取所有镜像
for image in $(cat ../docker-compose.yml | grep  image: | awk -F  ": " '{print $2}')
do
    echo "需要打包的镜像" $image
    images+=($image)
done

# 去重
images=($(awk -vRS=' ' '!a[$1]++' <<< ${images[@]}))

for image in ${images[@]}
do
    echo "打包镜像" ${image} "开始"
    arr=(${image//// })
    docker save ${image} -o ${arr[-1]}.tgz
    echo "打包镜像" ${image} "成功"
done
