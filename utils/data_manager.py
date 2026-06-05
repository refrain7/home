# -*- coding: utf-8 -*-
"""
JSON 数据管理器 - 提供统一的数据读写接口
数据以JSON格式存储，兼具可读性和可迁移性
"""

import json
import os
import threading
import time
from datetime import datetime


class DataManager:
    """JSON文件数据管理器，线程安全"""

    _locks = {}
    _lock_creation = threading.Lock()

    @staticmethod
    def _get_lock(filepath):
        """获取文件级别的锁"""
        if filepath not in DataManager._locks:
            with DataManager._lock_creation:
                if filepath not in DataManager._locks:
                    DataManager._locks[filepath] = threading.Lock()
        return DataManager._locks[filepath]

    @staticmethod
    def read_json(filepath, default=None):
        """读取JSON文件，返回数据"""
        if default is None:
            default = []
        lock = DataManager._get_lock(filepath)
        with lock:
            try:
                if not os.path.exists(filepath):
                    DataManager._ensure_file(filepath, default)
                    return default.copy() if isinstance(default, list) else dict(default)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data if data is not None else default
            except (json.JSONDecodeError, IOError):
                return default.copy() if isinstance(default, list) else dict(default)

    @staticmethod
    def write_json(filepath, data):
        """写入JSON文件，带缩进格式化"""
        lock = DataManager._get_lock(filepath)
        with lock:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            # 先写入临时文件，再原子替换
            tmp_file = filepath + '.tmp'
            with open(tmp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            os.replace(tmp_file, filepath)

    @staticmethod
    def _ensure_file(filepath, default):
        """确保数据文件存在"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=2, default=str)

    @staticmethod
    def generate_id(data_list):
        """生成唯一ID"""
        if not data_list:
            return 1
        max_id = max((item.get('id', 0) for item in data_list), default=0)
        return max_id + 1

    @staticmethod
    def get_by_id(data_list, item_id):
        """根据ID获取数据项"""
        for item in data_list:
            if item.get('id') == item_id:
                return item
        return None

    @staticmethod
    def get_index_by_id(data_list, item_id):
        """根据ID获取数据项索引"""
        for i, item in enumerate(data_list):
            if item.get('id') == item_id:
                return i
        return -1

    @staticmethod
    def update_by_id(data_list, item_id, updates):
        """根据ID更新数据项"""
        idx = DataManager.get_index_by_id(data_list, item_id)
        if idx >= 0:
            data_list[idx].update(updates)
            data_list[idx]['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return True
        return False

    @staticmethod
    def delete_by_id(data_list, item_id):
        """根据ID删除数据项"""
        idx = DataManager.get_index_by_id(data_list, item_id)
        if idx >= 0:
            data_list.pop(idx)
            return True
        return False

    @staticmethod
    def query(data_list, filters=None, sort_key=None, sort_reverse=False,
              page=1, page_size=20):
        """通用查询方法，支持过滤、排序、分页"""
        if filters is None:
            filters = {}

        result = []
        for item in data_list:
            match = True
            for key, value in filters.items():
                if value is None or value == '':
                    continue
                item_val = item.get(key)
                if isinstance(value, str) and isinstance(item_val, str):
                    if value.lower() not in item_val.lower():
                        match = False
                        break
                elif isinstance(value, list):
                    if item_val not in value:
                        match = False
                        break
                elif item_val != value:
                    match = False
                    break
            if match:
                result.append(item)

        # 排序
        if sort_key:
            result.sort(key=lambda x: x.get(sort_key, ''), reverse=sort_reverse)

        # 分页
        total = len(result)
        start = (page - 1) * page_size
        end = start + page_size
        items = result[start:end]

        return {
            'items': items,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if total > 0 else 1
        }

    @staticmethod
    def search(data_list, keyword, search_fields):
        """全文搜索 - 在指定字段中搜索关键词"""
        if not keyword or not search_fields:
            return data_list

        keyword_lower = keyword.lower()
        result = []
        for item in data_list:
            for field in search_fields:
                val = str(item.get(field, '')).lower()
                if keyword_lower in val:
                    result.append(item)
                    break
        return result
