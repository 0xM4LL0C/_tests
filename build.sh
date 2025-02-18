#!/bin/bash

os_list=("linux" "darwin" "windows")
arch_list=("amd64" "386" "arm64")


if [ -z "$1" ]; then
    echo "Usage: $0 <module_name>"
    exit 1
fi
module_name=$1


output_dir="./bin"
module_basename="app"

mkdir -p "$output_dir/$module_basename"
rm -rf "$output_dir/$module_basename"/*

build_for_platform() {
    local os=$1
    local arch=$2
    local app_name="$module_basename-$os-$arch"

    if [ "$os" == "windows" ]; then
        app_name+=".exe"
    fi

    printf "Building $app_name: "

    GOOS=$os GOARCH=$arch go build -o "$output_dir/$module_basename/$app_name" -ldflags "-w" "$module_name"

    if [ $? -eq 0 ]; then
        echo "Done"
    else
        echo "Failed"
    fi
}

for os in "${os_list[@]}"; do
    for arch in "${arch_list[@]}"; do
        build_for_platform "$os" "$arch"
    done
done

echo "All builds completed."
