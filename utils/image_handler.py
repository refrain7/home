# -*- coding: utf-8 -*-
"""
图片处理工具 - 处理图片上传、验证、缩略图生成
"""

import os
import uuid
import hashlib
from datetime import datetime
from PIL import Image

from config import UPLOAD_DIR, ALLOWED_EXTENSIONS


class ImageHandler:
    """图片处理器"""

    THUMBNAIL_SIZE = (300, 300)  # 缩略图尺寸
    MAX_IMAGE_SIZE = (1920, 1920)  # 最大图片尺寸

    @staticmethod
    def allowed_file(filename):
        """检查文件扩展名是否允许"""
        if '.' not in filename:
            return False
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in ALLOWED_EXTENSIONS

    @staticmethod
    def get_extension(filename):
        """获取文件扩展名（小写）"""
        if '.' not in filename:
            return ''
        return filename.rsplit('.', 1)[1].lower()

    @staticmethod
    def generate_filename(original_filename, prefix='img'):
        """生成唯一文件名"""
        ext = ImageHandler.get_extension(original_filename)
        unique_id = uuid.uuid4().hex[:12]
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        return f'{prefix}_{timestamp}_{unique_id}.{ext}'

    @staticmethod
    def save_image(file_storage, subfolder='', prefix='img'):
        """
        保存上传的图片
        返回: {'success': True, 'filename': 'xxx.jpg', 'thumbnail': 'thumb_xxx.jpg'}
        或 {'success': False, 'error': '错误信息'}
        """
        if not file_storage or not file_storage.filename:
            return {'success': False, 'error': '没有选择文件'}

        if not ImageHandler.allowed_file(file_storage.filename):
            return {'success': False, 'error': f'不支持的文件格式，仅支持: {", ".join(ALLOWED_EXTENSIONS)}'}

        try:
            # 生成唯一文件名
            filename = ImageHandler.generate_filename(file_storage.filename, prefix)
            thumb_filename = f'thumb_{filename}'

            # 确定存储路径
            if subfolder:
                save_dir = os.path.join(UPLOAD_DIR, subfolder)
                os.makedirs(save_dir, exist_ok=True)
                filepath = os.path.join(save_dir, filename)
                thumb_path = os.path.join(save_dir, thumb_filename)
            else:
                filepath = os.path.join(UPLOAD_DIR, filename)
                thumb_path = os.path.join(UPLOAD_DIR, thumb_filename)

            # 打开图片
            img = Image.open(file_storage)

            # 转换为RGB（处理PNG透明度等）
            if img.mode in ('RGBA', 'P', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')

            # 限制最大尺寸
            img.thumbnail(ImageHandler.MAX_IMAGE_SIZE, Image.LANCZOS)

            # 保存原图
            img.save(filepath, quality=85, optimize=True)

            # 生成并保存缩略图
            thumb = img.copy()
            thumb.thumbnail(ImageHandler.THUMBNAIL_SIZE, Image.LANCZOS)
            thumb.save(thumb_path, quality=75, optimize=True)

            # 返回相对路径
            if subfolder:
                rel_path = f'uploads/{subfolder}/{filename}'
                rel_thumb = f'uploads/{subfolder}/{thumb_filename}'
            else:
                rel_path = f'uploads/{filename}'
                rel_thumb = f'uploads/{thumb_filename}'

            return {
                'success': True,
                'filename': filename,
                'thumbnail': thumb_filename,
                'path': rel_path,
                'thumb_path': rel_thumb,
                'size': os.path.getsize(filepath)
            }

        except Exception as e:
            return {'success': False, 'error': f'图片处理失败: {str(e)}'}

    @staticmethod
    def delete_image(filename, subfolder=''):
        """删除图片及其缩略图"""
        try:
            thumb_filename = f'thumb_{filename}'
            if subfolder:
                filepath = os.path.join(UPLOAD_DIR, subfolder, filename)
                thumb_path = os.path.join(UPLOAD_DIR, subfolder, thumb_filename)
            else:
                filepath = os.path.join(UPLOAD_DIR, filename)
                thumb_path = os.path.join(UPLOAD_DIR, thumb_filename)

            for p in [filepath, thumb_path]:
                if os.path.exists(p):
                    os.remove(p)
            return True
        except Exception:
            return False
