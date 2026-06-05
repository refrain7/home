/**
 * 民宿房间管理系统 - 主 JavaScript 文件
 * 提供全局功能：Toast、模态框、搜索、导出导入等
 */

// ==================== Toast 通知 ====================

function showToast(message, type = 'info', duration = 3000) {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <span>${message}</span>
        <button class="toast-dismiss" onclick="this.parentElement.remove()">✕</button>`;
    container.appendChild(toast);

    if (duration > 0) {
        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.opacity = '0';
                toast.style.transform = 'translateX(100%)';
                toast.style.transition = 'all 0.3s ease';
                setTimeout(() => toast.remove(), 300);
            }
        }, duration);
    }
}

// ==================== 模态框 ====================

function openModal() {
    document.getElementById('modalOverlay').style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    document.getElementById('modalOverlay').style.display = 'none';
    document.body.style.overflow = '';
}

// 点击遮罩关闭
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('modalOverlay').addEventListener('click', function(e) {
        if (e.target === this) closeModal();
    });

    // ESC 关闭
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeModal();
    });
});

// ==================== HTML 转义 ====================

function escHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

// ==================== 分页渲染 ====================

function renderPagination(containerId, data, loadCallback) {
    const container = document.getElementById(containerId);
    if (!container || data.total_pages <= 1) {
        if (container) container.innerHTML = '';
        return;
    }

    let html = '';
    html += `<button ${data.page <= 1 ? 'disabled' : ''} onclick="goToPage(${data.page - 1}, '${containerId}', arguments[0])">上一页</button>`;

    const totalPages = data.total_pages;
    const currentPage = data.page;
    const maxButtons = 7;

    let startPage = Math.max(1, currentPage - Math.floor(maxButtons / 2));
    let endPage = Math.min(totalPages, startPage + maxButtons - 1);
    if (endPage - startPage < maxButtons - 1) {
        startPage = Math.max(1, endPage - maxButtons + 1);
    }

    if (startPage > 1) {
        html += `<button onclick="goToPage(1, '${containerId}', event)">1</button>`;
        if (startPage > 2) html += '<span class="page-info">...</span>';
    }

    for (let i = startPage; i <= endPage; i++) {
        html += `<button class="${i === currentPage ? 'active' : ''}" onclick="goToPage(${i}, '${containerId}', event)">${i}</button>`;
    }

    if (endPage < totalPages) {
        if (endPage < totalPages - 1) html += '<span class="page-info">...</span>';
        html += `<button onclick="goToPage(${totalPages}, '${containerId}', event)">${totalPages}</button>`;
    }

    html += `<button ${data.page >= totalPages ? 'disabled' : ''} onclick="goToPage(${data.page + 1}, '${containerId}', event)">下一页</button>`;
    html += `<span class="page-info">共 ${data.total} 条</span>`;

    container.innerHTML = html;
}

function goToPage(page, containerId, event) {
    // 通过全局变量更新页码（各页面有自己的 currentPage）
    if (typeof currentPage !== 'undefined') {
        currentPage = page;
    }
    // 触发对应页面的加载函数
    const container = document.getElementById(containerId);
    if (container) {
        // Dispatch a custom event that the page can listen to
        window.dispatchEvent(new CustomEvent('pageChange', { detail: { page, containerId } }));
    }
    // Try to call the load function directly
    if (containerId === 'typePagination' && typeof loadTypes === 'function') { currentPage = page; loadTypes(); }
    else if (containerId === 'roomPagination' && typeof loadRooms === 'function') { currentPage = page; loadRooms(); }
    else if (containerId === 'guestPagination' && typeof loadGuests === 'function') { currentPage = page; loadGuests(); }
    else if (containerId === 'bookingPagination' && typeof loadBookings === 'function') { currentPage = page; loadBookings(); }
    else if (containerId === 'logPagination' && typeof loadLogs === 'function') { currentPage = page; loadLogs(); }
}

// ==================== 全局搜索 ====================

let searchTimeout;
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('globalSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const keyword = this.value.trim();
            if (keyword.length < 1) {
                document.getElementById('searchResults').style.display = 'none';
                return;
            }
            searchTimeout = setTimeout(() => doGlobalSearch(keyword), 400);
        });

        // 点击其他地方关闭搜索结果
        document.addEventListener('click', function(e) {
            const results = document.getElementById('searchResults');
            if (results && !e.target.closest('.search-box')) {
                results.style.display = 'none';
            }
        });
    }

    // 时钟更新
    updateClock();
    setInterval(updateClock, 10000);
});

function updateClock() {
    const now = new Date();
    const timeStr = now.toLocaleString('zh-CN', {
        year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit', second: '2-digit'
    });
    const el = document.getElementById('currentTime');
    if (el) el.textContent = timeStr;
}

async function doGlobalSearch(keyword) {
    try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(keyword)}`);
        const json = await res.json();
        if (!json.success) return;

        const data = json.data;
        const container = document.getElementById('searchResults');
        let html = '';

        const hasResults = data.room_types.length > 0 || data.rooms.length > 0 ||
                          data.guests.length > 0 || data.bookings.length > 0;

        if (!hasResults) {
            html = '<div class="search-section"><p class="text-muted" style="padding:12px;text-align:center;">未找到匹配结果</p></div>';
        } else {
            if (data.bookings.length > 0) {
                html += '<div class="search-section"><h4>📋 预订</h4>';
                data.bookings.forEach(b => {
                    html += `<div class="search-item" onclick="location.href='/bookings'">
                        ${escHtml(b.guest_name)} - ${escHtml(b.room_number)} (${b.check_in_date}~${b.check_out_date})
                    </div>`;
                });
                html += '</div>';
            }
            if (data.guests.length > 0) {
                html += '<div class="search-section"><h4>👤 客人</h4>';
                data.guests.forEach(g => {
                    html += `<div class="search-item" onclick="location.href='/guests'">
                        ${escHtml(g.name)} - ${escHtml(g.phone || '无手机号')}
                    </div>`;
                });
                html += '</div>';
            }
            if (data.rooms.length > 0) {
                html += '<div class="search-section"><h4>🚪 房间</h4>';
                data.rooms.forEach(r => {
                    html += `<div class="search-item" onclick="location.href='/rooms'">
                        房间 ${escHtml(r.room_number)} (${escHtml(r.status)})
                    </div>`;
                });
                html += '</div>';
            }
            if (data.room_types.length > 0) {
                html += '<div class="search-section"><h4>🏠 房型</h4>';
                data.room_types.forEach(t => {
                    html += `<div class="search-item" onclick="location.href='/room-types'">
                        ${escHtml(t.name)} - ¥${t.base_price}
                    </div>`;
                });
                html += '</div>';
            }
        }

        container.innerHTML = html;
        container.style.display = 'block';
    } catch (e) {
        console.error('搜索失败:', e);
    }
}

