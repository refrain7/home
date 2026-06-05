# -*- coding: utf-8 -*-
"""
民宿房间管理系统 - 配置文件
适用于 iStoreOS (OpenWrt) 环境
"""

import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据存储目录（JSON文件，可读可迁移）
DATA_DIR = os.path.join(BASE_DIR, 'data')

# 上传文件目录
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')

# 日志目录
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# 数据文件路径
ROOM_TYPES_FILE = os.path.join(DATA_DIR, 'room_types.json')
ROOMS_FILE = os.path.join(DATA_DIR, 'rooms.json')
GUESTS_FILE = os.path.join(DATA_DIR, 'guests.json')
BOOKINGS_FILE = os.path.join(DATA_DIR, 'bookings.json')
LOGS_FILE = os.path.join(DATA_DIR, 'system_logs.json')
PRICES_FILE = os.path.join(DATA_DIR, 'special_prices.json')
DIARY_FILE = os.path.join(DATA_DIR, 'diary.json')

# Flask 配置
SECRET_KEY = 'homestay-manager-secret-key-2024'
DEBUG = True
HOST = '0.0.0.0'
PORT = 8080

# 图片上传配置
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

# 民宿基本信息
HOMESTAY_NAME = '民宿房间管理系统'
PAGE_SIZE = 20  # 分页大小

# 房间状态选项
ROOM_STATUS = {
    'available': '空闲',
    'occupied': '已入住',
    'reserved': '已预订',
    'cleaning': '打扫中',
    'maintenance': '维修中',
    'blocked': '已锁定'
}

# 预订状态选项
BOOKING_STATUS = {
    'pending': '待确认',
    'confirmed': '已确认',
    'checked_in': '已入住',
    'checked_out': '已退房',
    'cancelled': '已取消',
    'no_show': '未到店'
}

# 确保必要目录存在
for d in [DATA_DIR, UPLOAD_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)
