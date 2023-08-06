from subprocess import CompletedProcess
import sys
from pathlib import Path
from mtlibs import process_helper
from dotenv import load_dotenv, find_dotenv
from mtlibs.docker_helper import isInContainer


def setup_mtxlib():
    print("安装mtxlib")
    npm_install_mtxlib_cp = process_helper.exec("yarn global add mtxlib")
    if npm_install_mtxlib_cp.returncode == 0:
        print("安装mtxlib 安装")

    print("启动sm")
    sm_cp = process_helper.exec("sm")
    if sm_cp.returncode == 0:
        print("sm_cp 运行结果")