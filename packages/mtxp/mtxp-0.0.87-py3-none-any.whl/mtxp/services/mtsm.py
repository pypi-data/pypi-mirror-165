#!/usr/bin/env python3
import sys
import os
from os.path import join
import subprocess
from pathlib import Path
import time
import subprocess
import traceback
import shlex
from .. import settings
from os import path
import threading
import logging
import subprocess
import shutil

logger = logging.getLogger(__name__)


class MtsmService():
    # _instance_lock = threading.Lock()
    def __init__(self):
        self.logdirBase = settings.get("LOG_DIR")
        self.logfile = open(os.path.join(self.logdirBase,".mtsm.log"), "a")

    def write_log(self, message: str):
        self.logfile.write(f"{message}\n")
        self.logfile.flush()

    def start(self):

        p1 = shutil.which("mtsm.py")
        logger.info(f"路径{p1}")
        # cp_command_v  = subprocess.run(shlex.split("command -v mtsm.py"), shell=True)
        if not shutil.which("mtsm.py"):
            logger.info("安装mtsm.py命令")
            subprocess.run(shlex.shlex("python3 -m pip install mtsm"))

        logger.info("启动mtsm")
        # cp = subprocess.run(shlex.split("mtsm"))
        self.target_process = subprocess.Popen(shlex.split(f"mtsm"),
                            stdout=self.logfile,
                            stderr=self.logfile)

        

    