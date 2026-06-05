# -*- coding: utf-8 -*-
"""
日志记录工具 - 同时记录到JSON数据文件和文本日志文件
"""

import os
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler

from config import LOG_DIR, LOGS_FILE
from utils.data_manager import DataManager


class SystemLogger:
    """系统日志记录器"""

    _file_logger = None

    @staticmethod
    def _get_file_logger():
        """获取文件日志记录器（单例）"""
        if SystemLogger._file_logger is None:
            log_file = os.path.join(LOG_DIR, 'system.log')
            logger = logging.getLogger('homestay_system')
            logger.setLevel(logging.INFO)
            logger.propagate = False

            # RotatingFileHandler: 每个日志文件最大5MB，保留5个备份
            handler = RotatingFileHandler(
                log_file, maxBytes=5 * 1024 * 1024, backupCount=5,
                encoding='utf-8'
            )
            handler.setFormatter(logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            ))
            logger.addHandler(handler)

            # 同时输出到控制台
            console = logging.StreamHandler()
            console.setFormatter(logging.Formatter(
                '[%(asctime)s] [%(levelname)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            ))
            logger.addHandler(console)

            SystemLogger._file_logger = logger

        return SystemLogger._file_logger

    @staticmethod
    def log(action, details='', user='系统', level='INFO'):
        """记录一条日志（同时记录到JSON和文本文件）"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 1. 记录到文本日志文件
        file_logger = SystemLogger._get_file_logger()
        msg = f'[{user}] {action} - {details}'
        getattr(file_logger, level.lower(), file_logger.info)(msg)

        # 2. 记录到JSON数据文件（供网页查看）
        try:
            logs = DataManager.read_json(LOGS_FILE, [])
            log_entry = {
                'id': DataManager.generate_id(logs),
                'timestamp': timestamp,
                'action': action,
                'details': str(details),
                'user': user,
                'level': level
            }
            logs.append(log_entry)
            # 保留最近2000条记录
            if len(logs) > 2000:
                logs = logs[-2000:]
            DataManager.write_json(LOGS_FILE, logs)
        except Exception as e:
            file_logger.error(f'写入JSON日志失败: {e}')

    @staticmethod
    def info(action, details='', user='系统'):
        """记录信息级别日志"""
        SystemLogger.log(action, details, user, 'INFO')

    @staticmethod
    def warning(action, details='', user='系统'):
        """记录警告级别日志"""
        SystemLogger.log(action, details, user, 'WARNING')

    @staticmethod
    def error(action, details='', user='系统'):
        """记录错误级别日志"""
        SystemLogger.log(action, details, user, 'ERROR')

    @staticmethod
    def get_logs(level=None, page=1, page_size=50):
        """获取JSON格式的日志列表"""
        logs = DataManager.read_json(LOGS_FILE, [])
        if level:
            logs = [l for l in logs if l.get('level') == level]
        # 按时间倒序
        logs.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        total = len(logs)
        start = (page - 1) * page_size
        end = start + page_size
        return {
            'items': logs[start:end],
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size if total > 0 else 1
        }

    @staticmethod
    def clear_logs():
        """清空日志"""
        DataManager.write_json(LOGS_FILE, [])
        # 也清空文本日志（通过重新创建文件）
        log_file = os.path.join(LOG_DIR, 'system.log')
        if os.path.exists(log_file):
            open(log_file, 'w').close()
        SystemLogger.info('日志已清空')
