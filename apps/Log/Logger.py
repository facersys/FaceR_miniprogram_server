# -*- coding: utf-8 -*-

import logging
from logging import handlers


class Logger:
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(
            self,
            filename,
            level=logging.INFO,
            when='D',
            back_count=10,
            format_str='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    ):
        self.logger = logging.getLogger(filename)

        # 设置日志格式
        format_str = logging.Formatter(format_str)
        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))
        # 输出在屏幕上
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)

        # 往指定文件写入日志，指定时间间隔
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒, M 分, H 小时, D 天, W 每星期（interval==0时代表星期一）, midnight 每天凌晨
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=back_count, encoding='utf-8')
        th.setFormatter(format_str)

        # 添加对象到logger
        self.logger.addHandler(sh)
        self.logger.addHandler(th)


if __name__ == '__main__':
    log = Logger('all.log', level='debug')
    log.logger.debug('debug')
    log.logger.info('info')
    log.logger.warning('警告')
    log.logger.error('报错')
    log.logger.critical('严重')
