#!/bin/bash

# 定义需要配置的设备ID
DEVICE_ID="1fe1:2030"

# 遍历所有PCI设备
for device in $(lspci -D | grep "$DEVICE_ID" | awk '{print $1}'); do
    # 执行setpci命令
    sudo setpci -s "$device" 0x4.w=7
done

echo "所有Device $DEVICE_ID的配置已完成。"

for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
    echo performance | sudo tee $cpu
done

journalctl -f -k >> /home/user/win2030/win2030/debug-log/host/dmesg+$(date +%Y年%m月%d日%H时%M分%S秒).log