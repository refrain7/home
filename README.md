# 🏡 民宿房间管理系统

适用于 **iStoreOS (OpenWrt)** 环境的轻量级民宿管理 Web 应用。

## ✨ 功能特性

| 功能 | 说明 |
|------|------|
| 📊 **仪表盘** | 实时统计概览：房间状态、入住率、收入、高考倒计时、名言滚动 |
| 🏠 **房型管理** | 管理房型名称、价格（基础/周末/节假日）、设施、图片 |
| 🚪 **房间管理** | 管理每个房间的编号、楼层、状态、所属房型 |
| 👤 **客人管理** | 客人信息登记：姓名、手机、身份证、国籍等 |
| 📋 **预订管理** | 完整预订流程：预订→确认→入住→退房，每日价格联动日历 |
| 📅 **日历视图** | 可视化房间预订状态，点击格子直接修改每日价格，支持导出 Excel |
| 📈 **统计报表** | 收入/入住率按年/月/周可视化图表（Chart.js） |
| 📖 **运营日记** | 记录日常运营，支持天气、心情、图片 |
| 🔍 **全局搜索** | 快速搜索客人、房间、预订 |
| 📝 **系统日志** | 完整操作日志记录，支持查看和清空 |
| 🖼️ **图片上传** | 支持房型/日记图片上传，自动生成缩略图 |
| 📤 **数据导出/导入** | JSON 格式一键备份恢复，日历可导出 Excel |
| 📱 **响应式设计** | 适配桌面端和移动端 |

## 📁 项目结构

```
home/
├── app.py                  # Flask 主应用
├── config.py               # 配置文件
├── requirements.txt        # Python 依赖
├── start.sh                # Linux/iStoreOS 启动脚本
├── start.ps1               # Windows PowerShell 启动脚本
├── data/                   # JSON 数据文件（可读、可迁移）
│   ├── room_types.json
│   ├── rooms.json
│   ├── guests.json
│   ├── bookings.json
│   ├── daily_prices.json   # 每日价格
│   ├── extra_income.json   # 额外收入
│   ├── diary.json          # 运营日记
│   ├── system_logs.json
│   └── quotes.txt          # 名言库
├── logs/                   # 文本日志文件
│   └── system.log
├── static/
│   ├── css/style.css       # 样式表
│   ├── js/main.js          # JavaScript
│   └── uploads/            # 上传的图片
├── templates/              # HTML 模板
│   ├── base.html           # 基础布局
│   ├── index.html          # 仪表盘（含高考倒计时、名言滚动）
│   ├── room_types.html     # 房型管理
│   ├── rooms.html          # 房间管理
│   ├── guests.html         # 客人管理
│   ├── bookings.html       # 预订管理（含快速新增客人）
│   ├── calendar.html       # 日历视图（点击定价、导出Excel）
│   ├── statistics.html     # 统计报表（Chart.js图表）
│   ├── diary.html          # 运营日记
│   └── logs.html           # 系统日志
└── utils/
    ├── data_manager.py     # JSON 数据管理器
    ├── logger.py           # 日志工具
    └── image_handler.py    # 图片处理工具
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

**Linux / iStoreOS：**
```bash
sh start.sh
```

**Windows：**
```powershell
.\start.ps1
```

**或直接运行：**
```bash
python app.py
```

启动后访问：**http://localhost:8080**

### iStoreOS 部署建议

1. 将项目文件夹上传到 iStoreOS，例如 `/opt/homestay/`
2. 确保 iStoreOS 已安装 Python3：
   ```bash
   opkg update
   opkg install python3 python3-pip
   ```
3. 安装依赖：
   ```bash
   pip3 install Flask Pillow openpyxl
   ```
4. 创建开机自启服务（可选）：

   在 `/etc/init.d/homestay` 创建启动脚本：
   ```bash
   #!/bin/sh /etc/rc.common
   START=99
   SERVICE_USE_PID=1

   start() {
       cd /opt/homestay
       python3 app.py &
   }

   stop() {
       killall python3
   }
   ```

   然后执行：
   ```bash
   chmod +x /etc/init.d/homestay
   /etc/init.d/homestay enable
   /etc/init.d/homestay start
   ```

## 💾 数据存储说明

所有数据以 **JSON 格式** 存储在 `data/` 目录下：

- `room_types.json` — 房型数据
- `rooms.json` — 房间数据
- `guests.json` — 客人数据
- `bookings.json` — 预订数据
- `daily_prices.json` — 每日价格（日历定价）
- `extra_income.json` — 额外收入
- `diary.json` — 运营日记
- `system_logs.json` — 操作日志
- `quotes.txt` — 仪表盘名言库

**数据迁移**：直接复制 `data/` 目录即可完成数据迁移。也可通过网页的「导出/导入」功能进行备份与恢复。

**数据备份建议**：定期将 `data/` 目录备份到安全位置。

## 🔧 配置说明

编辑 `config.py` 可修改：

- `PORT` — 服务端口（默认 8080）
- `HOMESTAY_NAME` — 系统名称
- `PAGE_SIZE` — 分页大小
- `MAX_CONTENT_LENGTH` — 上传文件大小限制
- `ALLOWED_EXTENSIONS` — 允许的图片格式

## 📄 许可

MIT License
