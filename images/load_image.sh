#!/usr/bin/env bash

images=()

# 获取所有镜像
for image in $(cat ../docker-compose.yaml | grep  image: | awk -F  ": " '{print $2}')
do
    echo "需要加载的镜像" $image
    images+=($image)
done

# 去重
images=($(awk -vRS=' ' '!a[$1]++' <<< ${images[@]}))

for image in ${images[@]}
do
    echo "加载" ${image} "开始"
    arr=(${image//// })
    docker load -i ${arr[-1]}.tgz
    echo "加载" ${image} "成功"
done
