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

logger = logging.getLogger(__name__)


class TorService():
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(TorService, "_instance"):
            with TorService._instance_lock:
                if not hasattr(TorService, "_instance"):
                    # 类加括号就回去执行__new__方法，__new__方法会创建一个类实例：Singleton()
                    TorService._instance = object.__new__(cls)  
                    # 继承object类的__new__方法，类去调用方法，说明是函数，要手动传cls
        return TorService._instance  #obj1

    def __init__(self):
        self.logdirBase = settings.get("LOG_DIR")
        self.logfile_path = path.join(self.logdirBase, ".tor.log")
        Path(self.logfile_path).parent.mkdir(
            parents=True, mode=0o700, exist_ok=True)
        self.logfile = open(self.logfile_path, 'a')
        self.write_log("\n=======  start tor ========\n")
        self.write_log(f"pid: {os.getpid()}")
        self.thread = threading.Thread(target=self.thread_start)

    def write_log(self, message: str):
        self.logfile.write(f"{message}\n")
        self.logfile.flush()

    def start(self):       

        self.thread.start()

    def thread_start(self):
        torcc = [
            "VirtualAddrNetworkIPv4 10.192.0.0/10",
            "AutomapHostsOnResolve 1",
            "AvoidDiskWrites 1",
            "SocksPort 0.0.0.0:9050",
            # "TransPort 127.0.0.1:9040",
            # "DNSPort 127.0.0.1:5353",
            "CookieAuthentication 1",
            # "ControlPort 0.0.0.0:9051",
            "HashedControlPassword 16:E600ADC1B52C80BB6022A0E999A7734571A451EB6AE50FED489B72E3DF",
            # "HiddenServiceDir /tmp/hidden",
            # "HiddenServicePort 80 127.0.0.1:80",
            # "HiddenServicePort 22 127.0.0.1:22",
            # "HiddenServicePort 443 127.0.0.1:443"
        ]
        # 使用外部代理链接tor网络。
        TOR_SOCKS5PROXY = os.environ.get("TOR_SOCKS5PROXY")
        if TOR_SOCKS5PROXY:
            torcc.append(f"Socks5Proxy {TOR_SOCKS5PROXY}")

        torcc_path = "/tmp/torcc"
        Path(torcc_path).touch(mode=0o700)

        torcc_content = "\n".join(torcc)
        self.write_log(f"TORCC:\n{torcc_content}")
        # print(torcc_content)
        with open(torcc_path, "w") as f:
            f.write(torcc_content)

        self.target_process = subprocess.Popen(shlex.split(f"tor -f {torcc_path}"),
                            stdout=self.logfile,
                            stderr=self.logfile)
