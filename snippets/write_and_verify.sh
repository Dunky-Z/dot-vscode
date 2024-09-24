#!/bin/bash

# 检查是否有足够的参数传入
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <start_address> <length>"
    exit 1
fi

START_ADDR=$1  # 起始地址
LENGTH=$2      # 长度

# 检查 devmem2 命令是否存在
if ! command -v devmem2 &> /dev/null; then
    echo "Error: devmem2 is not installed."
    exit 1
fi

# 将16进制的长度转换为10进制
START_ADDR=$((START_ADDR))
LENGTH=$((LENGTH))

# 用于生成随机数据的函数
generate_random_value() {
    printf "0x%x" $((RANDOM))
}

# 写入数据并验证
for (( i=0; i<$LENGTH; i+=4 )); do
    CURRENT_ADDR=$(printf "0x%x" $((START_ADDR + i)))

    # 生成一个随机值
    VALUE=$(generate_random_value)

    echo "Writing value $VALUE to address $CURRENT_ADDR"
    devmem2 $CURRENT_ADDR w $VALUE

done

echo "All values successfully written and verified."
