#!/bin/bash

# 提示用户输入根文件系统镜像文件的路径
function get_rootfs_path() {
    read -p "请输入根文件系统镜像文件的路径: " rootfs_path

    if [ ! -f "$rootfs_path" ]; then
        echo "错误: 根文件系统镜像文件不存在。"
        exit 1
    fi

    echo "$rootfs_path"
}

# 提示用户输入驱动程序目录的路径
function get_drivers_path() {
    read -p "请输入驱动程序目录的路径: " drivers_path

    if [ ! -d "$drivers_path" ]; then
        echo "错误: 驱动程序目录不存在。"
        exit 1
    fi

    echo "$drivers_path"
}

# 创建唯一的挂载目录
function create_mount_dir() {
    local mount_dir
    mount_dir=$(mktemp -d /tmp/mount_dir.XXXXXX)

    if [ ! -d "$mount_dir" ]; then
        echo "错误: 无法创建挂载目录。"
        exit 1
    fi

    echo "$mount_dir"
}

# 挂载根文件系统镜像文件
function mount_rootfs() {
    local rootfs_path="$1"
    local mount_dir="$2"
    
    sudo mount -o loop "$rootfs_path" "$mount_dir"
    if [ $? -ne 0 ]; then
        echo "错误: 无法挂载根文件系统镜像文件。"
        rmdir "$mount_dir"
        exit 1
    fi
}

# 拷贝驱动程序目录到根文件系统中
function copy_drivers() {
    local drivers_path="$1"
    local mount_dir="$2"
    
    sudo cp -r "$drivers_path" "$mount_dir"
    if [ $? -ne 0 ]; then
        echo "错误: 无法拷贝驱动程序目录。"
        sudo umount "$mount_dir"
        rmdir "$mount_dir"
        exit 1
    fi
}

# 验证驱动程序是否复制成功
function verify_copy() {
    local drivers_path="$1"
    local mount_dir="$2"
    local driver_name

    driver_name=$(basename "$drivers_path")

    if [ ! -d "$mount_dir/$driver_name" ]; then
        echo "错误: 驱动程序目录未正确复制。"
        sudo umount "$mount_dir"
        rmdir "$mount_dir"
        exit 1
    fi
}

# 卸载挂载的目录
function umount_rootfs() {
    local mount_dir="$1"
    
    sudo umount "$mount_dir"
    if [ $? -ne 0 ]; then
        echo "错误: 无法卸载挂载的目录。"
        exit 1
    fi

    rmdir "$mount_dir"
}

# 主程序
function main() {
    local rootfs_path
    local drivers_path
    local mount_dir

    rootfs_path=$(get_rootfs_path)
    drivers_path=$(get_drivers_path)
    mount_dir=$(create_mount_dir)

    mount_rootfs "$rootfs_path" "$mount_dir"
    copy_drivers "$drivers_path" "$mount_dir"
    verify_copy "$drivers_path" "$mount_dir"
    umount_rootfs "$mount_dir"

    echo "操作成功完成。"
}

main
