import logging
logger = logging.getLogger(__name__)

from  .config import config # 导入存储配置的字典
def get(name, default=None):
    result = getattr(config["default"],name)
    return result or default

def getHtmlRoot():
    return getattr(config["default"],"HTML_ROOT_DIR")

def getLogDirBase():
    return getattr(config["default"],"LOG_DIR")