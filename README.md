# 🏡 民宿房间管理系统

适用于 **iStoreOS (OpenWrt)** 环境的轻量级民宿管理 Web 应用，扁平化浅蓝少女配色。

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 📊 **仪表盘** | 实时统计：房间状态、入住率、收支、高考倒计时、名言滚动 |
| 📋 **预订管理** | 预订→确认→入住→退房全流程，每日价格自动填入日历，支持 ID 搜索 |
| 📅 **日历视图** | 可视化日历：点击格子定价，周五/六为周末，法定节假日+节前日标记，底行日合计/列合计，导出 Excel |
| 📂 **基础信息** | 折叠菜单：房型、房间（支持拖拽排序）、客人、预订来源（自定义颜色）、节假日管理 |
| 💸 **支出管理** | 自定义支出类别和颜色，关联房间，筛选查询 |
| 📈 **统计报表** | 收支净利润柱状图+入住率折线，按月/周/天/房间多维度，支持自定义日期区间和房间筛选 |
| 📖 **运营日记** | 记录日常运营，天气/心情/图片 |
| 🔍 **全局搜索** | 快速搜索客人、房间、预订（含 ID） |
| 📝 **系统日志** | 完整操作日志，支持查看和清空 |
| 🖼️ **图片上传** | 房型/日记图片上传，自动生成缩略图 |
| 📤 **数据导出/导入** | JSON 格式一键备份恢复，日历导出 Excel |
| 🗑️ **清空数据** | 一键清除所有业务数据 |
| 📱 **响应式设计** | 适配桌面端和移动端 |

## 📁 项目结构

```
home/
├── app.py                  # Flask 主应用
├── config.py               # 配置文件
├── requirements.txt        # Python 依赖
├── start.sh / start.ps1    # 启动脚本
├── data/                   # JSON 数据（可读、可迁移）
│   ├── room_types.json     # 房型
│   ├── rooms.json          # 房间（含 sort_order）
│   ├── guests.json         # 客人
│   ├── bookings.json       # 预订
│   ├── daily_prices.json   # 每日价格
│   ├── extra_income.json   # 额外收入
│   ├── expenses.json       # 支出记录
│   ├── expense_categories.json  # 支出类别
│   ├── booking_sources.json     # 预订来源
│   ├── holidays.json       # 节假日
│   ├── diary.json          # 运营日记
│   ├── system_logs.json    # 操作日志
│   └── quotes.txt          # 名言库
├── logs/system.log         # 文本日志
├── static/
│   ├── css/style.css       # 扁平化少女配色
│   ├── js/main.js          # 通用 JS
│   └── uploads/            # 上传图片
├── templates/              # HTML 模板（10个页面）
└── utils/                  # 工具模块
```

## 🚀 快速开始

### 环境要求

- Python 3.7+
- pip

### 安装依赖

```bash
pip install Flask Pillow openpyxl
```

### 启动服务

```bash
python app.py
```

启动后访问：**http://localhost:8080**

### iStoreOS 部署

1. 上传项目到 `/opt/homestay/`
2. `opkg install python3 python3-pip`
3. `pip3 install Flask Pillow openpyxl`
4. 创建 `/etc/init.d/homestay` 开机自启脚本

## 💾 数据存储

所有数据以 **格式化 JSON** 存储在 `data/` 目录，直接复制即可迁移。也可使用网页「导出/导入」按钮备份恢复。

## 🔧 配置

编辑 `config.py` 可修改端口（默认 8080）、分页大小、上传限制等。

