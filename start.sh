# 民宿房间管理系统 - 启动脚本
# 适用于 iStoreOS (OpenWrt) 环境
# 用法: sh start.sh

#!/bin/sh

# 获取脚本所在目录
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

# Python 解释器（iStoreOS 通常使用 python3）
PYTHON="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON="python"
fi

echo "========================================="
echo "  民宿房间管理系统"
echo "  数据目录: $DIR/data"
echo "  上传目录: $DIR/static/uploads"
echo "  日志目录: $DIR/logs"
echo "========================================="

# 检查依赖
echo "检查 Python 依赖..."
$PYTHON -c "import flask" 2>/dev/null || {
    echo "正在安装 Flask..."
    pip3 install Flask Pillow || pip install Flask Pillow
}

$PYTHON -c "import PIL" 2>/dev/null || {
    echo "正在安装 Pillow..."
    pip3 install Pillow || pip install Pillow
}

# 确保目录存在
mkdir -p data logs static/uploads static/uploads/room_types

# 启动应用
echo "启动服务..."
$PYTHON app.py