// ==================== 数据导出/导入 ====================

async function exportData() {
    try {
        const res = await fetch('/api/export');
        const json = await res.json();
        if (!json.success) {
            showToast('导出失败', 'error');
            return;
        }

        const blob = new Blob([JSON.stringify(json.data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        const now = new Date().toISOString().slice(0, 10);
        a.href = url;
        a.download = `homestay_backup_${now}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        showToast('数据导出成功', 'success');
    } catch (e) {
        showToast('导出失败: ' + e.message, 'error');
    }
}

async function importData(input) {
    const file = input.files[0];
    if (!file) return;

    if (!confirm(`确定要导入文件 "${file.name}" 中的数据吗？\n这将覆盖现有数据，请确保已备份！`)) {
        input.value = '';
        return;
    }

    try {
        const text = await file.text();
        const data = JSON.parse(text);

        const res = await fetch('/api/import', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const json = await res.json();
        if (json.success) {
            showToast(json.message || '导入成功', 'success');
            // 刷新当前页面
            setTimeout(() => location.reload(), 1000);
        } else {
            showToast(json.error || '导入失败', 'error');
        }
    } catch (e) {
        showToast('导入失败，请检查文件格式: ' + e.message, 'error');
    }
    input.value = '';
}

// ==================== 侧边栏切换（移动端） ====================

document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }
});
