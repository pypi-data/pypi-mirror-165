#!/usr/bin/env python3
import sys
import os
from os.path import join
import subprocess
from pathlib import Path
import time
import subprocess
from os import path
import threading
import yaml
import logging
from .. import settings
from mtlibs import process_helper
from mtlibs import mtutils
import platform

logger = logging.getLogger(__name__)

class TailscaleService():
    def __init__(self):
        self.html_root = settings.getHtmlRoot()
        logger.info(f"html root {self.html_root}")
        self.smapiRoot = "/mtxp"        

    def start(self):
        logger.info("启动taillscale 服务")
        port = 80
        check_port = mtutils.get_tcp_open_port(80)
        if not check_port:
            logger.info(f"tcp port opend {port},skip start nginx")
        else:
            logger.info("[TODO:] start tailscale")

    def stop(self):
        pass