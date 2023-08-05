import logging

class logger(logging.Logger):
    def __init__(self):
        # 文件的命名
        # self.logname = os.path.join(log_path, '%s.log' % time.strftime('%Y_%m_%d'))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 日志输出格式
        self.formatter = logging.Formatter('%(asctime)s (%(thread)s) [%(levelname)s] %(module)s:%(lineno)d %(message)s',
                                           datefmt='%Y-%m-%d %H:%M:%S')
        # 创建一个StreamHandler,用于输出到控制台
        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.DEBUG)
        self.ch.setFormatter(self.formatter)
        self.logger.addHandler(self.ch)

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        # fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')  # 这个是python3的
        # fh.setLevel(logging.DEBUG)
        # fh.setFormatter(self.formatter)
        # self.logger.addHandler(fh)
        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(self.ch)
        # self.logger.removeHandler(fh)
        # 关闭打开的文件
        # fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)

log = logger().logger