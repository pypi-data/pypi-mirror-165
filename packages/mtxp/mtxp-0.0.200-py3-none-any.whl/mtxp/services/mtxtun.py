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
import shutil
from mtlibs import process_helper

import logging
logger = logging.getLogger(__name__)



def startup_mtxtun(logfile_path:str):
    Path(logfile_path).parent.mkdir(parents=True,mode=0o700, exist_ok=True)
    with open(logfile_path,'w') as logfile:
        logfile.write("=========================  start mtxtun ==================================\n")
        data_dir =join(Path(__file__).parent.parent,"data")
        logger.debug(f"data dir: {data_dir}")
        if not shutil.which('mtxtun'):
            logger.info("安装mtxtun命令")
            cp_install_mtxtun = process_helper.exec("npm i -g mtxtun@^0.0.23")
            if cp_install_mtxtun.returncode != 0:
                logger.warn("安装mtxtun 失败？")

        data_dir =join(Path(__file__).parent.parent,"data")
        logger.info(f"data dir: {data_dir}")
        p = subprocess.Popen(shlex.split(f"mtxtun --config {data_dir}/mtxtun.yml"), stdout=logfile, stderr=logfile)



    

