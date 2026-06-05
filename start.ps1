<# 
    民宿房间管理系统 - Windows 启动脚本
    用法: .\start.ps1
#>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  民宿房间管理系统" -ForegroundColor Yellow
Write-Host "  数据目录: $ScriptDir\data" -ForegroundColor Gray
Write-Host "  上传目录: $ScriptDir\static\uploads" -ForegroundColor Gray
Write-Host "  日志目录: $ScriptDir\logs" -ForegroundColor Gray
Write-Host "=========================================" -ForegroundColor Cyan

# 确保目录存在
New-Item -ItemType Directory -Force -Path "data", "logs", "static\uploads", "static\uploads\room_types" | Out-Null

# 检查 Python
try {
    python --version | Out-Null
} catch {
    Write-Host "错误: 未找到 Python，请先安装 Python 3" -ForegroundColor Red
    exit 1
}

# 检查并安装依赖
Write-Host "检查依赖..." -ForegroundColor Yellow
python -c "import flask" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "安装 Flask..." -ForegroundColor Yellow
    pip install Flask Pillow
}

# 启动
Write-Host "启动服务..." -ForegroundColor Green
python app.py
