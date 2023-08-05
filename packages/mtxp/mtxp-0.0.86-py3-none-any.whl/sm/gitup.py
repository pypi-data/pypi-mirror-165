import sys
import os
from mtlibs.docker_helper import isInContainer
from mtlibs import process_helper
from pathlib import Path
import logging

from dotenv import load_dotenv, find_dotenv
from mtlibs.github import gitup
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

logging.basicConfig(level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def console_script_entry():
    logger.info("(试验), 直接clone 并启动开发容器")
    env_gitup = os.environ.get("MTX_GITUP")
    if env_gitup:
        logger.info(f"gitup 环境变量:{env_gitup}")
        items = env_gitup.split("|")
        for item in items:
            gitup(item)