#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Date    : 2025/5/10 17:58
@Author  : Poco Ray
@File    : log_control.py
@Software: PyCharm
@Desc    : Description
"""
import logging
from logging import handlers
from colorlog import ColoredFormatter
import os
from typing import Optional
from config.global_config import LOG_PATH


class Logger:
    """自定义日志记录器，支持彩色控制台输出和文件日志"""

    def __init__(self, name: str, log_file: Optional[str] = None, level: int = logging.DEBUG):
        """
        初始化日志记录器
        :param name: 日志记录器名称, 通常是模块名
        :param log_file: 日志文件路径（可选）, 如果不指定，则只输出到控制台
        :param level: 日志级别（默认为DEBUG）
        """
        # 获取或创建日志记录器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 避免重复添加处理器
        if not self.logger.handlers:
            # 创建控制台处理器（带颜色格式）
            self._add_console_handler()

            # 如果指定了日志文件，创建文件处理器
            if log_file:
                self._add_file_handler(log_file)

    def _add_console_handler(self):
        """添加彩色控制台日志处理器"""
        # 颜色格式配置
        console_format = (
            '%(log_color)s[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s'
        )
        formatter = ColoredFormatter(
            console_format,
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_black',
            }
        )
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def _add_file_handler(self, log_file: str):
        """添加文件日志处理器"""
        # 确保日志目录存在
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        # 文件日志格式
        file_format = (
            '[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s'
        )
        formatter = logging.Formatter(file_format, datefmt="%Y-%m-%d %H:%M:%S")

        # 创建轮转文件处理器（每个文件最大5MB，保留5个备份）
        file_handler = handlers.RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


if __name__ == '__main__':
    # 测试彩色日志输出
    logger = Logger("test_logger", LOG_PATH)

    # 测试不同日志级别
    logger.logger.debug("This is a debug message")
    logger.logger.info("This is an info message")
    logger.logger.warning("This is a warning message")
    logger.logger.error("This is an error message")
    logger.logger.critical("This is a critical message")

    # 测试没有文件日志的实例
    console_only_logger = Logger("console_only")
    console_only_logger.logger.info("This message appears only in console")